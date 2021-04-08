from discord.ext import commands, tasks
import os, discord, db, re, utils
import mysql.connector as mysql
from . import templates as tmp
from config import CONFIG
from log import logger

# CMC API CALLS
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

class WatchCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.channel_id = 829037611841749063
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.check_prices.start()
        
    def cog_unload(self):
        self.check_prices.cancel()

    @tasks.loop(minutes=15.0)
    async def check_prices(self):
        channel = self.bot.get_channel(self.channel_id)

        dbh = db.get_dbh()
        cur = dbh.cursor(buffered=True)
        
        sql = 'SELECT * FROM watch_cog WHERE status=0'
        ret = db.select(cur, sql, null_as_blank=False)

        symbols = set() # Get unique set of SYMBOLS to poll from CMC
        [symbols.add(r['symbol']) for r in ret]

        if not len(symbols):
            return
        
        prices = self.fetch_data(symbols)

        if prices['stat'] != 0:
            await channel.send(prices['msg'])
            return

        user_map = {}
        for r in ret:
            user   = r['user']  # readability
            symbol = r['symbol']

            if symbol not in prices.keys(): # more readable price lookup
                bound = None
                if   r['upper'] and prices['data'][symbol] >= r['upper']: bound = r['upper']
                elif r['lower'] and prices['data'][symbol] <= r['lower']: bound = r['lower']

                # Nothing to do, go to next
                if bound is None: continue

                if user   not in user_map.keys():       user_map[user]         = {}
                if symbol not in user_map[user].keys(): user_map[user][symbol] = []

                user_map[user][symbol].append({
                    'BOUND': f'${ utils.atos(bound) }',
                    'PRICE': f'${ utils.atos(prices["data"][symbol]) }',
                })

                sql = 'UPDATE watch_cog SET status=1 WHERE id=%s'
                cur.execute(sql, (r['id'],))

        for user in user_map.keys():
            table = tmp.gen_notification_table(user_map[user])
            await channel.send(f"<@{ user }> I have an update for you!\n```{ table }\n```")

        dbh.commit()
        cur.close()
        dbh.close()
        return

    @commands.command(name="watch", pass_context=True)
    async def watch(self, ctx):
        # Only allow watch command in "crypto-prices" channel
        if ctx.channel.id != self.channel_id:
            await ctx.channel.send("Please send watch commands in <#829037611841749063>")
            return

        m = re.match(rf'{ CONFIG["PREFIX"] }watch ([a-zA-Z0-9]+) (?:\$)?(\d+(?:\.\d+)?)(?: (?:\$)?(\d+(?:\.\d+)?))?$', ctx.message.content)
        if m is None:
            await ctx.channel.send(
            f"Could not parse required information, please follow the format:\n`{ CONFIG['PREFIX'] }watch SYMBOL [$]0[.00][ [$]0[.00]]`"
            )
            return

        symbol, price_1, price_2 = m.groups()
        ubnd = lbnd = None

        symbol = symbol.upper()
        prices = self.fetch_data([symbol])
        if prices['stat'] != 0:
            await ctx.channel.send(prices['msg'])
            return
        
        cur_price = prices['data'][symbol]
        if price_2 is not None:
            ubnd = max(utils.atof(price_1), utils.atof(price_2))
            lbnd = min(utils.atof(price_1), utils.atof(price_2))
        else:
            # preserves None value for unused bound
            bnd  = utils.atof(price_1)
            if cur_price > bnd: lbnd = bnd
            else:               ubnd = bnd

        if ubnd == 0 or lbnd == 0:
            await ctx.channel.send("You are not allowed to enter 0 as a price marker, please try again.")
            return

        dbh = db.get_dbh()
        cur = dbh.cursor(buffered=True)

        sql = 'INSERT INTO watch_cog (symbol, user, lower, upper) VALUES (%s, %s, %s, %s)'
        cur.execute(sql, (symbol, ctx.author.id, lbnd, ubnd))

        await ctx.channel.send(f"Orders recieved, now watching *{ symbol }*")

        dbh.commit()
        cur.close()
        dbh.close()

        return

    @commands.command(name="watchlist", pass_context=True)
    async def watchlist(self, ctx):
        dbh = db.get_dbh()
        cur = dbh.cursor(buffered=True)

        sql = 'SELECT * FROM watch_cog WHERE user=%s AND status=0'
        ret = db.select(cur, sql, (ctx.author.id,))
        msg = ''
        for i, r in enumerate(ret):
            if i > 0: msg += '\n'
            msg += f'ID: { r["id"] } | Symbol: { r["symbol"] }'
            if r['lower'] != 0: msg += f' | Lower Bound: { r["lower"] }'
            if r['upper'] != 0: msg += f' | Upper Bound: { r["upper"] }'

        if len(msg): await ctx.channel.send(msg)
        else:        await ctx.channel.send("You are not currently tracking any coins")

        cur.close()
        dbh.close()
        return

    def fetch_data(self, symbols):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        parameters = {
            'symbol' : ','.join(symbols),
            'convert': 'USD'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': CONFIG['CMCKEY'],
        }

        session = Session()
        session.headers.update(headers)

        try:
            ret = {
                'data': {},
                'stat': 0,
                'msg' : '',
            }
            response = session.get(url, params=parameters)

            data  = json.loads(response.text)
            stat  = data.get('status', {})
            error = stat.get('error_code',  999)

            if error != 0:
                ret['stat'] = error
                ret['msg'] = "I've encountered an HTTP error, please try again.\n<@280231128852332544> I'm having issues..."
                logger.error(f"Could not fetch from CMC: { stat }")
                return ret

            for symbol, info in json.loads(response.text).get('data', {}).items():
                price = info.get('quote', {}).get('USD', {}).get('price', None)
                if price is None:
                    logger.error(f"Parsed '{ price }' for price on symbol '{ symbol }'")
                    ret['stat'] = -1
                    ret['msg'] = "Failed to parse price information, please try again.\n<@280231128852332544> I'm having issues..."
                    return ret

                ret['data'][symbol] = price
            return ret
        
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            logger.error(e)
            ret['stat'] = -1
            return ret

def setup(bot: commands.Bot):
    bot.add_cog(WatchCog(bot))
