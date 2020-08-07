import discord
from discord.ext import commands
from .db_checks import is_mod
from .db_converters import SmartMember
import datetime
import typing

class db_moderation(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
	@commands.command()
	@is_mod()
	async def ban(self, ctx, user : typing.Union[SmartMember, int], *, reason : typing.Optional[str]):

		dawdle = ctx.guild
		if isinstance(user,discord.Member):
			member = user
		else:
			member = await self.bot.fetch_user(user)
		admonitions = dawdle.get_channel(527899554184691715)
		banEmbed = discord.Embed(title=f'{member} has been banned', color=0xffb6c1)
		await ctx.send(embed=banEmbed)
		if reason:
			await admonitions.send(f"```{member} was banned by {ctx.author.name} (Rule {reason})```")
			try:
				await member.send('You have been banned from Dawdle.')
			except:
				pass
		await dawdle.ban(user=member)

	@commands.command()
	@is_mod()
	async def unban(self, ctx, userID : int):
		dawdle = ctx.guild
		user = await self.bot.fetch_user(userID)
		await dawdle.unban(user=user)
		unbanEmbed = discord.Embed(title=f'{user} has been unbanned', color=0xffb6c1)
		banmess = await ctx.send(embed = unbanEmbed)



	@commands.command()
	@is_mod()
	async def kick(self, ctx, member : SmartMember):
		dawdle = ctx.guild
		kickEmbed = discord.Embed(title=f'{member} has been kicked', color=0xffb6c1)
		await dawdle.kick(user= member)
		await ctx.send(embed=kickEmbed)

	@commands.command(aliases=['postadmon'])
	@is_mod()
	async def postadmonition(self, ctx, *, post : str):
		dawdle = ctx.guild
		admonitions = dawdle.get_channel(527899554184691715)
		await admonitions.send(f'```{post}```')
		admonEmbed = discord.Embed(title='',description='Admonition posted', color=0xffb6c1)
		await ctx.send(embed=admonEmbed)

	@commands.command()
	@is_mod()
	async def prune(self, ctx, num : int,*, user : typing.Optional[typing.Union[SmartMember, int]]):
		toprune = num + 1
		if num < 100:
			if not user:
				await ctx.channel.purge(limit=toprune)
				pruneEmbed = discord.Embed(title=f'Pruned {num} messages.', color=0xffb6c1)

			else:
				if isinstance(user, int):
					user_id = user
					user = await self.bot.fetch_user(user_id)

				def is_user(m):
					return m.author == user
				await ctx.channel.purge(limit = toprune, check = is_user)
				pruneEmbed = discord.Embed(title=f'Pruned all messages by {user} in last {num} messages.', color=0xffb6c1)

			pruneMess = await ctx.send(embed=pruneEmbed)
			await pruneMess.delete(delay = 2.5)

	@commands.group()
	@is_mod()
	async def lockdown(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.send('Invalid lockdown command')

	@lockdown.command()
	async def lock(self, ctx):
		if ctx.guild:
			dawdle = ctx.guild
			parlor = dawdle.get_channel(514550733732053012)
			foyer = dawdle.get_channel(514554494495752204)
			unverifiedrole = dawdle.get_role(479410607821684757)
			await parlor.set_permissions(target=unverifiedrole,read_messages = False, send_messages =  False)
			await ctx.send('Parlor has been locked from unverified members. Use \`/lockdown unlock\` to undo this.')
			await foyer.send('The main chat has been locked from unverified members due to a raid. Please be patient for staff to handle the issue.')

	@lockdown.command()
	async def unlock(self, ctx):
		if ctx.guild:
			dawdle = ctx.guild
			parlor = dawdle.get_channel(514550733732053012)
			foyer = dawdle.get_channel(514554494495752204)
			unverifiedrole = dawdle.get_role(479410607821684757)
			await parlor.set_permissions(target=unverifiedrole,read_messages = True, send_messages =  True)
			await ctx.send('Parlor has been unlocked for unverified members. Use \`/lockdown lock\` to undo this.')
			await foyer.send('The main chat has been unlocked for unverified members.')

	@commands.command()
	async def report(self, ctx, *, report_text : str):
		dawdle = self.bot.get_guild(475584392740339712)
		verifChannel = dawdle.get_channel(623016717429374986)
		staffrole = dawdle.get_role(519616340940554270)
		if not ctx.message.guild:
			embedReport = discord.Embed(title='Report',description = "", color=0xffb6c1,timestamp = datetime.datetime.utcnow())
			embedReport.add_field(name="Reporter",value=ctx.message.author.mention,inline=False)
			embedReport.add_field(name="Content",value=report_text,inline=False)
			embedReport.set_footer(text=ctx.message.author.id)
			repMess = await verifChannel.send(content=f'{staffrole.mention} Report',embed=embedReport, )
			for a in ctx.message.attachments:
				embedReport = discord.Embed(title='Report',description = "", color=0xffb6c1,timestamp = datetime.datetime.utcnow())
				embedReport.add_field(name="Reporter",value=ctx.message.author.mention,inline=False)
				embedReport.set_image(url=a.url)
				embedReport.set_footer(text=ctx.message.author.id)
				await verifChannel.send(content=f'{staffrole.mention} Report',embed=embedReport)
			try:
				await ctx.message.author.send('Your report has been sent to staff.')
			except:
				pass

	@report.error
	async def report_error(self, ctx,error):
		if isinstance(error,commands.errors.MissingRequiredArgument):
			await ctx.send('It looks like you are sending a report. You need text after the `/report`.')


	async def cog_command_error(self, ctx, error):
		if isinstance(error,commands.errors.BadArgument):
			await ctx.send('I could not find this member or user.')
		elif isinstance(error,commands.errors.CheckFailure):
			await ctx.send('you do not have permissions to do this')
		elif isinstance(error, commands.BadUnionArgument):
			await ctx.send('I could not find this member. If they are not in the server currently then use their ID.')
		else:
			await ctx.send(f'Error: {str(error)}')
