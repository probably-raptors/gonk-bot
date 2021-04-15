from discord.ext import commands, tasks
import os, discord, db, re, utils, argparse
import mysql.connector as mysql
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

        self.help_msg = (
            "**Watch Cog**: A small discord utility that helps *you* manage *your* "
            "investments. From notifications for price targets being met, to quick "
            "up to date info on how your favorite token is running, this tool is "
            "the only one for you."
        )

        self.dispatch = {
            'HELP': {
                'call': self.watch_help,
                'info': 'Display this message.',
            },
            'ADD': {
                'call': self.add_token,
                'info': 'Start tracking new coin.',
            },
            'DEL': {
                'call': self.del_token,
                'info': 'Stop tracking coin(s).',
            },
            'LIST': {
                'call': self.list_token,
                'info': 'List all tracked coin(s).',
            },
            'INFO': {
                'call': self.token_info,
                'info': 'Return current info of coin(s).',
            },
        }


    @commands.Cog.listener()
    async def on_ready(self):
        self.check_prices.start()
        
    def cog_unload(self):
        self.check_prices.cancel()

    @commands.command(name="watch", pass_context=True)
    async def watchcli(self, ctx, mode=None, *args):
        # Only allow watch command in "crypto-prices" channel
        if ctx.channel.id != self.channel_id and ctx.channel.id != CONFIG['DEV_CHANNEL']:
            await ctx.channel.send(f"Please send watch commands in <#{ CONFIG['DEV_CHANNEL'] }>")
            return

        if mode is not None and mode.upper() in self.dispatch.keys():
            await self.dispatch[mode.upper()]['call'](ctx, *args)
        else:
            await self.dispatch['HELP']['call'](ctx)
        return

    async def watch_help(self, ctx, *args):
        await ctx.channel.send(self.help_msg)
        for cmd in self.dispatch.keys():
            await ctx.channel.send(f'**{ cmd.lower() }**: *{ self.dispatch[cmd]["info"] }*')

        await ctx.channel.send(f'For more information on a given command, please use `{ CONFIG["PREFIX"] }watch COMMAND help`')
        return


    async def add_token(self, ctx, *args):
        m = re.match(rf'([a-zA-Z0-9]+) (?:\$)?(\d+(?:\.\d+)?)(?: (?:\$)?(\d+(?:\.\d+)?))?$', ' '.join(args))
        if m is None: # show help
            embed = discord.Embed(title='Help', description='add accepts 3 positional arguments: `SYMBOL PRICE PRICE`')
            
            #\u200b for "no name field"
            embed.add_field(name='Formatting', value=f"`{ CONFIG['PREFIX'] }watch add SYMBOL [$]0[.00][ [$]0[.00]]`", inline=False)
            embed.add_field(name='How it works', inline=False, value=(
                "The add command takes 1 coin symbol like `XRP` or `BTC` and 1 or 2 prices to use "
                "as targets for the watcher to track. When 2 prices are given, the lower of the 2 "
                "is considered the Lower Bound, while the other is considered the Upper. If only "
                "1 price is found, it is compared to the current price of the coin and is then "
                "assigned as an Upper or Lower bound accordingly."
            ))

            embed.add_field(name='Bounds', inline=False, value=(
                "Upper and Lower Bounds act as targets for the tracker to look for. You will be "
                "notified whenever the current price goes **above** the Upper Bound, and whenever "
                "the current price goes **below** the Lower Bound."
            ))

            await ctx.channel.send(embed=embed)
            return
            

        symbol, price_1, price_2 = m.groups()
        ubnd = lbnd = None

        symbol = symbol.upper()

        prices = self.fetch_data([symbol])
        if prices['stat'] != 0:
            embed = discord.Embed(title=f"Error: { prices['stat'] }", description=prices['msg'], color=0xa33b24)
            await ctx.channel.send(embed=embed)
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

        if (ubnd is not None and utils.atof(ubnd) <= 0) or (lbnd is not None and utils.atof(lbnd) <= 0):
            embed = discord.Embed(
                color       = 0xa33b24,
                title       = f"Price Error",
                description = 'You are not allowed to enter 0 or anything less than 0 as a price marker, please try again.'
            )
            await ctx.channel.send(embed=embed)
            return

        dbh = db.get_dbh()
        cur = dbh.cursor(buffered=True)

        sql = 'INSERT INTO watch_cog (symbol, user, lower, upper) VALUES (%s, %s, %s, %s)'
        cur.execute(sql, (symbol, ctx.author.id, lbnd, ubnd))

        embed = discord.Embed(
            color       = 0x24a36a,
            title       = "Success",
            description = f'Orders recieved, now watching **{ symbol }**'
        )

        if ubnd is not None:
            embed.add_field(name="Upper Bound", value=self.format_price(ubnd))
        if lbnd is not None:
            embed.add_field(name="Lower Bound", value=self.format_price(lbnd))
            
        await ctx.channel.send(embed=embed)
        
        dbh.commit(); cur.close()
        dbh.close()

    async def del_token(self, ctx, *args):
        dbh = db.get_dbh()
        cur = dbh.cursor(buffered=True)

        ids  = set(); err = []
        info = {}
        for arg in args: # hacky way of looking up arg[n] as ID or SYMBOL to avoid complex regex parsing
            sql  = 'SELECT * FROM watch_cog WHERE user=%s AND status=0 AND (id=%s OR symbol=%s)'
            rows = db.select(cur, sql, (ctx.author.id,arg,arg))

            if len(rows) == 0:
                err.append(arg)
                continue
            
            for row in rows:
                if row['id'] in ids:
                    continue # avoid duplicates
                ids.add(row['id'])

                if row['symbol'] not in info.keys():
                    info[row['symbol']] = []
                info[row['symbol']].append(row)
            
        if len(ids) == 0: # HELP
            embed = discord.Embed(title='Help', description='del accepts an arbitrary number of IDs and SYMBOLS: `(ID|SYMBOL)[ (ID|SYMBOL)...]`')
            
            #\u200b for "no name field"
            embed.add_field(name='Formatting', value=f"`{ CONFIG['PREFIX'] }watch del (ID|SYMBOL)[ (ID|SYMBOL)...]`", inline=False)
            embed.add_field(name='How it works', inline=False, value=(
                f"The del command accepts any `SYMBOL` or `ID` you see listed in `{ CONFIG['PREFIX'] }watch list`."
                "The system will do it's best to locate the tracked coins to delete as long as there is a "
                "match on the `SYMBOL` or `ID` passed. If an `ID` is passed, only that `ID` will be deleted, "
                "if a `SYMBOL` is passed, any match on that `SYMBOL` will be deleted."
            ))
            await ctx.channel.send(embed=embed)
            cur.close(); dbh.close()
            return

        embed = discord.Embed(
            color       = 0x24a36a,
            title       = 'Success',
            description = 'Orders recieved. Deleted the following:'
        )

        sql = 'UPDATE watch_cog SET status=1 WHERE user=%s AND status=0 AND id=%s'
        for id in ids: cur.execute(sql, (ctx.author.id,id))

        for symbol, deleted in info.items():
            v = []
            for d in deleted:
                s = f"`ID: { d['id'] }"
                if d['upper']: s += f" | Upper Bound: { self.format_price(d['upper']) }"
                if d['lower']: s += f" | Lower Bound: { self.format_price(d['lower']) }"
                s += '`'
                v.append(s)
                
            embed.add_field(name=symbol, value='\n'.join(v))
        
        await ctx.channel.send(embed=embed)

        if len(err):
            embed = discord.Embed(title=f"Error: Could not delete the following", description='\n'.join(err), color=0xa33b24)
            await ctx.channel.send(embed=embed)
            
        cur.close(); dbh.commit()
        dbh.close()

    async def list_token(self, ctx, *args):
        if len(args) != 0: # HELP
            embed = discord.Embed(title='Help', description='Info does not accept any arguments.')
            
            #\u200b for "no name field"
            embed.add_field(name='Formatting', value=f"`{ CONFIG['PREFIX'] }watch list`", inline=False)
            embed.add_field(name='How it works', inline=False, value=(
                "The list command does not accept any arguments. When called, it will simply return "
                "any coins you are currently tracking, what the bounds you set were, and the current "
                "price of the coin."
            ))
            await ctx.channel.send(embed=embed)
            return

        
        dbh = db.get_dbh()
        cur = dbh.cursor(buffered=True)

        sql  = 'SELECT * FROM watch_cog WHERE user=%s AND status=0'
        ret  = db.select(cur, sql, (ctx.author.id,))

        symbols = set() # Get unique set of SYMBOLS to poll from CMC
        [symbols.add(r['symbol']) for r in ret]

        if not len(symbols):
            embed = discord.Embed(
                color       = 0x24a36a,
                title       = 'Success',
                description = 'Orders recieved, but you are not currently tracking anything.'
            )
            await ctx.channel.send(embed=embed)
            return
        
        prices = self.fetch_data(symbols)
        if prices['stat'] != 0:
            embed = discord.Embed(title=f"Error: { prices['stat'] }", description=prices['msg'], color=0xa33b24)
            await ctx.channel.send(embed=embed)
            return

        data = {}
        for i, r in enumerate(ret):
            if r['symbol'] not in data.keys():
                data[r['symbol']] = []
            data[r['symbol']].append(r)

        embed = discord.Embed(
            color       = 0x24a36a,
            title       = 'Success',
            description = 'Orders recieved. You are tracking the following:'
        )

        for symbol, info in data.items():
            v = []
            for i in info:
                s = f"`ID: { i['id'] }"
                if i['upper']: s += f" | Upper Bound: { self.format_price(i['upper']) }"
                if i['lower']: s += f" | Lower Bound: { self.format_price(i['lower']) }"
                s += '`'
                v.append(s)
                
            embed.add_field(name=f"\n{ symbol }  --  { self.format_price(prices['data'][symbol]) }", value='\n'.join(v), inline=False)

        await ctx.channel.send(embed=embed)
        cur.close(); dbh.close()

    async def token_info(self, ctx, *args):
        return
   
    @tasks.loop(minutes=10.0)
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
            embed = discord.Embed(title=f"Error: { prices['stat'] }", description=f"While checking targets, I ran into an issue.\n\n{ prices['msg'] }", color=0xa33b24)
            await channel.send(embed=embed)
            return

        user_map = {}
        for r in ret:
            user   = r['user']  # readability
            symbol = r['symbol']

            if symbol in prices['data'].keys(): # more readable price lookup
                bound = None; above = False

                if   r['upper'] and prices['data'][symbol] >= r['upper']:
                    bound = r['upper']
                    above = True
                elif r['lower'] and prices['data'][symbol] <= r['lower']:
                    bound = r['lower']

                # Nothing to do, go to next
                if bound is None: continue

                if user   not in user_map.keys():       user_map[user]         = {}
                if symbol not in user_map[user].keys(): user_map[user][symbol] = []

                user_map[user][symbol].append(f'Now **{ "over" if above else "under" }** { self.format_price(utils.atos(bound)) }')

                sql = 'UPDATE watch_cog SET status=1 WHERE id=%s'
                cur.execute(sql, (r['id'],))

        for user, data in user_map.items():
            embed = discord.Embed(
                color       = 0x24a36a,
                title       = 'Gonk Ticker',
                description = f'<@{ user }> I have an update for you!',
            )

            for symbol, msgs in data.items():
                for msg in msgs:
                    embed.add_field(name=f"{ symbol }  --  { self.format_price(prices['data'][symbol]) }", value=msg, inline=False)

            await channel.send(embed=embed)

        dbh.commit(); cur.close()
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
                ret['msg'] = f"I've encountered an HTTP error, please try again.\n<@{ CONFIG['ADMIN_NOTIFY'] }> I'm having issues..."
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

    def format_price(self, price):
        price = utils.atof(price)
        if price.is_integer():
            return f'${price:,.0f}'
        if price > 10:
            return f'${price:,.2f}'
        if price > 0.05:
            return f'${price:.3f}'
        if price > 0.005:
            return f'${price:.4f}'
        if price > 0.0005:
            return f'${price:.5f}'
        if price > 0.00005:
            return f'${price:.6f}'
        if price > 0.000005:
            return f'${price:.7f}'
        if price > 0.0000005:
            return f'${price:.8f}'
        if price > 0.00000005:
            return f'${price:.9f}'
        return f'${price:.12f}'
    
def setup(bot: commands.Bot):
    bot.add_cog(WatchCog(bot))
