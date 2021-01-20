import discord


def get_tokens(msg: str):
    # .add [Member1, Member2, ...] [Roles1, Role2, ...]

    members = ""
    roles = ""
    state = 0
    for c in msg:
        if state == 0:
            # Skip command chars until first [
            if c == "[":
                state = 1
            continue

        if state == 1:
            # we are gathering members
            if c != "]":
                members += c
            else:
                state = 2
            continue

        if state == 2:
            # we finished members, waiting for roles
            if c == "[":
                state = 3
            continue

        if state == 3:
            # we found our roles!
            if c != "]":
                roles += c
            else:
                break

    tokens = {
        "members": [x.strip() for x in members.split(",")],
        "roles": [x.strip() for x in roles.split(",")],
    }
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