import discord
import json,typing
from .db_checks import is_mod
from discord.ext import commands


class db_fuzzies(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		with open('src/data/fuzzies.json', 'r') as json_f_r:
			self.fuzz_dict = json.load(json_f_r)


	@commands.command()
	async def fuzzie(self, ctx, *, msg : str):

		for guild in self.bot.guilds:
			if guild.name == 'dawdle':
				dawdle = guild
				break
		dbchannel = dawdle.get_channel(623016717429374986)
		fuzEmbed = discord.Embed(title = 'Fuzzie', description = msg,color=0xffb6c1)
		fuzEmbed.set_footer(text=ctx.author.id)
		fuzAprv = await dbchannel.send(embed=fuzEmbed)
		await fuzAprv.add_reaction('<:pinkcheck:609771973341610033>')
		await fuzAprv.add_reaction('<:pinkx:609771973102534687>')
		await ctx.send('Your fuzzie has been sent to staff for approval.')

	@commands.command()
	@is_mod()
	async def fuzziechannel(self, ctx, channel : discord.TextChannel):
		self.fuzz_dict['channel'] = channel.id
		with open('src/data/fuzzies.json', 'w') as file:
			json.dump(self.fuzz_dict, file)
		await ctx.send(f"Fuzzies channel was set to {channel.mention}!")




	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		for guild in self.bot.guilds:
			if guild.name == 'dawdle':
				dawdle = guild
				break
		fchannel_id = self.fuzz_dict['channel']
		if payload.guild_id == 475584392740339712 and payload.channel_id == 623016717429374986:
			dbchannel = dawdle.get_channel(623016717429374986)
			fmess = await dbchannel.fetch_message(payload.message_id)
			reactemoj = payload.emoji
			if fmess.embeds and fmess.embeds[0].title == 'Fuzzie':
				for react in fmess.reactions:
					if react.emoji == reactemoj and react.count == 2:
						if reactemoj.id == 609771973341610033:
							fchannel = dawdle.get_channel(fchannel_id)
							fuzzie = fmess.embeds[0].description
							fEmbed = discord.Embed(title = '', description=fuzzie,color=0xffb6c1)
							finalfMess = await fchannel.send(embed=fEmbed)
							await finalfMess.add_reaction('❤')
							await fmess.delete(delay=2.0)

						elif reactemoj.id == 609771973102534687:
							fuzzMem = await dawdle.fetch_member(fmess.embeds[0].footer.text)
							await fuzzMem.send('Your fuzzie has been denied because it did not follow the rules. Please review them before trying again.')
