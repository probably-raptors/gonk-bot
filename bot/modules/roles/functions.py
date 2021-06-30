import discord, re


def get_tokens(msg: str):
    """Tokenize command string like so: { member, [role1, role2, ...] }"""

    args = str.split(" ")
    member = args[1].strip()
    roles = args[2:]

    tokens = {
        "member": member,
        "roles": [x.strip() for x in roles.split(",")],
    }

    return tokens


async def update_roles(ctx, tokens, action):
    m = discord.utils.find(lambda m: m.name == tokens["member"], ctx.guild.members)
    if m is not None:
        for role in tokens["roles"]:
            r = discord.utils.find(lambda r: r.name == role, ctx.guild.roles)
            if r is not None:
                if action == "add":
                    await m.add_roles(r)
                else:
                    await m.remove_roles(r)
