from typing import Dict
import discord

# TODO
# add error handling for getters


class Poll:
    def __init__(self, msg: discord.Message):
        self.msg = msg.removeprefix(".poll")
        self.title = self.get_title()
        self.duration = self.get_duration()
        self.options = self.get_options()
        self.reacts = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
        self.embed = self.create_embed()
        self.voters: Dict[discord.Member, discord.Reaction] = {}

    def get_title(self) -> str:
        return self.msg.content.split(",")[1].strip()

    def get_duration(self) -> int:
        return self.msg.content.split(",")[2].strip()

    def get_options(self):
        return self.msg.content.split(",")[3].split(",")

    def create_embed(self):
        embed = self.embed(title=self.title)
        embed.set_author(
            name=self.msg.author.display_name, icon_url=self.msg.author.avatar_url
        )
        for i in range(len(self.options)):
            embed.add_field(name=self.emojis[i], value=self.emojis[i], inline=True)
        return embed

    async def vote(self, reaction: discord.Reaction, member: discord.Member):
        if member not in self.voters:
            self.voters[member] = reaction
        else:
            await reaction.remove(member)

    async def unvote(self, reaction: discord.Reaction, member: discord.Member):
        if member in self.voters:
            self.voters.pop(member)
