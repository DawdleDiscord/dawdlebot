import discord
from discord.ext import commands
from .db_converters import SmartMember,SmartRole
from .db_checks import is_mod,in_dawdle
import json,typing
import datetime
import asyncio
import random

class db_games(commands.Cog):

	def __init__(self, bot):
		self.bot = bot


	
	@commands.command()
	@in_dawdle
	async def duel(self, ctx, member : SmartMember):
		player1 = ctx.author
		player2 = member
		#duelScenario = 
		startDuel = False
		duelEmbed = discord.Embed(title = "Duel", description = f"{player1} has challenged {player2} to a duel! If you accept, one of you will win the other's entire korb balance!\n\n{player2}, react with a <:pinkcheck:609771973341610033> to accept or a <:pinkx:609771973102534687> to decline.", color = 0xffb6c1)
		challenge_mess = await ctx.send(content=f"{player1.mention} {player2.mention}" , embed=duelEmbed)
		await challenge_mess.add_reaction("<:pinkcheck:609771973341610033>")
		await challenge_mess.add_reaction("<:pinkx:609771973102534687>")
		def check_chall(reaction, user):
			return user == player2 and (reaction.emoji == "<:pinkcheck:609771973341610033>" or reaction.emoji == "<:pinkx:609771973102534687>")
		try:
			reaction, user = await self.bot.wait_for('reaction_add', check = check_chall, timeout = 120.0)
		except asyncio.TimeoutError:
			duelEmbed.description = "The time to accept the duel has passed."

		else:
			startDuel = reaction.emoji == "<:pinkcheck:609771973341610033>"
			if reaction.emoji == "<:pinkcheck:609771973341610033>":
				duelEmbed.description = "The challenge has been accepted! Duel beginning."
			else:
				duelEmbed.description = "The challenge has been declined."
		await challenge_mess.clear_reactions()
		await challenge_mess.edit(embed=duelEmbed)
		
		if startDuel:
			def try_int(string):
				try:
					int(string)
					return True
				except ValueError:
					return False
			await ctx.send(f"{player2.mention} begin guessing!")
			correctNum = random.randint(1, 10)
			currentplayer = player2
			otherplayer = player1
			guesslist = []
			guesslist_str = "None"
			keepGoing = True
			while keepGoing:
				await ctx.send(f"{currentplayer.mention}, make your guess! Guesses so far: {guesslist_str}")
				def check_guess(message):
					return message.author == currentplayer and try_int(message.content) and int(message.content) in range(1, 10)
				try:
					guess_mess = await self.bot.wait_for("message", check = check_guess, timeout = 10.0)
				except asyncio.TimeoutError:
					keepGoing = False
					await ctx.send(f"{currentplayer.mention} did not guess in time, {otherplayer.mention} wins!")
					winningplayer = otherplayer
					losingplayer = currentplayer
				else:
					if int(guess_mess.content) == correctNum:
						keepGoing = False
						await ctx.send(f"{currentplayer.mention} guessed the correct number and won the duel!")
						winningplayer = currentplayer
						losingplayer = otherplayer
					else:
						guesslist.append(guess_mess.content)
						guesslist_str = ", ".join(guesslist)

						if currentplayer == player1:
							currentplayer = player2
						else:
							currentplayer = player1
			duelEmbed.description = f"The duel has been completed and {winningplayer.name} has won!\n\n{losingplayer.name}, you must give them your whole korb balance (`$with all`, then `$give {winningplayer.name} all`)\n\n{winningplayer}, react with <:pinkcheck:609771973341610033> once you've been paid."
			result_mess = await.ctx(content=f"{player1.mention} {player2.mention}", embed = duelEmbed)
			result_mess.add_reaction("<:pinkcheck:609771973341610033>")
			def check_confirm(reaction, user):
				return user == winningplayer and reaction.emoji == "<:pinkcheck:609771973341610033>"
			try:
				reaction, user = await self.bot.wait_for('reaction_add', check = check_confirm, timeout = 120.0)
			except asyncio.TimeoutError:
				duelEmbed.description(f"Payment to {winningplayer} by {losingplayer} has not been confirmed, staff has been notified.")
				dawdle_channel = ctx.guild.get_channel(623016717429374986)
				await dawdle_channel.send(f"Payment to {winningplayer} by {losingplayer} has not been confirmed after a duel".)
			else:
				duelEmbed.description(f"Payment confirmed. Thanks for playing!")
			await result_mess.edit(content=f"{player1.mention} {player2.mention}", embed = duelEmbed)



