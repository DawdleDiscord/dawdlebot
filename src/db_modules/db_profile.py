import discord
from discord.ext import commands
from .db_converters import SmartMember,SmartRole
from .db_checks import is_mod,in_dawdle
import json,typing
import asyncio

class db_profile(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		with open("src/data/profile.json", "r") as json_file:
			try:
				self.profile_dict = json.load(json_file)
			except json.decoder.JSONDecodeError:
				print ("Currently no profiles!")
				self.profile_dict = {}

	@commands.command()
	@in_dawdle()
	async def profile(self, ctx, member : typing.Optional[SmartMember]):
		if member is None:
			member = ctx.author
		profileEmbed = discord.Embed(title = member.name, color = 0xffb6c1)
		profileEmbed.set_thumbnail(url=member.avatar_url)
		profileEmbed.add_field(name = "name", value = member.mention)
		introchannel = ctx.guild.get_channel(514555898648330260)
		foundIntro = False
		async for mess in introchannel.history(limit=None):
			if mess.author.id == member.id:
				intro_link =  mess.jump_url
				foundIntro = True
				break
		if not str(member.id) in self.profile_dict.keys():
			self.profile_dict[str(member.id)] = {"extra" : "", "badges" : "", "banner" : ""}
		elif not "banner" in self.profile_dict[str(member.id)].keys():
			self.profile_dict[str(member.id)]["banner"] = ""
		if foundIntro:
			profileEmbed.add_field(name = "intro", value = f"[Jump!]({intro_link})")
		if str(member.id) in self.profile_dict.keys() and self.profile_dict[str(member.id)]["badges"]:
			badge_str = ""
			for badge in self.profile_dict[str(member.id)]["badges"]:
				badge_str += badge
			profileEmbed.add_field(name = "badges", value = badge_str)
		profileEmbed.add_field(name = "account made", value = member.created_at.date().strftime("%d %m %Y"))
		profileEmbed.add_field(name = "joined server", value = member.joined_at.date().strftime("%d %m %Y"))
		if str(member.id) in self.profile_dict.keys() and self.profile_dict[str(member.id)]["extra"]:
			profileEmbed.add_field(name = "about", value = self.profile_dict[str(member.id)]["extra"], inline = False)
		if str(member.id) in self.profile_dict.keys() and self.profile_dict[str(member.id)]["banner"]:
			profileEmbed.set_image(url = self.profile_dict[str(member.id)]["banner"])

		await ctx.send(embed=profileEmbed)
	@profile.error
	async def profile_error(self, ctx, error):	
		await ctx.send("The banner url for this profile is invalid. Use `editbanner` to fix it and be sure to include the `https://`")

	@commands.command()
	@is_mod()
	async def givebadge(self,ctx,  member_or_role : typing.Union[SmartMember, SmartRole], *emoji : str):
	
		if isinstance(member_or_role, discord.Member):
			mem_list = [member_or_role]
		else:
			mem_list = member_or_role.members
		spamchannel = ctx.guild.get_channel(514560994337620008)
		for member in mem_list:
			if not str(member.id) in self.profile_dict.keys():
				self.profile_dict[str(member.id)] = {"extra" : "", "badges" : ""}
			if not self.profile_dict[str(member.id)]["badges"]:
				badge_list = []
			else:
				badge_list =  list(self.profile_dict[str(member.id)]["badges"])
			emoj_list = list(emoji)
			for badg in badge_list:
				for emoj in emoji:
					if badg == emoj:
						emoj_list.remove(emoj)
			if emoj_list:
				emoj_str = "".join(emoj_list)
				await ctx.send(f"Gave {member} the following badge(s): {emoj_str}")
				await spamchannel.send(f"{member.mention} just received the {emoj_str} badge(s)!")
			badge_list += emoj_list
			self.profile_dict[str(member.id)]["badges"] = badge_list
		with open("src/data/profile.json", "w") as json_file:
			json.dump(self.profile_dict, json_file)
		await ctx.send(f"Done giving out badges to `{member_or_role}`.")

	@commands.command()
	@is_mod()
	async def takebadge(self, ctx, member_or_role : typing.Union[SmartMember, SmartRole], *emoji : str):
		if isinstance(member_or_role, discord.Member):
			mem_list = [member_or_role]
		else:
			mem_list = member_or_role.members
		for member in mem_list:
			if str(member.id) in self.profile_dict.keys() and self.profile_dict[str(member.id)]["badges"]:
				badge_list = self.profile_dict[str(member.id)]["badges"]
				no_list = []
				for em in emoji:
					if em in badge_list:
						badge_list.remove(em)
					else:
						no_list.append(em)
				self.profile_dict[str(member.id)]["badges"] = badge_list
				with open("src/data/profile.json", "w") as json_file:
					json.dump(self.profile_dict, json_file)
				emoj_str = "".join(emoji)
				if no_list:
					no_str = "".join(no_list)
					to_send = f"Took {emoj_str} from {member} except for {no_str} because they did not have them."
				else:
					to_send = f"Took {emoj_str} from {member}"
			else:
				to_send = f"{member} does not have any badges!"
			await ctx.send(to_send)
	@commands.command()
	@is_mod()
	async def cleanbadges(self, ctx, member_or_role : typing.Union[SmartMember, SmartRole]):
		if isinstance(member_or_role, discord.Member):
			mem_list = [member_or_role]
		else:
			mem_list = member_or_role.members
		for member in mem_list:
			if str(member.id) in self.profile_dict.keys() and "badges" in self.profile_dict[str(member.id)] and self.profile_dict[str(member.id)]["badges"]:
				for badge in self.profile_dict[str(member.id)]["badges"]:
					foundBadge = False
					for emoj in ctx.guild.emojis:
						if badge == str(emoj):
							foundBadge = True
							break
					if not foundBadge:
						testserver = self.bot.get_guild(622553382279708672)
						for emoj in testserver.emojis:
							if badge == str(emoj):
								foundBadge = True
								break
					if not foundBadge:
						self.profile_dict[str(member.id)]["badges"].remove(badge)
						await ctx.send(f"Removed bad badge {badge} from {member}")
		with open("src/data/profile.json", "w") as json_file:
				json.dump(self.profile_dict, json_file)

	@commands.command()
	@is_mod()
	async def cleanprofiles(self, ctx):
		to_delete = []
		for mem_id in self.profile_dict.keys():
			if not ctx.guild.get_member(int(mem_id)):
				to_delete.append(mem_id)
		with open("src/data/profile.json", "w") as json_file:
				json.dump(self.profile_dict, json_file)
		if to_delete:
			for mem_id in to_delete:
				del self.profile_dict[mem_id]
		await ctx.send(f"Cleaned {len(to_delete)} profiles of members who left")

	@commands.command()
	@in_dawdle()
	async def editprofile(self, ctx):
		extraresp = await ctx.send("Enter what you would like to show for the **about** section of your profile or type `cancel`!")
		def check_response(message):
			return message.author == ctx.author and message.channel == ctx.channel
		try:
			response = await self.bot.wait_for("message", check = check_response, timeout = 60.0)
		except asyncio.TimeoutError:
			await extraresp.edit(content="Timed out.", supress = True)
		else:
			if response.content.lower() == "cancel":
				await extraresp.edit(content="Profile editing canceled.")
			else:
				if not str(ctx.author.id) in self.profile_dict.keys():
					self.profile_dict[str(ctx.author.id)] = {"extra" : "", "badges" : "", "banner" : ""}
				self.profile_dict[str(ctx.author.id)]["extra"] = response.content
				with open("src/data/profile.json", "w") as json_file:
					json.dump(self.profile_dict, json_file)
					await extraresp.edit(content="Profile edited! Use `~profile` to see it!")
	@commands.command()
	@in_dawdle()
	async def editbanner(self, ctx):
		bannerresp = await ctx.send("Enter the url for the banner you would like to show with your profile, type `none` to remove your current banner, or type `cancel`.")
		def check_response(message):
			return message.author == ctx.author and message.channel == ctx.channel
		try:
			response = await self.bot.wait_for("message", check = check_response, timeout = 60.0)
		except asyncio.TimeoutError:
			await bannerresp.edit(content="Timed out.", supress = True)
		else:
			if response.content.lower() == "cancel":
				await bannerresp.edit(content="Banner editing canceled.")
			elif response.content.lower() == "none":
				if not str(ctx.author.id) in self.profile_dict.keys():
					self.profile_dict[str(ctx.author.id)] = {"extra" : "", "badges" : "", "banner" : ""}
				self.profile_dict[str(ctx.author.id)]["banner"] = ""
				with open("src/data/profile.json", "w") as json_file:
					json.dump(self.profile_dict, json_file)
					await bannerresp.edit(content="Banner deleted.")
			elif response.content.lower()[0:4] != "http":
				await bannerresp.edit(content="Your url needs to start with `http` or `https`, try again.")
			else:
				if not str(ctx.author.id) in self.profile_dict.keys():
					self.profile_dict[str(ctx.author.id)] = {"extra" : "", "badges" : "", "banner" : ""}
				self.profile_dict[str(ctx.author.id)]["banner"] = response.content
				with open("src/data/profile.json", "w") as json_file:
					json.dump(self.profile_dict, json_file)
					await bannerresp.edit(content="Banner edited! Use `~profile` to see it!")

