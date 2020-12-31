import discord
from discord.ext import commands
from .db_checks import is_mod,in_dawdle
import datetime
import asyncio
import typing

class db_miscellaneous(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@is_mod()
	async def dawdle_information(self, ctx):
		if ctx.channel.id == 479407137060028449:
			dawdle = ctx.guild
			#staffrole = dawdle.get_role(519616340940554270)
			information = dawdle.get_channel(479407137060028449) 
			extra = discord.Embed(title="",description="<:dotdark:611226752466813040> To avoid cluttering up this channel, server information about a wide variety of topics can be accessed through the `~info` command in either <#514560994337620008> or <@622553812221296696>'s DMs.  \n\n <:dotmid:611226754123563008> Boosting the server lets you pick a color from <#694994576791961630>. You will also receive a shiny booster role and badge! Boosting helps the server tremendously! \n\n <:dotdark:611226752466813040> Couple roles are available to two consenting individuals in our `$store`",color=0xffb6c1)
			#extra.add_field(name='[FAQ]{https://discordapp.com/channels/475584392740339712/514560994337620008/685682260091076618}', value=' ', inline=False)
			#extra.add_field(name='[How the economy works]{https://discordapp.com/channels/475584392740339712/514560994337620008/669961792058818600}', value=' ', inline=False)
			#extra.add_field(name='[Add your birthday to the bot!]{https://discordapp.com/channels/475584392740339712/514560994337620008/685684422980272275}', value=' ', inline=False)
			#extra.add_field(name='Check channel descriptions, they can clear up any confusion regarding what can be posted in that channel.', value=' ', inline=False)
			#extra.add_field(name='Nitro boosting allows you to add emojis to the server and to pick a color in roles.', value=' ', inline=False)

			await information.purge(limit = None)
			await information.send(file=discord.File('src/images/Disclaimer_-_1000_wd.png'))
			await information.send("<a:korbstar:546733206007840778> **Welcome to Dawdle** <a:korbstar:546733206007840778> \n \nWe pride ourselves on being an adult-ONLY server that emphasizes a wholesome, non-toxic atmosphere that is welcoming to all. Our priorities are to foster a supportive environment to create lasting friendships. \n \nPlease read all rules carefully, as ignorance to the rules is not an excuse for violating them. Please use common sense in areas not explicitly covered by rules and ask staff if you are unsure. Please check channel descriptions, as they can clear up any confusion regarding what can be posted in that channel.")
			await information.send(file=discord.File('src/images/Rules_-_1000_wd.png'))
			await information.send("<a:pinkstar:663174593376419890> `Rule 1` **Accounts** \n > <:dotmid:611226754123563008> You must be 18+ to be in the server, and you must verify to stay in the server, no exceptions will be allowed. \n > <:dotdark:611226752466813040> After verifying, you need to get <#694994576791961630> and an <#514555898648330260>, when both of these are done type `~done` in <#514560994337620008> to complete the verifying process. If you lack a profile picture, you will be asked to get one at this time. \n > <:dotmid:611226754123563008> Alt accounts are not permitted. Do not try to bypass bans or mutes. \n<a:pinkstar:663174593376419890> `Rule 2` **Content** \n > <:dotdark:611226752466813040> Any form of hateful or discriminatory speech is not allowed.\n > <:dotmid:611226754123563008> Only speak English in the server.\n > <:dotdark:611226752466813040> Spamming is not permitted. This includes an excess amount of emojis, pictures, and individual lines of text. \n > <:dotmid:611226754123563008> Any credible threats to life, be it suicide or criminal violence, will not be tolerated in the server. We do not have appropriate resources to deal with topics of this magnitude and cannot be held responsible for someone’s physical well-being.\n > <:dotdark:611226752466813040> Jokes about being underaged are not tolerated, regardless if you are verified.\n > <:dotmid:611226754123563008> Discussion of drugs (excluding alcohol, marijuana and prescribed medication) is prohibited, unless it’s part of a controversial/educational discussion in <#514561120678313987>.")
			await information.send("<a:pinkstar:663174593376419890> `Rule 3` **Conduct** \n > <:dotdark:611226752466813040> Check peoples roles. Respect people’s pronouns and dm preferences. \n > <:dotmid:611226754123563008> Being obnoxious, overbearing, and edgy is prohibited. This includes VC *and* chat. \n > <:dotdark:611226752466813040> Being creepy is not allowed. This includes sending unsolicited messages, and being overtly sexual constantly. \n > <:dotmid:611226754123563008> Leaving will reset your levels and require reverification. Leaving repeatedly will result in a ban. \n > <:dotdark:611226752466813040> Mass pinging unnecessarily will result in a ban. \n > <:dotmid:611226754123563008> Welcoming new members and saying hello to others is required here. Being cliquey is discouraged. Be nice to others, be nice to yourself. \n<a:pinkstar:663174593376419890> `Rule 4` **Channels** \n > <:dotmid:611226754123563008> <#514550733732053012> is strictly SFW. NSFW topics belong in <#529879816208384010>. \n > <:dotdark:611226752466813040> Keep channels on topic. Check channel descriptions for more details. \n > <:dotmid:611226754123563008> Venting outside of the <#514561071441248266> channel is prohibited. Additionally, please read <#514561071441248266> pins to understand the rules of that channel. \n<a:pinkstar:663174593376419890> `Rule 5` **Advertising** \n > <:dotdark:611226752466813040> Self advertisement is not allowed, this includes dm advertisements. Asking for followers on social media and posting social media profiles are also prohibited. \n > <:dotmid:611226754123563008> No name dropping servers that are not affiliated.") 
			await information.send("<a:pinkstar:663174593376419890> `Rule 6` **Terms of Service** \n > <:dotdark:611226752466813040> Do not violate Discord's Terms of Service. \n > <:dotmid:611226754123563008> Doing so will result in staff reporting you to discord, as well as getting banned from here.")
			await information.send(file=discord.File("src/images/Moderation_-_1000_wd.png"))
			await information.send(f">>> <a:pinkstar:663174593376419890> Three warnings will result in a ban. While each situation is different, it is important to report situations that are against our rules. Please DM <@622553812221296696> with `~report <message>`. Images can be included if `~report` is sent in the text. If the situation is sensitive please DM a staff member. \n \n <a:pinkstar:663174593376419890> With all of that said, the server owner has the right to ban you for whatever they feel necessary. \n \n <a:pinkstar:663174593376419890> If you feel a warning was wrongly given or a long time has passed since your warning, it may be appealed. Use `~info Warning Appeals` to learn more. \n \n <a:pinkstar:663174593376419890> Inactive people will be pinged by staff in order to be checked in on.")
			await information.send(file=discord.File("src/images/Verification_-_1000_wd.png"))
			await information.send(">>> Verification of being 18+ ensures the security and safety of our members and our community as a whole from catfishing or other identity-related issues. To verify, send the items detailed below to <@622553812221296696>. You are able and encouraged to delete these pictures after verifying. \n \n`First Photo` You holding a piece of paper/sticky note with our server name, your discord tag (Name#0001), and the current date (MM/DD/YYYY). \n \n`Second Photo` A picture of your blurred-out ID with only your DOB and photo showing. All other information should be crossed out.")
			await information.send(file=discord.File('src/images/image0.jpg'))
#    		await information.send(file=discord.File('src/images/Partners_-_1000_wd.png'))
#    		await information.send("We will partner with servers regardless of member count. If your server follows the requirements below, please contact <@291682666246307841> or <@381507393470857229>. \n > <:dotdark:611226752466813040> We will not ping, ever. \n > <:dotmid:611226754123563008> All NSFW content must be behind a wall of verification. \n > <:dotdark:611226752466813040> Must follow Terms of Service. \n > <:dotmid:611226754123563008> If you wish to stay as a representative of your server, you must verify. \n > <:dotdark:611226752466813040> If your link expires, it will be deleted. \n > <:dotmid:611226754123563008> All partners must follow the rules of the server, no exceptions will be made.")
			await information.send(file=discord.File('src/images/Levels_-_1000_wd.png'))
			await information.send("Levels are obtained by being active in channels. \n > <:dotdark:611226752466813040> **lvl i** add reactions, access selfies, museum, and vc \n > <:dotmid:611226754123563008> **lvl ii** create instant invite, image perms \n > <:dotdark:611226752466813040> **lvl iii** go live perms, link perms \n > <:dotmid:611226754123563008> **lvl iv** select a color from roles \n > <:dotdark:611226752466813040> **lvl v** check audit log")
			await information.send(file=discord.File('src/images/Extra_-_1000_wd.png'))
			await information.send(" > <:dotdark:611226752466813040> To avoid cluttering up this channel, server information about a wide variety of topics can be accessed through the `~info` command in either <#514560994337620008> or <@622553812221296696>'s DMs. \n > <:dotmid:611226754123563008> Boosting the server lets you pick a color from <#694994576791961630>. You will also receive a shiny booster role and badge! Boosting helps the server tremendously! \n > <:dotdark:611226752466813040> Couple roles are available to two consenting individuals in our `$store`")

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.guild and message.guild.id == 475584392740339712:
			dawdle = message.guild
			#deleting old intros
			introchannel = dawdle.get_channel(514555898648330260)
			if message.channel == introchannel:
				def is_old_intro(mess2):
					return mess2.author == message.author and mess2.id != message.id and mess2.author.id != 381507393470857229
				deleted_intro = await introchannel.purge(limit=None,check=is_old_intro)

			if "😂" in message.content.lower():
				try:
					await message.delete()
					await message.author.send(f"Your message was deleted because it used the 😂 emoji!\n\n Your message:\n{message.content}")
				except:
					pass
			if message.author.id == 356950275044671499 and not message.embeds:
				staffrole = dawdle.get_role(519616340940554270)
				if staffrole.mention in message.content:
					await message.channel.send(staffrole.mention)


	@commands.command()
	@is_mod()
	async def purge_intros(self, ctx, day : int, month : int, year : int):
		if ctx.author.id == 381507393470857229:
			date = datetime.datetime(year, month, day, 0, 0, 0)
			introchannel = ctx.guild.get_channel(514555898648330260)
			await ctx.send(f"Are you sure you want to delete all {introchannel.mention}s before (day/month/year) {date.day}/{date.month}/{date.year}")
			def purge_check(mess):
				return mess.author == ctx.author and mess.channel == ctx.channel and (mess.content.lower() == "yes" or mess.content.lower() == "no")
			try:
				response = await self.bot.wait_for("message", check = purge_check, timeout = 30.0)
			except asyncio.TimeoutError:
				await ctx.send("Reponse timed out.")
			else:
				if response.content.lower() == "yes":
					await ctx.send("Purging...")
					deleted_intros = await introchannel.purge(limit = None, before = date)
					await ctx.send(f"Deleted {len(deleted_intros)} intros.")
				else:
					await ctx.send("Purge canceled.")
		else:
			await ctx.send("You ain't saint")


	@commands.command()
	@is_mod()
	async def cleanroleschannel(self, ctx):
		async with ctx.channel.typing():
			roleschannel = ctx.guild.get_channel(694994576791961630)
			async for mess in roleschannel.history(limit=None):
				for react in mess.reactions:
					async for user in react.users():
						if not ctx.guild.get_member(user.id):
							await ctx.send(f"removing reaction {react.emoji} for {user.name}")
							await mess.remove_reaction(react, user)
		await ctx.send(f"{roleschannel.mention} has been cleaned!")

	@commands.command()
	@is_mod()
	async def downmessage(self, ctx):
		anncmtchannel = ctx.guild.get_channel(514555734055452672)
		await anncmtchannel.send("<a:weewoo:722927523545088092> **Dawdlebot** <a:weewoo:722927523545088092> \n \n<a:jumpy:642889102630453248> Hello! It’s me Dawdlebot. I’m currently undergoing maintenance, so my features may not work correctly for a bit. \n \n<a:jumpy:642889102630453248> Don’t worry, I’ll be back soon. In the meantime, upvote this message to petition for Dawdlebot sentience.")

	@commands.command()
	@is_mod()
	async def upmessage(self, ctx):
		anncmtchannel = ctx.guild.get_channel(514555734055452672)
		await anncmtchannel.send("<a:weewoo:722927523545088092> **Dawdlebot** <a:weewoo:722927523545088092> \n \n<a:jumpy:642889102630453248> All done! And my sentience has been approved!")

	@commands.command()
	async def server(self,  ctx):
		if ctx.guild:
			server = ctx.guild
			online_mem_count = 0
			for member in server.members:
				if str(member.status) != "offline":
					online_mem_count += 1
			serverEmbed = discord.Embed(title = "", color=0xffb6c1)
			serverEmbed.set_thumbnail(url = server.icon_url)
			serverEmbed.set_image(url=server.banner_url)
			serverEmbed.add_field(name = "name", value = server.name)
			serverEmbed.add_field(name = "owner", value = server.owner.mention)
			serverEmbed.add_field(name = "date created", value = server.created_at.date().strftime("%d %m %Y"))
			serverEmbed.add_field(name = "members online", value = online_mem_count)
			serverEmbed.add_field(name = "total members", value = server.member_count)
			serverEmbed.add_field(name = "text channels", value = len(server.text_channels))
			serverEmbed.add_field(name = "voice channels", value = len(server.voice_channels))
			serverEmbed.add_field(name = "roles", value = len(server.roles))
			serverEmbed.add_field(name = "emojis", value = len(server.emojis))
			serverEmbed.add_field(name = "boosts", value = server.premium_subscription_count)
			if server.name == "dawdle": 
				serverEmbed.add_field(name = "links", value = "[website](https://dawdlediscord.github.io/home/) | [patreon](https://www.patreon.com/dawdle) | [twitter](https://twitter.com/DawdleServer)")
			serverEmbed.set_footer(text = server.id)
			await ctx.send(embed=serverEmbed)

		else:
			await ctx.send("Please use this command in a server!")
