import discord


def get_tokens(msg: str):
    """Tokenize command string like so: { (action: action), (member: member), (roles: [role1, role2, ...]) }"""

    args = msg.split()
    tokens = {
        "member": args[1].strip(),
        "roles": args[2:],
    }
    return tokens


async def update_roles(ctx, tokens, action: str):
    m = discord.utils.find(lambda m: m.name == tokens["member"], ctx.guild.members)
    if m is not None:
        for role in tokens["roles"]:
            r = discord.utils.find(lambda r: r.name == role, ctx.guild.roles)
            if r is not None:
                if action == "add":
                    await m.add_roles(r)
                else:
                    await m.remove_roles(r)
