import discord
from discord.ext import commands
from .db_checks import is_mod,in_dawdle
import datetime
from .db_converters import SmartMember,SmartRole
import asyncio
import json
import typing

class db_warns(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		with open("src/data/warnings.json", "r") as json_file:
			try:
				self.all_warns = json.load(json_file)
			except json.decoder.JSONDecodeError:
				print ("Currently no warns!")
				self.all_warns = []

	async def get_warn_embed(self, ctx, current_warn):
		warn_embed = discord.Embed(title = "Warning")
		if ctx.guild and ctx.guild.get_member(current_warn["member"]) is not None:				
			warn_embed.add_field(name = "member", value = ctx.guild.get_member(current_warn["member"]).mention)
		else:
			member_name = await self.bot.fetch_user(current_warn["member"])
			warn_embed.add_field(name = "member", value = member_name)
		if current_warn["rule"]: 
			warn_embed.add_field(name = "rule", value = current_warn["rule"])	
		else:
			warn_embed.add_field(name = "rule", value = "[none given]")
		if current_warn["context"]:
			warn_embed.add_field(name = "context", value = current_warn["context"])
		else:
			warn_embed.add_field(name = "context", value = "[none given]")
		if ctx.guild and ctx.guild.get_member(current_warn["mod"]) is not None:
			warn_embed.add_field(name = "mod", value = ctx.guild.get_member(current_warn["mod"]).mention)
		else:
			mod_name = await self.bot.fetch_user(current_warn["mod"])
			warn_embed.add_field(name = "mod", value = mod_name)
		warn_embed.add_field(name = "date", value = current_warn["date"])
		if "attachments" in current_warn.keys():
			warn_embed.add_field(name = "attachments", value = " ".join(current_warn["attachments"]))
		return warn_embed				

	def save_warnings(self):
		with open("src/data/warnings.json", "w") as json_file:
			json.dump(self.all_warns, json_file)

	@commands.command()
	@is_mod()
	async def warn(self, ctx, member : SmartMember, rule : str, admon : typing.Optional[bool] = True):
		current_warn = {}
		await ctx.send(f"{member.mention} will be warned for `{rule}`. Respond with context or type `cancel`.")

		def check_response(m):
			return  m.author == ctx.author and m.channel == ctx.channel
		try: 
			context_resp = await ctx.bot.wait_for('message', check=check_response, timeout = 180.0)
		except asyncio.TimeoutError:
			await ctx.send("Response timed out, warn canceled.")
		else:
			if context_resp.content.lower() == "cancel":
				await ctx.send("Warn canceled.")
			elif len(context_resp.content) > 1024:
				await ctx.send("Context must be 1024 characters or less.")
			else:
				current_warn["member"]  = member.id
				current_warn["rule"]    = rule
				if context_resp.content:
					current_warn["context"] = context_resp.content
				else:
					current_warn["context"] = "[none given]"
				current_warn["date"]    = str(datetime.date.today())
				current_warn["mod"]     = ctx.author.id
				if len(context_resp.attachments) > 0:
					url_list = []
					counter = 1
					for attach in context_resp.attachments:
						url_list.append(f"[{counter}]({attach.url})")
						counter += 1
					current_warn["attachments"] = url_list
				warn_embed = await self.get_warn_embed(ctx, current_warn)
				self.all_warns.append(current_warn)
				self.save_warnings()
				await ctx.send(embed=warn_embed)
				if admon and rule.lower() != "verbal":
					admonchannel = ctx.guild.get_channel(527899554184691715)
					await admonchannel.send(f"```{member} was warned by {ctx.author.name} (Rule {rule})```")
					try:
						await member.send(f"You have been warned in Dawdle for Rule {rule}. If you would like more information, you can contact staff by responding with `~report <your message>`.\n \nUse `~mywarnings` to see all of your warnings.")
					except:
						await ctx.send(f"I could not DM {member.mention}")

	@commands.command()
	@is_mod()
	async def warnings(self, ctx, member : SmartMember, warn_type : typing.Optional[str] = ""):
		warncolors = { "official" : discord.Colour.red(), "verbal" : discord.Colour.orange(), "oldverbal" : discord.Colour.gold()}
		counter = 1
		officialcounter = 1
		is_any = False
		invalid_warnings = []
		for warn in self.all_warns:
			if warn["member"] == member.id:
				if len(warn["context"]) > 1024:
					invalid_warnings.append(warn)
					continue
				if warn_type == "verbal" and warn["rule"].lower() != "verbal":
					counter += 1
					continue
				if warn_type == "nonverbal" and warn["rule"].lower() == "verbal":
					counter += 1
					continue
				is_any = True
				warn_embed = await self.get_warn_embed(ctx, warn)
				if warn["rule"].lower() == "verbal":
					if abs((datetime.date.today() - datetime.datetime.strptime(warn["date"], "%Y-%m-%d").date()).days) < 60:
						warn_embed.color = warncolors["verbal"]
					else:
						warn_embed.color = warncolors["oldverbal"] 
					warncount = f"**Warn {counter} [verbal]**"
				else:
					warn_embed.color = warncolors["official"]
					warncount = f"**Warn {counter} [Official: {officialcounter}]**"
					officialcounter += 1
				await ctx.send(content = warncount, embed = warn_embed)
				counter += 1
		if not is_any:
			await ctx.send(f"{member} has no {warn_type} warnings.")

		for invalid in invalid_warnings:
			self.all_warns.remove(invalid)
	
	@commands.command()
	async def mywarnings(self, ctx):
		is_any = False
		counter = 1
		for warn in self.all_warns:
			if warn["member"] == ctx.author.id and warn["rule"].lower() != "verbal":
				warn_embed = await self.get_warn_embed(ctx, warn)
				warn_embed.remove_field(2)
				if len(warn_embed.fields) == 5:
					warn_embed.remove_field(4)
				is_any = True
				await ctx.send(content = f"**Warn {counter}**", embed = warn_embed)
				counter += 1
		if not is_any:
			await ctx.send("You have no warnings.")

	@commands.command()
	@is_mod()
	async def editwarning(self, ctx, member : SmartMember, number : int):
		counter = 0
		for warnIt in range(len(self.all_warns)):
			if self.all_warns[warnIt]["member"] == member.id:
				counter += 1
				if number == counter:
					await ctx.send("Reply with updated context.")
					def check_response(m):
						return  m.author == ctx.author and m.channel == ctx.channel
					try: 
						context_resp = await ctx.bot.wait_for('message', check=check_response, timeout = 180.0)
					except asyncio.TimeoutError:
						await ctx.send("Response timed out, update canceled.")
					else:
						if context_resp.content.lower() == "cancel":
							await ctx.send("update canceled.")
						else:
							self.all_warns[warnIt]["context"] = context_resp.content
							warn_embed = await self.get_warn_embed(ctx, self.all_warns[warnIt])
							self.save_warnings()
							await ctx.send(embed=warn_embed)
					break				
		if counter < number:
			await ctx.send(f"This member only has {counter} warnings.")

	@commands.command(aliases = ["delwarning"])
	@is_mod()
	async def deletewarning(self, ctx, member : SmartMember, number : int):
		delete_number = -1
		counter = 1
		for warnIt in range(len(self.all_warns)):
			if self.all_warns[warnIt]["member"] == member.id:
				if number == counter:
					warn_embed = await self.get_warn_embed(ctx, self.all_warns[warnIt])
					await ctx.send(content = "Are you sure you want to delete this warning? (yes/no).", embed = warn_embed)
					def check_response(m):
						return  m.author == ctx.author and m.channel == ctx.channel and (m.content.lower() == "yes" or m.content.lower() == "no")
					try: 
						context_resp = await ctx.bot.wait_for('message', check=check_response, timeout = 60.0)
					except asyncio.TimeoutError:
						await ctx.send("Response timed out, delete canceled.")
					else:
						if context_resp.content.lower() == "no":
							await ctx.send("Delete canceled.")
						else:
							delete_number = warnIt
					break
				counter += 1
		if delete_number != -1:
			del self.all_warns[delete_number]
			self.save_warnings()
			await ctx.send("Warning deleted.")
