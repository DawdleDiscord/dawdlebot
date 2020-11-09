import discord
from .db_checks import is_mod, in_dawdle
from discord.ext import commands, tasks
import typing
from .db_converters import SmartMember
import json
import asyncio

class db_inventory(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		with open("src/data/inventoryitems.json", "r") as json_file:
			try:
				self.invitems = json.load(json_file)
			except json.decoder.JSONDecodeError:
				print ("Currently no items!")
				self.invitems = {}
			with open("src/data/inventoryusers.json", "r") as json_file:
				try:
					self.invusers = json.load(json_file)
				except json.decoder.JSONDecodeError:
					print ("Currently no inventories!")
					self.invusers = {}

	def saveitems(self):
		with open("src/data/inventoryitems.json", "w") as json_file:
			json.dump(self.invitems, json_file)
	def saveinvs(self):
		with open("src/data/inventoryusers.json", "w") as json_file:
			json.dump(self.invusers, json_file)


	@commands.group()
	@is_mod()
	async def editinv(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.send('Invalid editinv command')

	@editinv.command()
	async def add(self, ctx, *, item_name : str):
		keepGoing = True
		foundItem = False		
		for item in self.invitems.keys():
			if item_name.lower() == item.lower():
				foundItem = True
				break
		if foundItem:
			await ctx.send(f"**Warning**: {item_name} already found, this will overwrite it.")
		invEmbed = discord.Embed(title = item_name, color=0xffb6c1)
		invEmbed.add_field(name = "Desription", value = "Enter description or `cancel`.")
		invAdd = await ctx.send(embed = invEmbed)
		def check_response(message):
			return message.author == ctx.author and message.channel == ctx.channel
		def check_yesno(message):
			return message.author == ctx.author and message.channel == ctx.channel and (message.content.lower() == "yes" or message.content.lower() == "no")
		try:
			response = await self.bot.wait_for("message", check = check_response, timeout = 60.0)
		except asyncio.TimeoutError:
			await invAdd.edit(content="Timed out, item addition canceled.", supress = True)
		else:
			if response.content.lower() == "cancel":
				await invAdd.edit(content="Item addition canceled.", supress = True)
				keepGoing = False
			else:
				invEmbed.set_field_at(0, name = "Description", value = response.content)
				#invEmbed.add_field(name = "Use", value = "Is this item usable? (yes/no)")
				await invAdd.edit(embed=invEmbed)
				self.invitems[item_name] = response.content
				self.saveitems()
				# try:
				# 	use_resp = await self.bot.wait_for("message", check = check_yesno, timeout = 60.0)
				# except asyncio.TimeoutError:
				# 	await invAdd.edit(content="Timed out, item addition canceled.", supress = True)
				# else:
				# 	if use_resp.content == "yes":
				# 		use = True
				# 	else:
				# 		use = False
				# 	invEmbed.set_field_at(1, name = "Use", value = str(use))
					
				# 	if use:
				# 		invEmbed.add_field(name = "Reply message", value = "Enter reply message")
				# 		await invAdd.edit(embed=invEmbed)
				# 		try:
				# 			reply_resp = await self.bot.wait_for("message", check = check_response, timeout = 60.0)
				# 		except asyncio.TimeoutError:
				# 			await invAdd.edit(content="Timed out, item addition canceled.", supress = True)
				# 		else:
				# 			if reply_resp.content.lower() == "cancel":
				# 				await invAdd.edit(content="Item addition canceled.", supress = True)
				# 			else:
				# 				invEmbed.set_field_at(2, name = "Reply message", value = reply_resp.content)
				# 				await invAdd.edit(embed=invEmbed)
				# 				self.invitems[item_name] = {"description" : response.content,
				# 											"use" : str(use),
				# 											"reply" : reply_resp.content}
							
				# 	else:
				# 		await invAdd.edit(embed=invEmbed)
				# 		self.invitems[item_name] = {"description" : response.content,
				# 										"use" : str(use),
				# 										"reply" : "none"}
				# 	self.saveitems()
				# 	invEmbed.title = f"{item_name} was saved!"
				# 	await invAdd.edit(embed=invEmbed)

	@editinv.command()
	async def remove(self, ctx, *, item_name : str):
		try:
			for item in self.invitems.keys():
				if item_name.lower() in item.lower():
					item_name = item
					break
			descr = self.invitems[item_name]
			invEmbed = discord.Embed(title = item_name, color=0xffb6c1)
			invEmbed.add_field(name = "Description", value = descr)
			confirm = await ctx.send("Delete this item? (yes/no)", embed=invEmbed)
			def response_check(message):
				return message.author == ctx.author and message.channel == ctx.channel and (message.content.lower() == "yes" or message.content.lower() == "no")
			try:
				response = await self.bot.wait_for("message", check = response_check, timeout = 60.0)
			except asyncio.TimeoutError:
				await confirm.edit(content="Response timed out, item not deleted.", supress = True)
			else:
				if response.content == "yes":
					del self.invitems[item_name]
					self.saveitems()
					await confirm.edit(content=f"{item_name} was deleted.", supress = True)
				elif response.content == "no":
					await confirm.edit(content="Item not deleted.", supress = True)
		except KeyError:
			await ctx.send("Item not found.")

	# @editinv.command()
	# async def edit(self, ctx, *, item_name : str):
	# 	def get_response():
	# 		def check(message):
	# 			return message.author == ctx.author and message.channel == ctx.channel
	# 		try:
	# 			response = await self.bot.wait_for("message", check = check, timeout = 60.0)
	# 		except asyncio TimeoutError:
	# 				await editMess.edit(content = "Editing timed out")
	# 				return None
	# 		else:
	# 			return response.content
	# 	foundItem = False
	# 	for item in self.invitems.keys():
	# 		if item_name.lower() in item.lower():
	# 			item_name = item
	# 			foundItem = True
	# 			break
	# 	if foundItem:
	# 		try:
	# 			itemEmbed = discord.Embed(title = f"Editing {item_name}, reply with what you want to change or `cancel`.", color=0xffb6c1)
	# 			itemEmbed.add_field(name = "Description", value = self.invitems[item_name]["description"])
	# 			itemEmbed.add_field(name = "Use", value = self.invitems[item_name]["use"])
	# 			if self.invitems[item_name]["use"] == "True":
	# 				itemEmbed.add_field(name = "Reply message", value = self.invitems[item_name]["reply"])
	# 			editMess = await ctx.send(embed=itemEmbed)
	# 		except KeyError:
	# 			await ctx.send(f"{item_name} is missing some information, please re-add it!")
	# 		else:
	# 			def check_edit(message):
	# 				possible = ["description", "use", "reply message", "cancel"]
	# 				return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() in possible
	# 			try:
	# 				response = await self.bot.wait_for("message", check = check_edit, timeout = 60.0)
	# 			except asyncio TimeoutError:
	# 				await editMess.edit(content = "Editing timed out")
	# 			else:
	# 				message.content.lower() = to_edit
	# 				if to_edit == "cancel":
	# 					await editMess.edit(content = "Editing canceled")
	# 				elif to_edit == "description":
	# 					itemEmbed.set_field_at(0, name = "Description", value = "Enter new discription")
	# 					new_descr = get_response()



		else:
			await ctx.send("No such item found.")

	@editinv.command()
	async def list(self, ctx):
		itemlist_str = "\n".join(list(self.invitems.keys()))
		invEmbed = discord.Embed(title = "All Items", description = itemlist_str, color=0xffb6c1)
		await ctx.send(embed=invEmbed)

	# @editinv.command()
	# async def clean(self, ctx):
	# 	ncleaned = 0
	# 	for user in self.invusers.keys():
	# 		if ctx.guild.get_member(int(user)) is None:
	# 			del self.invusers[user]
	# 			ncleaned += 1
	# 	self.saveinvs()
	# 	await ctx.send(f"Removed the inventories of {ncleaned} former members.")


	@commands.group(aliases=['inv'])
	@in_dawdle()
	async def inventory(self, ctx):
		if ctx.subcommand_passed is not None and ctx.invoked_subcommand is None:
			await ctx.send("No such command found!")

		elif ctx.subcommand_passed is None:
			item_list_str = []
			try:
				item_list = self.invusers[str(ctx.author.id)]
				for item in item_list.keys():
					item_list_str.append(f"{item} - {item_list[item]}")
				descr = "\n".join(item_list_str)
			except KeyError:
				descr = "*just dust here*"
			if not item_list_str:
				descr = "*just dust here*" 
			invEmbed = discord.Embed(title = f"{ctx.author.name}'s inventory", description = descr, color=0xffb6c1)
			await ctx.send(embed=invEmbed)
	
	@inventory.command()
	async def info(self, ctx, *, item_name : str):
		foundItem = False
		for item in self.invitems.keys():
			if item_name.lower() in item.lower():
				item_name = item
				foundItem = True
				break
		if foundItem:
			itemEmbed = discord.Embed(title = item_name, description = self.invitems[item_name], color=0xffb6c1)
			await ctx.send(embed= itemEmbed)
		else:
			await ctx.send("No such item found.")

	@inventory.command()
	@is_mod()
	async def give(self, ctx, member : SmartMember, number : int, *, item_name : str):
		foundItem = False
		for item in self.invitems.keys():
			if item_name.lower() in item.lower():
				item_name = item
				foundItem = True
				break
		foundUser = False
		for userID in self.invusers.keys():
			if str(member.id) == userID:
				foundUser = True
				break

		if foundItem and foundUser:
			try:
				self.invusers[str(member.id)][item_name] = str(int(self.invusers[str(member.id)][item_name]) + number)
			except KeyError:
				self.invusers[str(member.id)][item_name] = str(number)
			self.saveinvs()
			await ctx.send(f"Gave {member} {number} {item_name}(s)." )
		elif foundItem and not foundUser:
			self.invusers[str(member.id)] = {item_name : str(number)}
			self.saveinvs()
			await ctx.send(f"Gave {member} {number} {item_name}(s)." )
		elif not foundItem:
			await ctx.send("No such item found.")


	@inventory.command()
	@is_mod()
	async def take(self, ctx, member : SmartMember, number : int, *, item_name : str):
		foundUser = False
		for userID in self.invusers.keys():
			if str(member.id) == userID:
				foundUser = True
				break
		if foundUser:
			try:
				for item in self.invusers[str(member.id)].keys():
					if item_name.lower() in item.lower():
						item_name = item
						break
				new_amt = int(self.invusers[str(member.id)][item_name]) - number
				if new_amt > 0:
					self.invusers[str(member.id)][item_name] = str(new_amt)
				else:
					del self.invusers[str(member.id)][item_name]
				self.saveinvs()
				await ctx.send(f"Removed `{number}` `{item_name}` from {member}")
			except KeyError:
				await ctx.send(f"{member} does not have a {item_name}.")
		elif not foundUser:
			await ctx.send(f"{member} does not have anything in their inventory.")

	@inventory.command()
	@is_mod()
	async def show(self, ctx, member : SmartMember):
		item_list_str = []
		try:
			item_list = self.invusers[str(member.id)]
			for item in item_list.keys():
				item_list_str.append(f"{item} - {item_list[item]}")
			descr = "\n".join(item_list_str)
		except KeyError:
			descr = "*just dust here*"
		if not item_list_str:
			descr = "*just dust here*"
		invEmbed = discord.Embed(title = f"{member.name}'s inventory", description = descr, color=0xffb6c1)
		await ctx.send(embed=invEmbed)

	# @inventory.command()
	# async def trade(self, ctx, member : SmartMember):
	#     tradeEmbed = discord.Embed(title = f"Trade Request (`cancel` to cancel)")
	#     tradeEmbed.add_field(name = "Requester", value = ctx.author.mention)
	#     tradeEmbed.add_field(name = "Recipient", value = member.mention)
	#     tradeEmbed.add_field(name = "Item to send", value = "Enter name of item to send")
	#     tradeMess = await ctx.send(embed=tradeEmbed)
	#     cancel = False
	#     def check_response(message):
	#         return message.author == ctx.author and message.channel == ctx.channel
	#     def get_answer();
	#         try:
	#             response = self.bot.wait_for("message", check = check_response, timeout = 60.0)
	#         except asyncio.TimeoutError:
	#             await tradeMess.edit("Trade request timed out", supress = True)
	#         else:
	#             return response.content
	#     keepGoing = True
	#     while keepGoing:
	#         item_to_give = get_answer()
	#         keepGoing == item_to_give.lower() != "cancel"
	#         foundItem = False
	#         for item in self.invitems.keys():
	#             if item_to_give.lower() in item.lower():
	#                 item_to_give = item
	#                 found = True
	#                 break


	async def cog_command_error(self, ctx, error):
		if isinstance(error,commands.errors.CheckFailure):
			await ctx.send("you do not have permissions to do this or you're trying to do it outside the server!")
		else:
			await ctx.send(f'Error: {str(error)}')
			print(error)
