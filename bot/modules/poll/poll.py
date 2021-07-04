import discord

# TODO
# error handling
# multiply duration by some factor for use with ctx.send.delete_after


class Poll:
    def __init__(self, msg: discord.Message):
        self.title = self.get_title(msg)
        self.duration = self.get_duration(msg)
        self.options = self.get_options(msg)
        self.reacts = self.get_reacts(len(self.options))
        self.embed = self.create_embed(msg)
        self.voters = {}

    def get_title(self, msg: discord.Message) -> str:
        return msg.content.split()[1]

    def get_duration(self, msg: discord.Message) -> float:
        return msg.content.split()[2]

    def get_options(self, msg: discord.Message):
        return msg.content.split()[3:]

    def get_reacts(self, numOpts):
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣",
                  "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
        reacts = emojis[:numOpts]
        return reacts

    def create_embed(self, msg: discord.Message):
        embed = discord.Embed(title=self.title)
        embed.set_author(
            name=msg.author.display_name, icon_url=msg.author.avatar_url
        )
        for i, r in enumerate(self.reacts):
            embed.add_field(name=self.options[i], value=r, inline=True)
        return embed

    async def vote(self, msg: discord.Message, member: discord.Member, emoji: discord.partial_emoji):
        if member not in self.voters.keys:
            self.voters[member] = emoji
        else:
            await msg.remove_reaction(emoji, member)

    def unvote(self, payload: discord.RawReactionActionEvent):
        self.voters.pop(payload.member)
