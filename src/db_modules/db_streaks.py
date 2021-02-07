import discord
from discord.ext import commands
from .db_converters import SmartMember,SmartRole
from .db_checks import is_mod,in_dawdle
import json,typing
import datetime
import asyncio

class db_streaks(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		with open("src/data/streak.json", "r") as json_file:
			try:
				self.streak_dict = json.load(json_file)
			except json.decoder.JSONDecodeError:
				print ("Currently no streaks!")
				self.streak_dict = {}
	
	def check_daily(self, memid):
		currentday = datetime.datetime.utcnow().day
		yesterday  = (datetime.datetime.utcnow() - datetime.timedelta(1)).day
		return self.streak_dict[str(memid)]["lastdaily"] == currentday or self.streak_dict[str(memid)]["lastdaily"] == yesterday

	@commands.group()
	@in_dawdle()
	async def daily(self, ctx):
		if ctx.subcommand_passed is not None and ctx.invoked_subcommand is None:
			await ctx.send("No such streak command found!")
		elif ctx.subcommand_passed is None:
			async with ctx.typing():
				streakEmbed = discord.Embed(title = "Dawdle Daily", description = "Checking your messages...", color = 0xffb6c1)
				streakEmbed.set_footer(text="Daily cooldown resets at 00:00 UTC")
				response_message = await ctx.send(content = ctx.author.mention, embed=streakEmbed)
				dawdle = ctx.guild
				currentday = datetime.datetime.utcnow().day
				messagesThresh = 10
				claimed = False
				currentstreak = 0
				if str(ctx.author.id) in self.streak_dict.keys():
					daily_check = self.check_daily(ctx.author.id)
					lastdaily = self.streak_dict[str(ctx.author.id)]["lastdaily"]
					if daily_check:
						currentstreak = self.streak_dict[str(ctx.author.id)]["streak"]
					if lastdaily == currentday:
						claimed = True
						response = f"<a:pout:586761599042322432> Oh my poyo! You have already claimed today’s daily.\n\n**Your streak: {currentstreak}**"
						response_image = "https://cdn.discordapp.com/attachments/654787316665286714/803369575944683530/16115444044027802_1.gif"
				else:
					self.streak_dict[str(ctx.author.id)] = {"streak" : 0, "lastdaily" : 0}

				if not claimed:	
					nMessages = 0
					parlor = dawdle.get_channel(514550733732053012)
					basement = dawdle.get_channel(529879816208384010)
					async def count_in_channel(channel):
						message_counter = 0
						async for mess in channel.history(limit= None):					
							if mess.created_at.day != currentday or message_counter >= messagesThresh:
								break
							if mess.author == ctx.author:
								message_counter += 1
						return message_counter
					nMessages += await count_in_channel(parlor)					
					nMessages += await count_in_channel(basement)
					if nMessages >= messagesThresh:
						currentstreak += 1
						self.streak_dict[str(ctx.author.id)]["streak"] = currentstreak
						self.streak_dict[str(ctx.author.id)]["lastdaily"] = currentday
						with open("src/data/streak.json", "w") as json_file:
							json.dump(self.streak_dict, json_file)
						response = f"<a:kittyyay:741075018905288767> Yay, you sent enough messages today! Daily has been claimed.\n\n**Your streak: {currentstreak}**"
						response_image = "https://cdn.discordapp.com/attachments/654787316665286714/803369022112006184/lrGphW1r.gif"
					else:
						response = f"<a:cryingcat:663168879383543818> Sorry, you haven’t sent enough messages today to claim a daily.\n\n**Your streak: {currentstreak}**"
						response_image = "https://cdn.discordapp.com/attachments/654787316665286714/803369490355191828/16115444044027802.gif"
				
				streakEmbed.description = response 
				streakEmbed.set_image(url=response_image)
				await response_message.edit(content = ctx.author.mention, embed=streakEmbed)

	@daily.command(aliases = ["lb"])
	async def leaderboard(self, ctx):
		sorted_lb = sorted(self.streak_dict.items(), key=lambda x: x[1]["streak"], reverse=True)

		lb_str_list = []
		rank = 1
		for strk in sorted_lb:
			member = ctx.guild.get_member(int(strk[0]))
			if member and strk[1]["streak"] > 0 and self.check_daily(member.id):
				lb_str = f"[{rank}] {member}".ljust(24)
				lb_str = lb_str+str(strk[1]["streak"])
				lb_str_list.append(lb_str)
				rank += 1

		lbEmbed = discord.Embed(title = "Daily Streak Leaderboard", description = "```"+"\n".join(lb_str_list)+"```", color = 0xffb6c1)
		await ctx.send(embed=lbEmbed)
		
	@daily.command()
	@is_mod()
	async def clean(self, ctx):
		cleanList = []
		for memid in self.streak_dict.keys():
			if not ctx.guild.get_member(int(memid)):
				cleanList.append(memid)
		if len(cleanList) > 0:
			for memid in cleanList:
				del self.streak_dict[memid]
			with open("src/data/streak.json", "w") as json_file:
				json.dump(self.streak_dict, json_file)

		await ctx.send(f"Cleaned {len(cleanList)} members.")



	@daily.command()
	@is_mod()
	async def set(self, ctx, member : SmartMember, streak : int): 
		if str(member.id) in self.streak_dict.keys():
			self.streak_dict[str(member.id)]["streak"] = streak
		else:
			self.streak_dict[str(member.id)] = {"streak" : streak, "lastdaily" : 0}
		with open("src/data/streak.json", "w") as json_file:
			json.dump(self.streak_dict, json_file)
		await ctx.send(f"Set {member.mention}'s streak to {streak}.")




