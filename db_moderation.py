import discord
from discord.ext import commands
from db_checks import is_mod
import typing

class moderation(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
	@commands.command()
	@is_mod()
	async def ban(self, ctx, user : typing.Union[discord.User, int], *, reason : typing.Optional[str]):

		dawdle = ctx.guild
		if isinstance(user,discord.User):
			member = user
		else:
			member = await self.bot.fetch_user(user)
		await dawdle.ban(user=member)
		admonitions = dawdle.get_channel(527899554184691715)
		banEmbed = discord.Embed(title=f'{member} has been banned', color=0xffb6c1)
		await ctx.send(embed=banEmbed)
		if reason:
			await admonitions.send(f"```{member} was banned by {ctx.author.name} (Rule {reason})```")
			try:
				await member.send('You have been banned from Dawdle.')
			except:
				pass

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
	async def kick(self, ctx, member : discord.Member):
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
	async def prune(self, ctx, num : int,*, user : typing.Optional[discord.User]):
		toprune = num + 1
		if num < 100:
			if not user:
				await ctx.channel.purge(limit=toprune)
				pruneEmbed = discord.Embed(title=f'Pruned {num} messages.', color=0xffb6c1)

			else:
				def is_user(m):
					return m.author == user
				await ctx.channel.purge(limit = toprune, check = is_user)
				pruneEmbed = discord.Embed(title=f'Pruned all messages by {user} in last {num} messages.', color=0xffb6c1)

			pruneMess = await ctx.send(embed=pruneEmbed)
			await pruneMess.delete(delay = 2.5)


	async def cog_command_error(self, ctx,error):
		if isinstance(error,commands.errors.BadArgument):
			await ctx.send('I could not find this member or user.')
		elif isinstance(error,commands.errors.CheckFailure):
			await ctx.send('you do not have permissions to do this')
