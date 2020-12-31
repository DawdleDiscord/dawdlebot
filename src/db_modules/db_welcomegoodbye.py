import discord
import json
from discord.ext import commands
from .db_checks import is_mod

class db_welcomegoodbye(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		with open("src/data/wcgb_messages.json", "r") as json_file:
			try:
				self.wgb_dict = json.load(json_file)
			except json.decoder.JSONDecodeError:
				print ("Currently no messages!! Using default.")
				self.wgb_dict = {"welcome": "Welcome to Dawdle, {ment}. Please read <#479407137060028449> to know how to access the rest of the server! Enjoy your stay.",
				"goodbye" : "{user} has departed Dawdle. Until next time!", "screened" : False}
				with open("src/data/wcgb_messages.json", "w") as json_file:
					json.dump(self.wgb_dict, json_file)
			self.welcome_form = self.wgb_dict["welcome"]
			self.goodbye_form = self.wgb_dict["goodbye"]
			self.setup_wcgb()

	def setup_wcgb(self):
		to_place = self.wgb_dict["welcome"].find("{")
		ident = self.wgb_dict["welcome"][to_place+1: to_place+5]
		trunc = self.wgb_dict["welcome"].replace(ident, "")
		self.welcome_form = {"message" : trunc, "ident" : ident}
		to_place = self.wgb_dict["goodbye"].find("{")
		ident = self.wgb_dict["goodbye"][to_place+1: to_place+5]
		trunc = self.wgb_dict["goodbye"].replace(ident, "")
		self.goodbye_form = {"message" : trunc, "ident" : ident}

	@commands.command()
	@is_mod()
	async def setwelcome(self, ctx):
		responseEmbed = discord.Embed(title = "Type new welcome message below or type `cancel` to exit.", color=0xffb6c1)
		responseEmbed.add_field(name = "Current", value = self.wgb_dict["welcome"])
		responseEmbed.add_field(name = "Formatting", value = "{ment} to mention, {user} for name#xxxx, {name} for name")
		menu = await ctx.send(embed=responseEmbed)
		def check_resp(message):
			return message.author == ctx.author and message.channel == ctx.channel
		try:
			response = await self.bot.wait_for('message', check = check_resp, timeout = 120.0)
		except asyncio.TimeoutError:
			await ctx.send('Response timed out. Message unchanged.')
		else:
			#check for formatting here
			if response.content.lower() != "cancel":
				responseEmbed.add_field(name = "New", value = response.content)
				self.wgb_dict["welcome"] = response.content
				self.setup_wcgb()
				with open("src/data/wcgb_messages.json", "w") as json_file:
					json.dump(self.wgb_dict, json_file)
				responseEmbed.title = "Saved new welcome message!"
				welc_mess = ""
				if self.welcome_form["ident"] == "ment" : welc_mess = self.welcome_form["message"].format(ctx.author.mention)
				elif self.welcome_form["ident"] == "user" : welc_mess = self.welcome_form["message"].format(ctx.author)
				elif self.welcome_form["ident"] == "name" : welc_mess = self.welcome_form["message"].format(ctx.author.name)
				await ctx.send("Test: "+welc_mess)
			else:
				responseEmbed.title = "Welcome message unchanged."
			await menu.edit(embed = responseEmbed)

	@commands.command()
	@is_mod()
	async def setgoodbye(self, ctx):
		responseEmbed = discord.Embed(title = "Type new goodbye message below or type `cancel` to exit.", color=0xffb6c1)
		responseEmbed.add_field(name = "Current", value = self.wgb_dict["goodbye"])
		responseEmbed.add_field(name = "Formatting", value = "{ment} to mention, {user} for name#xxxx, {name} for name")
		menu = await ctx.send(embed=responseEmbed)
		def check_resp(message):
			return message.author == ctx.author and message.channel == ctx.channel
		try:
			response = await self.bot.wait_for('message', check = check_resp, timeout = 120.0)
		except asyncio.TimeoutError:
			await ctx.send('Response timed out. Message unchanged.')
		else:
			#check for formatting here
			if response.content.lower() != "cancel":
				responseEmbed.add_field(name = "New", value = response.content)
				self.wgb_dict["goodbye"] = response.content
				self.setup_wcgb()
				with open("src/data/wcgb_messages.json", "w") as json_file:
					json.dump(self.wgb_dict, json_file)
				responseEmbed.title = "Saved new goodbye message!"
				gb_mess = ""
				if self.goodbye_form["ident"] == "ment" : gb_mess = self.goodbye_form["message"].format(ctx.author.mention)
				elif self.goodbye_form["ident"] == "user" : gb_mess = self.goodbye_form["message"].format(ctx.author)
				elif self.goodbye_form["ident"] == "name" : gb_mess = self.goodbye_form["message"].format(ctx.author.name)
				await ctx.send("Test: "+gb_mess)
			else:
				responseEmbed.title = "goodbye message unchanged."
			await menu.edit(embed = responseEmbed)

	# @commands.command()
	# @is_mod()
	# async def setscreened(self, ctx, screen : bool):
	# 	if "screened" not in self.wgb_dict.keys() or screen != self.wgb_dict["screened"]:
	# 		self.wgb_dict["screened"] = screen
	# 		with open("src/data/wcgb_messages.json", "w") as json_file:
	# 			json.dump(self.wgb_dict, json_file)

	# 		if screen:
	# 			await ctx.send("Will now only grant unverified role after screening.")
	# 		else:
	# 			await ctx.send("Will now grant unverified role upon joining.")

	# 	else: 
	# 		await ctx.send("This setting is already active.")


	@commands.Cog.listener()
	async def on_member_join(self, member):
	#	if "screened" not in self.wgb_dict.keys() or not self.wgb_dict["screened"]:
		if True:
			dawdle = self.bot.get_guild(475584392740339712)
			unverifrole = dawdle.get_role(479410607821684757)
			foyerchannel = dawdle.get_channel(514554494495752204)
			welc_mess = ""
			if member.guild == dawdle:
				if self.welcome_form["ident"] == "ment" : welc_mess = self.welcome_form["message"].format(member.mention)
				elif self.welcome_form["ident"] == "user" : welc_mess = self.welcome_form["message"].format(member)
				elif self.welcome_form["ident"] == "name" : welc_mess = self.welcome_form["message"].format(member.name)
				await foyerchannel.send(welc_mess)
				await member.add_roles(unverifrole)
				try:
					await member.send(f'Hi {member.name}, welcome to Dawdle! We\'re so happy to have you! Please read <#479407137060028449> for details on how to get verified so that the rest of the server can be opened up to you.\n \nVerification is required to stay, but we understand if you can\'t do it right away. <#514550733732053012> is open for you to talk and say hi before you verify so you can meet some of the great folks that we have! \n \n**When you\'re ready to verify, please send your items to me (this bot) so that a member of staff can review it and you can access more of the server!**')
				except:
					pass
			countchannel = dawdle.get_channel(705498700771754054)
			await countchannel.edit(name=f'members: {dawdle.member_count}')

	# @commands.Cog.listener()
	# async def on_member_update(self, before, after):
	# 	if "screened" in self.wgb_dict.keys() and self.wgb_dict["screened"]:
	# 		if before.pending and not after.pending:
	# 			dawdle = self.bot.get_guild(475584392740339712)
	# 			unverifrole = dawdle.get_role(479410607821684757)
	# 			foyerchannel = dawdle.get_channel(514554494495752204)
	# 			welc_mess = ""
	# 			if member.guild == dawdle:
	# 				if self.welcome_form["ident"] == "ment" : welc_mess = self.welcome_form["message"].format(member.mention)
	# 				elif self.welcome_form["ident"] == "user" : welc_mess = self.welcome_form["message"].format(member)
	# 				elif self.welcome_form["ident"] == "name" : welc_mess = self.welcome_form["message"].format(member.name)
	# 				await foyerchannel.send(welc_mess)
	# 				await member.add_roles(unverifrole)
	# 				try:
	# 					await member.send(f'Hi {member.name}, welcome to Dawdle! We\'re so happy to have you! Please read <#479407137060028449> for details on how to get verified so that the rest of the server can be opened up to you.\n \nVerification is required to stay, but we understand if you can\'t do it right away. <#514550733732053012> is open for you to talk and say hi before you verify so you can meet some of the great folks that we have! \n \n**When you\'re ready to verify, please send your items to me (this bot) so that a member of staff can review it and you can access more of the server!**')
	# 				except:
	# 					pass
	# 			countchannel = dawdle.get_channel(705498700771754054)
	# 			await countchannel.edit(name=f'members: {dawdle.member_count}')			


	@commands.Cog.listener()
	async def on_member_remove(self, member):
		dawdle = self.bot.get_guild(475584392740339712)
		foyerchannel = dawdle.get_channel(514554494495752204)
		introChannel = dawdle.get_channel(514555898648330260)
		verifrole = dawdle.get_role(481148097960083471)
		verified = False
		if member.guild == dawdle:
			for role in member.roles:
				if role == verifrole:
					verified = True
					break
			if verified and member.id != 381507393470857229:
				def is_user(message):
					return message.author == member
				deleted = await introChannel.purge(limit=None,check=is_user)
			gb_mess = ""
			if self.goodbye_form["ident"] == "ment" : gb_mess = self.goodbye_form["message"].format(member.mention)
			elif self.goodbye_form["ident"] == "user" : gb_mess = self.goodbye_form["message"].format(member)
			elif self.goodbye_form["ident"] == "name" : gb_mess = self.goodbye_form["message"].format(member.name)
			await foyerchannel.send(gb_mess)
		countchannel = dawdle.get_channel(705498700771754054)
		await countchannel.edit(name=f'members: {dawdle.member_count}')
