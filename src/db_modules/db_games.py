import discord
from discord.ext import commands
from .db_converters import SmartMember,SmartRole
from .db_checks import is_mod,in_dawdle
import json,typing
import datetime
import asyncio
import random

scenario_dict = {
	"{user1} looks at {user2} and says \"Why are we in a burning plane?\", they shrug and you both look around for a pilot, there is no pilot and there's a big mountain closing in fast. You head to the back of the plane and find a box filled with parachutes. Unfortunately most of them have holes in. Which one of you will be lucky enough to find the pristine parachute?" : "{winner} jumps from the plane and swipes {loser}'s bank card, they gently fall to the ground with that lucky pristine parachute.",
	"{user1} and {user2} wake up naked and alone tied up to chairs in a very dark, dreary room. You see Kirby emerge from the shadows and he is holding a knife. He says, “do you want to play a game?” You both look at eachother in fear and shake your heads no. He laughs and makes you watch a 10 hour Shrek marathon. In order to win the game, you have to guess his favorite Shrek character." : "{winner} guesses the Shrek character correctly! It was Fiona, who would’ve thought?  {loser}’s chair falls into a hole never to be seen again.",
	"{user1} and {user2} wake up in a kirby dungeon, and a menacing kirby stares at them. He says \"There are ten jellybeans. Pick the right one and I will allow you to escape. Pick the wrong one, and you will be turned into a giant pink giraffe. Choose wisely\"." : "{winner} picks the bright pink jellybean and the kirby sets them free! {loser} picks the dark green one and suddenly transforms into a giant pink giraffe. Oops!"
}

class db_games(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	@in_dawdle()
	async def duel(self, ctx, member : SmartMember):
		player1 = ctx.author
		player2 = member
		#duelScenario = 
		startDuel = False
		duelEmbed = discord.Embed(title = "Duel", description = f"{player2}, you've been challenged to a duel by {player1}!\n\n**If you accept, you will both have to guess the number I'm thinking of between 1 and 10. The winner wins the loser's entire korb balance! You'll only have 10 seconds for each guess so think fast.**\n\n{player2}, react with a <:pinkcheck:609771973341610033> to accept or a <:pinkx:609771973102534687> to decline.", color = 0xffb6c1)
		challenge_mess = await ctx.send(content=f"{player1.mention} {player2.mention}" , embed=duelEmbed)
		await challenge_mess.add_reaction("<:pinkcheck:609771973341610033>")
		await challenge_mess.add_reaction("<:pinkx:609771973102534687>")
		def check_chall(reaction, user):			
			return user.id == player2.id and (str(reaction.emoji) == "<:pinkcheck:609771973341610033>" or str(reaction.emoji) == "<:pinkx:609771973102534687>")
		try:
			reaction, user = await self.bot.wait_for('reaction_add', check = check_chall, timeout = 120.0)
		except asyncio.TimeoutError:
			duelEmbed.description = "The time to accept the duel has passed."

		else:
			startDuel = str(reaction.emoji) == "<:pinkcheck:609771973341610033>"
			if str(reaction.emoji) == "<:pinkcheck:609771973341610033>":
				scenario = random.choice(list(scenario_dict.keys()))
				scenario_tosend = scenario.replace("{user1}", player1.name)
				scenario_tosend = scenario_tosend.replace("{user2}", player2.name)
				duelEmbed.description = "The challenge has been accepted! The scenario is below. **Guessing begins in 10 seconds**.\n\n"+scenario_tosend
			else:
				duelEmbed.description = "The challenge has been declined."
		await challenge_mess.clear_reactions()
		await challenge_mess.edit(embed=duelEmbed)
		
		if startDuel:
			await asyncio.sleep(10)
			def try_int(string):
				try:
					int(string)
					return True
				except ValueError:
					return False
			correctNum = random.randint(1, 10)
			currentplayer = player2
			otherplayer = player1
			guesslist = []
			guesslist_str = "None"
			keepGoing = True
			while keepGoing:
				await ctx.send(f"{currentplayer.mention}, make your guess! Guesses so far: {guesslist_str}")
				def check_guess(message):
					return message.author == currentplayer and try_int(message.content) and int(message.content) in range(1, 11)
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
#						await ctx.send(f"{currentplayer.mention} guessed the correct number and won the duel!")
						winningplayer = currentplayer
						losingplayer = otherplayer
					else:
						guesslist.append(guess_mess.content)
						guesslist_str = ", ".join(guesslist)

						if currentplayer == player1:
							currentplayer = player2
						else:
							currentplayer = player1
			victory = scenario_dict[scenario]
			victory_tosend = victory.replace("{winner}", winningplayer.name)
			victory_tosend = victory_tosend.replace("{loser}", losingplayer.name)
			duelEmbed.description = victory_tosend+f"\n\nThe duel has been completed and {winningplayer.name} has won!\n\n{losingplayer.name}, **you must give them your whole korb balance (`$with all`, then `$give {winningplayer.name} all`)\n\n{winningplayer}, react with <:pinkcheck:609771973341610033> once you've been paid.**"
			result_mess = await ctx.send(content=f"{player1.mention} {player2.mention}", embed = duelEmbed)
			await result_mess.add_reaction("<:pinkcheck:609771973341610033>")
			def check_confirm(reaction, user):
				return user.id == winningplayer.id and str(reaction.emoji) == "<:pinkcheck:609771973341610033>"
			try:
				reaction, user = await self.bot.wait_for('reaction_add', check = check_confirm, timeout = 120.0)
			except asyncio.TimeoutError:
				duelEmbed.description = victory_tosend+f"\n\nPayment to {winningplayer} by {losingplayer} has not been confirmed, staff has been notified."
				dawdle_channel = ctx.guild.get_channel(623016717429374986)
				await dawdle_channel.send(f"Payment to {winningplayer} by {losingplayer} has not been confirmed after a duel.")
			else:
				duelEmbed.description=victory_tosend+f"\n\nPayment confirmed. Thanks for playing!"
			await result_mess.edit(content=f"{player1.mention} {player2.mention}", embed = duelEmbed)
			await result_mess.clear_reactions()



