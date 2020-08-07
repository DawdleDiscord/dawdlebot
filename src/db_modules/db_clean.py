import discord
import json,typing
from .db_checks import is_mod
from discord.ext import commands

class db_clean(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		with open('src/data/cleanbotlist.json', 'r') as json_file:
			self.bot_dict = json.load(json_file)
		del json_file
		with open('src/data/cleanchannellist.json', 'r') as json_file:
			self.channellist = json.load(json_file)
		del json_file
		self.botprefixes = self.bot_dict.values()

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.guild and message.channel.id in self.channellist:
			is_command = False
			for pref in self.botprefixes:
				if message.content.startswith(pref) and message.content[1] != '~':
					is_command = True
					break
			if message.author.bot or is_command:
				await message.delete()

	@commands.group()
	@is_mod()
	async def clean(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.send('Invalid clean command')

	@clean.command()
	async def botadd(self, ctx, botname : str, prefix : str):
		self.bot_dict[botname] = prefix
		with open('src/data/cleanbotlist.json', 'w') as json_file:
			json.dump(self.bot_dict, json_file)
		del json_file
		await ctx.send('Bot added')

	@clean.command()
	async def botremove(self, ctx, botname : str):
		del self.bot_dict[botname]

		with open('src/data/cleanbotlist.json', 'w') as json_file:
			json.dump(self.bot_dict, json_file)
		del json_file
		await ctx.send('Bot removed')

	@botremove.error
	async def botremove_error(self, ctx, error):
		if isinstance(error, KeyError):
			await ctx.send('I could not find that bot')

	@clean.command()
	async def botlist(self, ctx):
		stringlist = []
		for bot in self.bot_dict.keys():
			botstring = f"❥ {bot}"
			botstring = botstring.ljust(24)
			botstring = botstring+f" {self.bot_dict[bot]}"
			stringlist.append(botstring)

		botlist = "**Botlist** ```"+'\n'.join(stringlist)+"```"
		listEmbed = discord.Embed(title = '', description=botlist, color=0xffb6c1)
		await ctx.send(embed=listEmbed)

	@clean.command()
	async def channeladd(self, ctx, channel : discord.TextChannel):
		self.channellist.append(channel.id)
		with open('src/data/cleanchannellist.json', 'w') as json_file:
			json.dump(self.channellist, json_file)
		del json_file
		await ctx.send(f'Added {channel.mention}')

	@clean.command()
	async def channelremove(self, ctx, channel : discord.TextChannel):
		self.channellist.remove(channel.id)
		with open('src/data/cleanchannellist.json', 'w') as json_file:
			json.dump(self.channellist, json_file)
		del json_file
		await ctx.send(f'Removed {channel.mention}')

	@clean.command()
	async def channellist(self, ctx):
		channellist_str = []
		for ch_id in self.channellist:
			channel = ctx.guild.get_channel(ch_id)
			if channel is None:
				self.channellist.remove(ch_id)
				with open('src/data/cleanchannellist.json', 'w') as json_file:
					json.dump(self.channellist, json_file)
			else:
				channel_str = f"❥ {channel.mention}"
				channellist_str.append(channel_str)
		channellist_all = "**Channels**\n"+'\n'.join(channellist_str)
		channelEmbed = discord.Embed(title = '', description = channellist_all, color=0xffb6c1)
		await ctx.send(embed=channelEmbed)
