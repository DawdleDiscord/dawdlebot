import discord
from discord.ext import commands
def is_mod():
	async def is_mod_predicate(ctx):
		adminroles = [490249474619211838, 514556928655884298, 623220291882975292]
		modroles = [490249474619211838, 514556928655884298, 623220291882975292, 519632663246536736]
		dawdle = ctx.guild
		is_mod = False
		for role in ctx.author.roles:
			if role.id in modroles:
				is_mod = True
				break
		return is_mod
	return commands.check(is_mod_predicate)

def is_member():
	async def is_member_predicate(ctx):
		dawdle = ctx.bot.get_guild(475584392740339712)
		if dawdle.get_member(ctx.author.id):
			return True
		else:
			return False
	return commands.check(is_member_predicate)

def in_dawdle():
	async def in_dawdle_predicate(ctx):
		return ctx.guild and ctx.guild.id == 475584392740339712

	return commands.check(in_dawdle_predicate)
