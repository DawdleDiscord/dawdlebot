import discord
from discord.ext import commands
import datetime
from .db_checks import is_mod
from .db_converters import SmartMember

class verification(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	# 	with open('src/data/verification.json', 'r') as json_file:
	# 		self.verif_dict = json.load(json_file)

	# @commands.group()
	# async def verify(self, ctx):
	# 	if ctx.invoked_subcommand is None:
	# 		await ctx.send('Invalid verify command')

	# @verify.command()
	# async def emojilist(self, ctx):
	# 	listemoj =[]
	# 	if ctx.guild:
	# 		dawdle = ctx.guild:
	# 		for emoj in self.verif_dict.keys():
	# 			reactemoj = dawdle.fetch_emoji
	# 	embedList = discord.Embed(title = 'Emoji List')

	@commands.Cog.listener()
	async def on_message(self, message):
		if not message.guild:
			for guild in self.bot.guilds:
				if guild.name == 'dawdle':
					dawdle = guild
					break

			mem = dawdle.get_member(message.author.id)
			if mem:
				unverifiedrole = dawdle.get_role(479410607821684757)

				if unverifiedrole in mem.roles:
					verifchannel = dawdle.get_channel(623016717429374986)
					staffrole = dawdle.get_role(519616340940554270)
					if message.content:
						embedMess = discord.Embed(title='Message',description=f'{message.content}', color=0xffb6c1,timestamp = datetime.datetime.utcnow())
						embedMess.set_author(name=f'{message.author}',icon_url = message.author.avatar_url)
						embedMess.set_footer(text=f"ID: {message.author.id}")
						await verifchannel.send(embed=embedMess)

					for a in message.attachments:
						embedVer = discord.Embed(title='Verification', color=0xffb6c1,timestamp = datetime.datetime.utcnow())
						embedVer.set_author(name=f'{message.author}',icon_url = message.author.avatar_url)
						embedVer.set_image(url=a.url)
						embedVer.add_field(name="Link",value=f"[Image]({a.url})")
						embedVer.set_footer(text=f"ID: {message.author.id}")
						verifImage = await verifchannel.send(embed=embedVer)

					if message.attachments:
						sentMess = await verifchannel.send(f'{staffrole.mention}, verify {message.author.mention}?')
						await sentMess.add_reaction('<:pinkcheck:609771973341610033>')
						await sentMess.add_reaction('<:pinkx:609771973102534687>')
						await sentMess.add_reaction('<a:twinklethemoreyouknow:630533105903730689>')
						await sentMess.add_reaction('<a:star2:586767353740656656>')
						await sentMess.add_reaction('<a:pink_flowers:598695827891945472>')
						await message.author.send('Your message has been successfully submitted. Please wait patiently for a staff member to review your pictures.')

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):

		if payload.channel_id == 623016717429374986:
			dawdle = self.bot.get_guild(payload.guild_id)
			verifchannel = dawdle.get_channel(623016717429374986)
			message = await verifchannel.fetch_message(payload.message_id)

			if message.mentions and "verify" in message.content:

				for react in message.reactions:

					if react.count == 2:
						user = message.mentions[0]

						if str(react.emoji) == '<:pinkcheck:609771973341610033>':

							verifiedrole = dawdle.get_role(481148097960083471)
							unverifiedrole = dawdle.get_role(479410607821684757)
							dotrole = dawdle.get_role(587397534469718022)
							await user.add_roles(verifiedrole, dotrole)
							await user.remove_roles(unverifiedrole)
							await user.send("Thank you for verifying! You’ve successfully completed this process, you are now able to see the majority of the server. Please proceed to get some <#694994576791961630> and to post an <#514555898648330260>! No formats are necessary for introductions, just a little snippet will do. When you are done with both, type `~done` (without the quotes) in <#514560994337620008>.")

						if str(react.emoji) == '<:pinkx:609771973102534687>':
							await user.send("Sorry, but the pictures you provided do not follow our outlines as described in <#479407137060028449>. Please review and try again!")

						if str(react.emoji) == '<a:twinklethemoreyouknow:630533105903730689>':
							await user.send("You’re missing today’s date on the selfie picture!")

						if str(react.emoji) == '<a:star2:586767353740656656>':
							await user.send("You're missing the server name on the selfie picture!")

						if str(react.emoji) == '<a:pink_flowers:598695827891945472>':
							await user.send("You're missing your discord name on the selfie picture!")

	@commands.command()
	async def done(self, ctx):

		if ctx.guild.id == 475584392740339712:

			dawdle = ctx.guild
			dotrole = dawdle.get_role(587397534469718022)

			if dotrole in ctx.author.roles:

				hasIntro = False
				introchannel = dawdle.get_channel(514555898648330260)

				async for mess in introchannel.history(limit=None):
					if ctx.author == mess.author:
						hasIntro = True
						break

				age_roles = [481138497856602113, 480080787253755905, 481138992151003156, 481138740484505611]
				pronoun_roles = [551901787297284096, 551901739700322324, 551901812677017611]
				dm_roles = [479410113115979805, 479410060804751371, 479410091905253376]
				loc_roles = [481135072427376641, 481135146129424415, 481135185497423900, 481135221572501516, 481135414321610763, 481135465399844882, 481136198014861336]
				check_age, check_pronoun, check_dm, check_loc, has_dot = (False,)*5

				for role in ctx.author.roles:
					if role.id in age_roles: check_age = True
					if role.id in pronoun_roles: check_pronoun = True
					if role.id in dm_roles: check_dm = True
					if role.id in loc_roles: check_loc = True

				role_check = check_age and check_pronoun and check_dm and check_loc

				if hasIntro and role_check:
					await ctx.author.remove_roles(dotrole)
					await ctx.send(f'Well done {ctx.message.author.mention}! You’ve completed everything that needs to be done, enjoy your stay!')

				elif hasIntro and not role_check:
					await ctx.send(f'Sorry {ctx.message.author.mention}, but you seem to be missing some <#694994576791961630>. Try again!')
				elif not hasIntro and role_check:
					await ctx.send(f'Sorry {ctx.message.author.mention}, but it seems you haven\'t posted an <#514555898648330260>. Please post one and try again!')

				else:
					await ctx.send(f'Sorry {ctx.message.author.mention}, but you seem to be missing some <#694994576791961630> and an <#514555898648330260>. Try again!')
	@commands.command(aliases=['mb','msgback','msg','message'])
	async def msg_back(self, ctx, member : SmartMember,*, message : str):
		if ctx.guild:
			dawdle = ctx.guild
			verifchannel = dawdle.get_channel(623016717429374986)
			if ctx.message.channel == verifchannel:
				await member.send(message)
				await ctx.send(f'Message sent to {member}.')
	@msg_back.error
	async def msg_back_error(self, ctx,error):
		if isinstance(error,discord.Forbidden) or isinstance(error,discord.HTTPException):
			await ctx.send('I was unable to send the message.')
		elif isinstance(error,commands.errors.BadArgument):
			await ctx.send('I could not find that member or too many members with that name.')
		else:
			await ctx.send(f'I had an unknown error {str(error)}')
