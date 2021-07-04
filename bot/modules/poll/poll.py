import discord

# TODO
# error handling
# multiply duration by some factor for use with ctx.send.delete_after


class Poll:
    def __init__(self, msg: discord.Message):
        self.title = self.get_title(msg)
        self.duration = self.get_duration(msg) * 60
        self.reacts = self.get_reacts(msg)
        self.embed = self.create_embed(msg)
        self.voters = {}

    def get_title(self, msg: discord.Message) -> str:
        return msg.content.split()[1]

    def get_duration(self, msg: discord.Message) -> int:
        return int(msg.content.split()[2])

    def get_reacts(self, msg: discord.Message) -> dict:
        options = msg.content.split()[3:]
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣",
                  "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]

        # zip() stops after the end of the shorter list,
        # so if there are more options than emojis only 9 options will be saved,
        # and if there are more emojis than options only [option] number of emojis will be saved
        # NOTE: this will also automatically ignore repeated keys (options)
        reacts = dict(zip(options, emojis))
        return reacts

    def create_embed(self, msg: discord.Message):
        embed = discord.Embed(title=self.title)
        embed.set_author(
            name=msg.author.display_name, icon_url=msg.author.avatar_url
        )
        for key, val in self.reacts.items():
            embed.add_field(name=key, value=val, inline=True)
        return embed

    async def vote(self, member: discord.Member, emoji: discord.PartialEmoji, msg: discord.Message):
        if emoji not in self.reacts.values():
            # do not allow users to add additional reactions
            await msg.remove_reaction(emoji, member)
            print("Member attempted to add option, removed")
            return

        if member in self.voters.keys():
            # do not allow users to react more than once
            await msg.remove_reaction(emoji, member)
            print("Member attempted to vote more than once, removed")
            return

        self.voters[member] = emoji
        print("Member Voted")

    def unvote(self, member: discord.Member):
        self.voters.pop(member, None)
