import discord, re


def get_tokens(msg: str):
    # .add [Member1, Member2, ...] [Roles1, Role2, ...]
    tokens = {
        "members": [],
        "roles": [],
    }

    match = re.match(r".*add \[(.*)\] \[(.*)\]", msg, re.I)
    if match is None:
        return tokens

    tokens["members"] = [x.strip() for x in match.group(1).split(",")]
    tokens["roles"] = [x.strip() for x in match.group(2).split(",")]

    print(f'Members: { tokens["members"] }')
    print(f'Roles:   { tokens["roles"]   }')

    return tokens


async def update_roles(ctx, tokens, flag):
    for member in tokens["members"]:
        m = discord.utils.find(lambda m: m.name == member, ctx.guild.members)
        if m is not None:
            for role in tokens["roles"]:
                r = discord.utils.find(lambda r: r.name == role, ctx.guild.roles)
                if r is not None:
                    if flag == "a":
                        await m.add_roles(r)
                    else:
                        await m.remove_roles(r)
