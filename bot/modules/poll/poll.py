import discord

# TODO
# error handling


class Poll:
    def __init__(self, msg: discord.Message):
        self.title = self.get_title(msg)
        self.duration = self.get_duration(msg)
        self.options = self.get_options(msg)
        self.reacts = ["1️⃣", "2️⃣", "3️⃣", "4️⃣",
                       "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
        self.embed = self.create_embed()
        self.voters = {}

    def get_title(self, msg: discord.Message) -> str:
        return msg.content.split()[1]

    def get_duration(self, msg: discord.Message) -> float:
        return msg.content.split()[2]

    def get_options(self, msg: discord.Message):
        return msg.content.split()[3:]

    def create_embed(self):
        embed = self.embed(title=self.title)
        embed.set_author(
            name=self.msg.author.display_name, icon_url=self.msg.author.avatar_url
        )
        for i in range(len(self.options)):
            embed.add_field(name=self.reacts[i],
                            value=self.options[i], inline=True)
        return embed

    async def vote(self, msg: discord.Message, member: discord.Member, emoji: discord.partial_emoji):
        if member not in self.voters.keys:
            self.voters[member] = emoji
        else:
            await msg.remove_reaction(emoji, member)
