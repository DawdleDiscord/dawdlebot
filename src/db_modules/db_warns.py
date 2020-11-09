import discord
from discord.ext import commands
from .db_checks import is_mod
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
		warn_embed = discord.Embed(title = "Warning", color=0xffb6c1)				
		warn_embed.add_field(name = "member", value = ctx.guild.get_member(current_warn["member"]).mention)
		warn_embed.add_field(name = "rule", value = current_warn["rule"])			
		warn_embed.add_field(name = "context", value = current_warn["context"])
		if ctx.guild.get_member(current_warn["mod"]) is not None:
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
			else:
				current_warn["member"]  = member.id
				current_warn["rule"]    = rule
				current_warn["context"] = context_resp.content
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
				if admon:
					admonchannel = ctx.guild.get_channel(527899554184691715)
					await admonchannel.send(f"```{member} was warned by {ctx.author.name} (Rule {rule})```")
					try:
						await member.send(f"You have been warned in Dawdle for Rule {rule}. If you would like more information, you can contact staff by responding with`~report <your message>`.")
					except:
						await ctx.send(f"I could not DM {member.mention}")

	@commands.command()
	@is_mod()
	async def warnings(self, ctx, member : SmartMember):
		counter = 1
		for warn in self.all_warns:
			if warn["member"] == member.id:
				warn_embed = await self.get_warn_embed(ctx, warn)
				await ctx.send(content = f"**Warn {counter}**", embed = warn_embed)
				counter += 1

	@commands.command()
	@is_mod()
	async def editwarning(self, ctx, member : SmartMember, number : int):
		counter = 1
		for warnIt in range(len(self.all_warns)):
			if self.all_warns[warnIt]["member"] == member.id and number == counter:
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
			counter += 1

	@commands.command(aliases = ["delwarning"])
	@is_mod()
	async def deletewarning(self, ctx, member : SmartMember, number : int):
		delete_number = -1
		counter = 1
		for warnIt in range(len(self.all_warns)):
			if self.all_warns[warnIt]["member"] == member.id:
				if number == counter:
					warn_embed = await self.get_warn_embed(ctx, self.all_warns[warnIt])
					await ctx.send(content = "Are you sure you want to delete this warnining? (yes/no).", embed = warn_embed)
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