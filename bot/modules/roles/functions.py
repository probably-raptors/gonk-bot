import discord


def get_tokens(msg: str):
    """Tokenize command string"""
    args = msg.split()
    tokens = {
        "member": args[1].strip(),
        "roles": args[2:],
    }
    return tokens


async def update_roles(ctx, tokens, action: str):
    member = discord.utils.find(
        lambda m: m.name == tokens["member"], ctx.guild.members)

    if member is not ctx.author and not member.guild_permissions.administrator:
        await ctx.send("You do not have permission to manage other users!")
        return

    if member is not None:
        for role in tokens["roles"]:
            r = discord.utils.find(lambda r: r.name == role, ctx.guild.roles)
            if r is not None:
                if action == "add":
                    await member.add_roles(r)
                else:
                    await member.remove_roles(r)
