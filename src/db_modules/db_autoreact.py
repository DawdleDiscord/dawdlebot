import discord
from discord.ext import commands
from .db_checks import is_mod
import json

class db_autoreact(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		with open('src/data/autoreacts.json', 'r') as json_file:
			self.reacts_dict = json.load(json_file)

		del json_file

	@commands.group()
	@is_mod()
	async def autoreact(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.send('Invalid clean command')

	@autoreact.command()
	async def add(self, ctx, channel : discord.TextChannel, *emoji : str):

		if emoji:
			self.reacts_dict[str(channel.id)] = emoji


			with open('src/data/autoreacts.json', 'w') as json_file:
				json.dump(self.reacts_dict, json_file)
			del json_file

			await ctx.send(f"{channel.mention} was added.")

		else:
			await ctx.send('Please include emojis')

	@autoreact.command()
	async def remove(self, ctx, channel : discord.TextChannel):

		if self.reacts_dict.keys():
			channel_found = False
			for ch in self.reacts_dict.keys():
				if channel.id == int(ch):
					channel_found = True
					del self.reacts_dict[ch]
					await ctx.send(f"{channel.mention} has been removed.")
					break
			if channel_found:
				with open('src/data/autoreacts.json', 'w') as json_file:
					json.dump(self.reacts_dict, json_file)
				del json_file
			else:
				await ctx.send(f"{channel.mention} is not currently added.")

	@autoreact.command()
	async def list(self, ctx):

		dawdle = ctx.guild
		channellist = []
		dellist = []
		if self.reacts_dict.keys():
			for ch_id in self.reacts_dict.keys():
				channel = dawdle.get_channel(int(ch_id))
				if channel:
					channel_str = f"{channel.mention}: "
					for emoji in self.reacts_dict[ch_id]:
						channel_str = channel_str+f"{emoji} "
					channellist.append(channel_str)
				else:
					dellist.append(ch_id)
			if dellist:
				for ch in dellist:
					del self.reacts_dict[ch]

			channellist_str = "\n".join(channellist)

			listEmbed = discord.Embed(title="Channel Autoreacts", description = channellist_str, color = 0xffb6c1)
			await ctx.send(embed=listEmbed)
		else:
			await ctx.send("No current autoreacts")


	@commands.Cog.listener()
	async def on_message(self, message):
		if message.guild and message.guild.id == 475584392740339712:
			dawdle = message.guild
			if str(message.channel.id) in self.reacts_dict.keys():
				for emoji in self.reacts_dict[str(message.channel.id)]:
					await message.add_reaction(emoji)
