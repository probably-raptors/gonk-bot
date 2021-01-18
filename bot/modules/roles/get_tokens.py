from discord.ext import commands
import discord


def get_tokens(self, ctx: commands.Context, msg: str):

	members = msg.partition("] [")[0].strip()
	members.split()[3:]

	roles = msg.partition("] [")[2]
	roles.split()[:-2]

	tokens = {"members": members, "roles": roles}
	return tokens