import discord
from discord.ext import commands
import json
import asyncio
import typing
from .db_checks import is_mod
from .db_converters import SmartMember


class db_info(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		with open("src/data/information.json", "r") as json_file:
			self.info_dict = json.load(json_file)

	def save_json_dict(self, dict):
		with open("src/data/information.json", "w") as json_file:
			json.dump(dict, json_file)

	def lowercase_keys_get(self, dict, match):
		for key in dict.keys():
			if match.lower() in key.lower():
				return key
	def try_int(self, string):
		try:
			int(string)
			return True
		except ValueError:
			return False

	async def search_info(self, ctx, keyword1, keyword2 = "aaaaaaaaaaaaaaa"):
		search_results = []
		keyword1 = keyword1.lower()
		keyword2 = keyword2.lower()
		for key in self.info_dict.keys():
			for subkey in self.info_dict[key].keys():
				if keyword1 in self.info_dict[key][subkey].lower() or keyword2 in self.info_dict[key][subkey].lower():
					search_results.append([key, subkey])
		if len(search_results) == 0:
			return None
			
		elif len(search_results) == 1:
			infoEmbed = discord.Embed(title = f"`{search_results[0][0]} : {search_results[0][1]}`", description = self.info_dict[key][search_results[0][1]], color=0xffb6c1)
			return infoEmbed
		else:
			counter = 1
			results_list = []
			for res in search_results:
				key = res[0]
				subkey = res[1]
				if key == subkey:
					results_list.append(f"[{counter}] {key}")
				else:
					results_list.append(f"[{counter}] {key} : {subkey}")
				counter += 1
			
			results_list_str = f'Multiple results, select number next to info you would like to see.```\n'+'\n'.join(results_list)+'\n```'
			tempEmbed = discord.Embed(title = "Search", description = results_list_str, color=0xffb6c1)
			await ctx.send(embed = tempEmbed)
			def check(m):
				return m.author == ctx.author and m.channel == ctx.channel and (self.try_int(m.content) or m.content.lower() == "cancel")
			try:
				confirm = await ctx.bot.wait_for('message', check=check, timeout = 60.0)
			except asyncio.TimeoutError:
				await ctx.send('Info select timed out')
				return None
			else:
				if confirm.content.lower() == "cancel":
					await ctx.send('Selection canceled.')
					return None
				else:
					topic_to_send = search_results[int(confirm.content) - 1][0]
					subtopic_to_send = search_results[int(confirm.content) - 1][1]
					infoEmbed = discord.Embed(title = f"`{topic_to_send} : {subtopic_to_send}`", description = self.info_dict[topic_to_send][subtopic_to_send], color=0xffb6c1)
					return infoEmbed


	@commands.command()
	async def info(self, ctx, topic :  typing.Optional[str],*, subtopic : typing.Optional[str]):
		topickey = None
		subtopickey = None
		if topic:
			topickey = self.lowercase_keys_get(self.info_dict, topic)
		if topickey and subtopic:
			subtopickey = self.lowercase_keys_get(self.info_dict[topickey], subtopic)

		if topic and topickey and (not subtopic or not subtopickey):
			subtopics_list = []
			topicinfo = ""
			for st in self.info_dict[topickey].keys():
				if st.lower() != topickey.lower():
					subtopics_list.append(st)
				else:
					topicinfo = self.info_dict[topickey][st]
			if len(subtopics_list) > 0:
				subtopics_list.sort(key=str.lower)
				allinfo_str = topicinfo+"\n\n**Subtopics**\n"+"```\n"+"\n".join(subtopics_list)+"\n```"+f"Use `~info {topic} <subtopic>` to learn more about a subtopic."
			else:
				allinfo_str = topicinfo
			infoEmbed = discord.Embed(title=f"`{topickey}`", description =allinfo_str, color=0xffb6c1)
			usemessage = f"Info was used for topic `{topickey}`"
		elif topic and topickey and subtopic and subtopickey:
			infoEmbed = discord.Embed(title = f"`{topickey} : {subtopickey}`", description = self.info_dict[topickey][subtopickey], color=0xffb6c1)

			usemessage = f"Info was used for {subtopickey} in {topic}"

		elif (topic and not topickey) or (subtopic and not subtopickey):
			if subtopic:
				infoEmbed = await self.search_info(ctx, topic, subtopic)
			else:
				infoEmbed = await self.search_info(ctx, topic)
			
			if not infoEmbed:
				topiclist = list(self.info_dict.keys())
				topiclist.sort(key=str.lower)
				topiclist_str = '```\n'+'\n'.join(topiclist)+'\n```'+'Use `~info <topic>` to see information and subtopics.'
				infoEmbed = discord.Embed(title = "Topics", description = topiclist_str, color=0xffb6c1)
				usemessage = "Info was used."
		else:

			topiclist = list(self.info_dict.keys())
			topiclist.sort(key=str.lower)
			topiclist_str = '```\n'+'\n'.join(topiclist)+'\n```'+'Use `~info <topic>` to see information and subtopics.'
			infoEmbed = discord.Embed(title = "Topics", description = topiclist_str, color=0xffb6c1)
			usemessage = "Info was used."

		await ctx.send(embed=infoEmbed)
		testserver = self.bot.get_guild(622553382279708672)
		infotrackchannel = testserver.get_channel(713113119861375007)
		#await infotrackchannel.send(usemessage)

	@commands.group()
	async def editinfo(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.send('Improper editinfo command.')

	@editinfo.command()
	async def addtopic(self, ctx, topic : str):
		if topic in self.info_dict:
			await ctx.send("This topic was already added.")
		else:
			self.info_dict[topic] = {}
			self.save_json_dict(self.info_dict)
			await ctx.send('Topic added.')

	@editinfo.command()
	async def removetopic(self, ctx, topic : str):

		if topic in self.info_dict:
			await ctx.send(f'Are you sure you want to delete `{topic}` from `info`?')
			def delete_response(m):
				return m.author == ctx.author and m.channel == ctx.channel and (m.content.lower() == "yes" or m.content.lower() == "no")
			try:
				response = await self.bot.wait_for('message', check = delete_response, timeout = 120.0)
			except asyncio.TimeoutError:
				await ctx.send('Response timed out.')
			else:
				if response.content.lower() == "yes":
					del self.info_dict[topic]
					self.save_json_dict(self.info_dict)
					await ctx.send(f'`{topic}` deleted.')
				else:
					await ctx.send(f'Deletion canceled')
		else:
			await ctx.send('This is not a topic in `info`.')

	@editinfo.command()
	async def addsubtopic(self, ctx, topic: str, subtopic : str):
		if topic in self.info_dict:
			if subtopic in self.info_dict[topic]:
				await ctx.send(f'**Warning: This subtopic already exists and this command will overwrite it.** \n \nInput the information for `{subtopic}` below or type `cancel` to leave this menu.')
			else:
				await ctx.send(f'Input the information for `{subtopic}` below or type `cancel` to leave this menu.')

			def info_response(m):
				return m.author == ctx.author and m.channel == ctx.channel
			try:
				response = await self.bot.wait_for('message', check = info_response, timeout = 120.0)
			except asyncio.TimeoutError:
				await ctx.send('Response timed out.')
			else:
				if response.content.lower() == "cancel":
					await ctx.send('Command canceled')
				else:
					self.info_dict[topic][subtopic] = response.content
					await ctx.send(f'`{subtopic}` has been added.')
					self.save_json_dict(self.info_dict)
		else:
			await ctx.send("This is not a topic in `info`.")
	@editinfo.command()
	async def removesubtopic(self, ctx, topic : str, subtopic : str):
		if topic in self.info_dict:
			if subtopic in self.info_dict[topic]:
				await ctx.send(f'Are you sure you want to delete `{subtopic}`?')
				def delete_response(m):
					return m.author == ctx.author and m.channel == ctx.channel and (m.content.lower() == "yes" or m.content.lower() == "no")
				try:
					response = await self.bot.wait_for('message', check = delete_response, timeout = 120.0)
				except asyncio.TimeoutError:
					await ctx.send('Response timed out.')
				else:
					if response.content.lower() == "yes":
						del self.info_dict[topic][subtopic]
						self.save_json_dict(self.info_dict)
						await ctx.send(f'`{subtopic}` deleted from {topic}.')
					else:
						await ctx.send(f'Deletion canceled')
			else:
				await ctx.send(f'This is not a subtopic under `{topic}`.')
		else:
			await ctx.send('This is not a topic in `info`.')

	@commands.command()
	@is_mod()
	async def sendinfo(self, ctx, member : SmartMember, topic : str,*, subtopic : typing.Optional[str]):
		topickey = None
		subtopickey = None
		if topic:
			topickey = self.lowercase_keys_get(self.info_dict, topic)
		if topickey and subtopic:
			subtopickey = self.lowercase_keys_get(self.info_dict[topickey], subtopic)

		if topic and topickey and (not subtopic or not subtopickey):
			subtopics_list = []
			topicinfo = ""
			for st in self.info_dict[topickey].keys():
				if st.lower() != topickey.lower():
					subtopics_list.append(st)
				else:
					topicinfo = self.info_dict[topickey][st]
			if len(subtopics_list) > 0:
				allinfo_str = topicinfo+"\n\n**Subtopics**\n"+"```\n"+"\n".join(subtopics_list)+"\n```"+"Use `~info <topic> <subtopic>` to learn more about a subtopic."
			else:
				allinfo_str = topicinfo
			infoEmbed = discord.Embed(title=topic, description =allinfo_str, color=0xffb6c1)
			if topickey == "Reporting":
				infoEmbed.set_image(url="https://i.imgur.com/6OD4GWr.png")
			await member.send(embed=infoEmbed)
			await ctx.send(f'Sent info about `{topickey}` to {member}')

		elif topic and topickey and subtopic and subtopickey:
			infoEmbed = discord.Embed(title = f"`{subtopic}` in `{topic}`", description = self.info_dict[topickey][subtopickey], color=0xffb6c1)
			await member.send(embed=infoEmbed)
			await ctx.send(f'Sent info about `{subtopickey}` in `{topickey}` to {member}')

		else:
			await ctx.send('Topic not found.')

	async def cog_command_error(self, ctx, error):
		print(error)
		await ctx.send(f'Error: {error}')
