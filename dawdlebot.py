import discord
import datetime
import asyncio
import math
from discord.ext.commands import Bot
from discord.ext import commands
import gn_mess_dict
import random
from dawdle_vars import dawdletoken

bot = Bot(command_prefix = '/')
#List for times
userAndDate = {}
#Time at start up.
botStartup = datetime.datetime.now()
token = dawdletoken
GUILD1 = 'dawdle'
GUILD2 = 'amertestserver'

def get_server(guilds,server):
	for guild in guilds:
		if guild.name == server:
			return guild
			break


@bot.event
async def on_ready():
	dawdle = get_server(bot.guilds,'dawdle')
	print(f'{bot.user} has connected to Discord!', f'{dawdle.name}(id: {dawdle.id})')
	game = discord.Game("say 'nini dawdle' for a goodnight message!")
	await bot.change_presence(activity=game)
	ventInstr = '<a:weewoo:598696151759192085> **Anonymous Venting Rules** <a:weewoo:598696151759192085> \n \n <a:tinyheart:546404868529717270> 1. Any vent about another person in the server will be immediately denied. \n \n <a:tinyheart:546404868529717270> 2. Overtly sexual or explicit vents are not allowed. \n \n <a:tinyheart:546404868529717270> 3. __Dawdle rules apply__. Any suicide/self-harm references will be denied. \n \n <a:tinyheart:546404868529717270> 4. If you wish to vent and do not want any advice or responses write NA at the end of your vent. \n \n <a:tinyheart:546404868529717270> 5. While it is anonymous, staff can see user IDs and will warn/ban any user when necessary. \n \n <a:weewoo:598696151759192085> **Instructions on how to use** <a:weewoo:598696151759192085> \n \n <a:tinyheart:546404868529717270>  DM <@622553812221296696> using this format: \n >>> `/vent "Message"` \n \n The quotes are important! \n \n `example:` /vent “Hello I am venting”'


@bot.event
async def on_raw_reaction_add(payload):
	dawdle = get_server(bot.guilds,'dawdle')
	verifchannel = dawdle.get_channel(623016717429374986)
	userR = bot.get_user(payload.user_id)	
	verifEmoj = payload.emoji
	channelR = dawdle.get_channel(payload.channel_id)
#verification code	
	if channelR == verifchannel and not userR.bot:
		verifMess = await verifchannel.fetch_message(payload.message_id)
		userM = verifMess.mentions[0]
		verifrole = dawdle.get_role(481148097960083471)
		unverifrole = dawdle.get_role(479410607821684757)
		dotRole = dawdle.get_role(587397534469718022)
		check_emoj = await dawdle.fetch_emoji(609771973341610033)
		cross_emoj = await dawdle.fetch_emoji(609771973102534687)
		date_emoj = await dawdle.fetch_emoji(630533105903730689)
		dawd_emoj = await dawdle.fetch_emoji(586767353740656656)
		name_emoj = await dawdle.fetch_emoji(598695827891945472)	

		for vr in verifMess.reactions:
			if vr.emoji == check_emoj and vr.count == 2 and verifMess.mentions:
				
				userM = verifMess.mentions[0]
				await userM.add_roles(verifrole)
				await userM.add_roles(dotRole)
				await userM.remove_roles(unverifrole)
				await userM.send("Thank you for verifying! You’ve successfully completed this process, you are now able to see the majority of the server. Please proceed to get some <#527307900662710297> and to post an <#514555898648330260>! No formats are necessary for introductions, just a little snippet will do. When you are done with both, type \"/done\" (without the quotes) in <#514560994337620008>.")

			elif verifEmoj == cross_emoj and vr.count == 2 and verifMess.mentions:
				
				await userM.send("Sorry, but the pictures you provided do not follow our outlines as described in <#479407137060028449>. Please review and try again!")

			elif verifEmoj == date_emoj and vr.count == 2 and verifMess.mentions:
				
				await userM.send("You’re missing today’s date on the selfie picture!")

			elif verifEmoj == dawd_emoj and vr.count == 2 and verifMess.mentions:

				await userM.send("You're missing the server name on the selfie picture!")
			
			elif verifEmoj == name_emoj and vr.count == 2 and verifMess.mentions:

				await userM.send("You're missing your discord name on the selfie picture!")

#pin code
	pinEmoj = await dawdle.fetch_emoji(491736157844144129)
	srcChannel = dawdle.get_channel(payload.channel_id)
	pinchannel = dawdle.get_channel(623016818709233678)
	korbIndex = 3

	if payload.emoji == pinEmoj and srcChannel:
		srcMess = await srcChannel.fetch_message(payload.message_id)
		pinnedMess = srcMess
		if payload.user_id == srcMess.author.id:
			await srcMess.remove_reaction(pinEmoj, srcMess.author)
		else:
			for r in srcMess.reactions:
				if r.emoji == pinEmoj and r.count >= 5:
					pinned = False
					async for pins in pinchannel.history(limit=100):
						if pins.embeds[0].footer.text == str(srcMess.id):
							pinned = True
							pinnedMess = pins
							break
					if not pinned:
						embedmess = discord.Embed(title="",value="",color=0xffb6c1,timestamp = datetime.datetime.utcnow())
						embedmess.set_thumbnail(url=r.message.author.avatar_url)
#						embedmess.set_author(name=f'{reaction.message.author}',icon_url = reaction.message.author.avatar_url)
						embedmess.add_field(name='Author', value = r.message.author.mention, inline = False)
						embedmess.add_field(name='Channel', value=r.message.channel.mention, inline = False)
						if r.message.content:
							embedmess.add_field(name='Content', value = r.message.content, inline = False)
						embedmess.add_field(name=f'{r.count} {r.emoji}',value=f'[Jump!]({r.message.jump_url})', inline = False)
						embedmess.set_footer(text=str(r.message.id))
						if r.message.attachments:
							embedmess.set_image(url=r.message.attachments[0].url)
						await pinchannel.send(embed=embedmess)
					else:
						editEmbedMess = pinnedMess.embeds[0]
						if editEmbedMess.fields[2].name != "Content":
							korbIndex = 2
						editEmbedMess.set_field_at(index=korbIndex, name=f'{r.count} {r.emoji}',value=f'[Jump!]({r.message.jump_url})')
						await pinnedMess.edit(embed = editEmbedMess,supress=False)
					break
	botChannel = dawdle.get_channel(654787316665286714)
	ventChannel = dawdle.get_channel(514561071441248266)
	if srcChannel == botChannel:
		ventMess = await srcChannel.fetch_message(payload.message_id)
		if ventMess.embeds[0].title=='Vent' and (verifEmoj.id == 609771973341610033 or verifEmoj.id == 609771973102534687):
			for vr in ventMess.reactions:
				if vr.emoji == verifEmoj and vr.count == 2:
					if verifEmoj.id == 609771973341610033:
						embedVent = ventMess.embeds[0]
						embedVent.title = ''
						embedVent.set_footer(text='')
						await ventChannel.send(embed=embedVent)
					elif verifEmoj.id == 609771973102534687:
						ventMemb = await dawdle.fetch_member(ventMess.embeds[0].footer.text)
						await ventMemb.send('<a:weewoo:598696151759192085> **Anonymous Venting Rules** <a:weewoo:598696151759192085> \n \n <a:tinyheart:546404868529717270> 1. Any vent about another person in the server will be immediately denied. \n \n <a:tinyheart:546404868529717270> 2. Overtly sexual or explicit vents are not allowed. \n \n <a:tinyheart:546404868529717270> 3. __Dawdle rules apply__. Any suicide/self-harm references will be denied. \n \n <a:tinyheart:546404868529717270> 4. If you wish to vent and do not want any advice or responses write NA at the end of your vent. \n \n <a:tinyheart:546404868529717270> 5. While it is anonymous, staff can see user IDs and will warn/ban any user when necessary. \n \n <a:weewoo:598696151759192085> **Instructions on how to use** <a:weewoo:598696151759192085> \n \n <a:tinyheart:546404868529717270>  DM <@622553812221296696> using this format: \n >>> `/vent "Message"` \n \n The quotes are important! \n \n `example:` /vent “Hello I am venting”')

@bot.event
async def on_member_join(member):
	dawdle = get_server(bot.guilds,'dawdle')
	unverifrole = dawdle.get_role(479410607821684757)
	foyerchannel = dawdle.get_channel(514554494495752204)
	await foyerchannel.send(f'Welcome to dawdle, {member.mention}. Please read <#479407137060028449> to know how to access the rest of the server! Enjoy your stay.')
	await member.add_roles(unverifrole)
	try:
		await member.send(f'Hi {member.name}, welcome to Dawdle! We\'re so happy to have you! Please read <#479407137060028449> for details on how to get verified so that the rest of the server can be opened up to you.\n \nVerification is required to stay, but we understand if you can\'t do it right away. <#514550733732053012> is open for you to talk and say hi before you verify so you can meet some of the great folks that we have! \n \n**When you\'re ready to verify, please send your items to me (this bot) so that a member of staff can review it and you can access more of the server!**')
	except:
		pass



@bot.event
async def on_message(message):

	dawdle = get_server(bot.guilds,'dawdle')
	verifchannel = dawdle.get_channel(623016717429374986)
	unverifrole = dawdle.get_role(479410607821684757)
	staffrole = dawdle.get_role(519616340940554270)
	staffchannel = dawdle.get_channel(641796475470217264)
	#Get disboard bot user
	# bumpbot = dawdle.get_member(302050872383242240)
	# #Check if disboard sent the message
	# if(message.author.id == bumpbot.id):
	# 	#Grab the embed from the message if there is an embed
	# 	if(message.embeds):
	# 		disboardEmbed = message.embeds[0]
	# 		#Use the URL of the bump image to check if the bot had a successful bump.
	# 		imageURL = 'https://disboard.org/images/bot-command-image-bump.png'
	# 		if(disboardEmbed.image.url == imageURL):
	# 			#Get the message directly before the bump as it should be whoever bumped it
	# 			async for prevmessage in message.channel.history(limit=1, before=message.id):
	# 				#Check if the message is a bump command
	# 				if(prevmessage.content == '!d bump'):
	# 					#Check if whoever sent the message is staff or not
	# 					for r in prevmessage.author.roles:
	# 						if r != staffrole:
	# 							staffchannel.send(f'{prevmessage.author.mention} bumped the disboard bot')
	# 							#Do whatever here to alert staff that someone bumped that wasn't staff
					
			
	if dawdle.get_member(message.author.id):
		userM = dawdle.get_member(message.author.id)
		unverified = False
		check_emoj = await dawdle.fetch_emoji(609771973341610033)
		cross_emoj = await dawdle.fetch_emoji(609771973102534687)
		date_emoj = await dawdle.fetch_emoji(630533105903730689)
		dawd_emoj = await dawdle.fetch_emoji(586767353740656656)
		name_emoj = await dawdle.fetch_emoji(598695827891945472)	
		for r in userM.roles:
			if r == unverifrole:
				unverified = True
				break
		if not message.guild and not message.author.bot and unverified:
			if message.content:
				embedMess = discord.Embed(title='Message',description=f'{message.content}', color=0xffb6c1,timestamp = datetime.datetime.utcnow())
				embedMess.set_author(name=f'{message.author}',icon_url = message.author.avatar_url)
				embedMess.set_footer(text=f"ID: {message.author.id}")
				await verifchannel.send(embed=embedMess)
			for a in message.attachments:
				embedVar = discord.Embed(title='Verification', color=0xffb6c1,timestamp = datetime.datetime.utcnow())
				embedVar.set_author(name=f'{message.author}',icon_url = message.author.avatar_url)
				embedVar.set_image(url=a.url)
				embedVar.set_footer(text=f"ID: {message.author.id}")
				await verifchannel.send(embed=embedVar)
			if message.attachments:
				userM = message.author.mention
				sentMess = await verifchannel.send(f'{staffrole.mention}, verify {userM}?')
				await sentMess.add_reaction(check_emoj)
				await sentMess.add_reaction(cross_emoj)
				await sentMess.add_reaction(date_emoj)
				await sentMess.add_reaction(dawd_emoj)
				await sentMess.add_reaction(name_emoj)
				await message.author.send('Your message has been successfully submitted. Please wait patiently for a staff member to review your pictures.')
	
	#Hearting posts in intro, selfies, museum
	introchannel = dawdle.get_channel(514555898648330260)
	museumchannel = dawdle.get_channel(564613278874075166)
	selfieChannel = dawdle.get_channel(514556004822941696)
	fuzzieChannel = dawdle.get_channel(639698875346845696)
	if message.channel == introchannel:
		await message.add_reaction('❤')
		def is_old_intro(mess2):
			return mess2.author == message.author and mess2.id != message.id and mess2.author.id != 381507393470857229 
		deleted_intro = await introchannel.purge(limit=None,check=is_old_intro)
	if message.channel == museumchannel or message.channel == selfieChannel or message.channel == fuzzieChannel:
		await message.add_reaction('❤')

	#Goodnight messages

	if message.channel and ("nini dawdle" in message.content.lower()):
		await message.author.send(random.choice(gn_mess_dict.gn_mess['nini_mess']))

#	if message.channel == spamchannel and message.author == dbumpbot:
#		print(message.embeds[0].description)



	await bot.process_commands(message)

@bot.event
async def on_member_remove(member):
	dawdle = get_server(bot.guilds,'dawdle')
	foyerchannel = dawdle.get_channel(514554494495752204)
	introChannel = dawdle.get_channel(514555898648330260)
	verifrole = dawdle.get_role(481148097960083471)
	verified = False
	for role in member.roles:
		if role == verifrole:
			verified = True
			break
	if verified:
		def is_user(message):
			return message.author == member
		deleted = await introChannel.purge(limit=None,check=is_user)

	await foyerchannel.send(f'Bye {member.name}, you whore.')

# @bot.event
# async def on_member_ban(dawdle,member):
# 	foyerchannel = dawdle.get_channel(514554494495752204)
# 	introChannel = dawdle.get_channel(514555898648330260)
# 	verifrole = dawdle.get_role(481148097960083471)
# 	verified = False
# 	for role in member.roles:
# 		if role == verifrole:
# 			verified = True
# 			break
# 	if verified:
# 		def is_user(message):
# 			return message.author == member
# 		deleted = await introChannel.purge(limit=None,check=is_user)

# 	await foyerchannel.send(f'Bye {member.name}, you whore.')
	
	#VC Tracker
@bot.event
async def on_voice_state_update(member, before, after):
	dawdle = get_server(bot.guilds,'dawdle')
	global botStartup
	global userAndDate
	musicchannel = dawdle.get_channel(479408746955669524)
	afkchannel = dawdle.get_channel(533325041723506688)
	#Check if they joined a voice channel
	if before.channel is None and after.channel is not None and after.channel != musicchannel and after.channel != afkchannel:
		currentTime = datetime.datetime.now()
		#Set the time for when they joined
		userAndDate[member.id] = currentTime
	#Check if they left a voice channel
	elif (before.channel is not None and after.channel is None and before.channel != musicchannel and before.channel != afkchannel):
		#Set time for when they left
		currentTime = datetime.datetime.now()
		#Set the time for when they joined to bot startup in case of bot crashing, if they are in the list
		#Set the time for when they actually joined
		lastJoin = botStartup
		if member.id in userAndDate:
			lastJoin = userAndDate[member.id]
		#Math the fuck out of some time for easy time differentiating
		diff = currentTime - lastJoin
		#hours = math.floor(diff.seconds/3600)
		#minutes = math.floor((diff.seconds - hours * 3600)/60)
		#seconds = diff.seconds - hours * 3600 - minutes * 60
		minutes = math.floor(diff.seconds / 60)
		#Formatted string for minutes
		mt = "{} minutes".format(minutes)
		#If they've been in VC for more than 10 minutes send to staff
		if (minutes>=20 and userAndDate[member.id]):
			del userAndDate[member.id]
			botChannel = get_server(bot.guilds,'dawdle').get_channel(654787316665286714)
			noKoins = False
			async for mess in botChannel.history(limit=200):
				if mess.embeds and mess.embeds[0].title == "VC Koins" and mess.author.id == 622553812221296696:
					if  mess.embeds[0].footer.text == str(member.id) and (datetime.datetime.utcnow() - mess.embeds[0].timestamp).days < 1:
						noKoins = True
						break
			if not noKoins:
				voiceEmbed = discord.Embed(title= "VC Koins",description=f"{member.mention} was in VC for {mt}. Give them koins!",color=0xffb6c1,timestamp = datetime.datetime.utcnow())
				voiceEmbed.set_footer(text=f'{member.id}')
				await botChannel.send(embed=voiceEmbed)
		#If they haven't been in VC for 10 minutes just remove them from the list
		elif(minutes<20 and userAndDate[member.id]):
			del userAndDate[member.id]


@bot.command()
async def cleanmembers(ctx,arg):
	dawdle = get_server(bot.guilds,'dawdle')
	staffrole = dawdle.get_role(519616340940554270)
	saintrole = dawdle.get_role(490249474619211838)
	introChannel = dawdle.get_channel(514555898648330260)
	selfieChannel = dawdle.get_channel(514556004822941696)
	museumChannel = dawdle.get_channel(564613278874075166)
	animalsChannel = dawdle.get_channel(514556101052858378)
	nsfwChannel = dawdle.get_channel(600720406902734858)


	isStaff = False
	for role in ctx.message.author.roles:
		if	role == staffrole or role == saintrole:
			isStaff = True
			break
	if isStaff and ctx.message.channel:
		if arg == "all":
			def is_member(message):
				return not isinstance(message.author,discord.Member)
			deletedSelfies = await selfieChannel.purge(limit=None,check=is_member)
			deletedMuseum = await museumChannel.purge(limit=None,check=is_member)
			deletedAnimals = await animalsChannel.purge(limit=None,check=is_member)
			deletedIntro = await introChannel.purge(limit=None,check=is_member)
			deletedNSFW = await nsfwChannel.purge(limit=None,check=is_member)
			await ctx.send(f'{ctx.message.author.mention} deleted {len(deletedSelfies)} selfies, {len(deletedIntro)} intros, {len(deletedMuseum)} museum posts, {len(deletedAnimals)} animal posts, and {len(deletedNSFW)} NSFW posts')
		else:
			membDel = await dawdle.fetch_member(arg)
			def is_user(message):
				return str(message.author.id) == arg

			deleted = await selfieChannel.purge(limit=None,check=is_user)
			await ctx.send(f'{ctx.message.author.mention} deleted {len(deleted)} of {membDel}\'s selfies')


@bot.command()
async def done(ctx):
	dawdle = get_server(bot.guilds,'dawdle')
	introChannel = dawdle.get_channel(514555898648330260)
	dotRole = dawdle.get_role(587397534469718022)
	verifrole = dawdle.get_role(481148097960083471)
	angelrole = dawdle.get_role(563814890184376331)
	spamchannel = dawdle.get_channel(514560994337620008)
	hasDotRole = False
	hasIntro = False
	for role in ctx.message.author.roles:
		if role == dotRole:
			hasDotRole = True
			break
	if hasDotRole and ctx.message.channel == spamchannel:
		reqRoles = ctx.message.author.roles
		for role in reqRoles:
			if role == verifrole or role == angelrole or role == dotRole:
				reqRoles.remove(role)

		async for mess in introChannel.history(limit=None):
			if ctx.message.author == mess.author:
				hasIntro = True
				break
		if hasIntro and len(reqRoles) >= 5:
			await ctx.message.author.remove_roles(dotRole)
			await ctx.send(f'Well done {ctx.message.author.mention}! You’ve completed everything that needs to be done, enjoy your stay!')

		elif hasIntro and not len(reqRoles) >= 5:
			await ctx.send(f'Sorry {ctx.message.author.mention}, but you seem to be missing some <#527307900662710297>. Try again!')
		elif not hasIntro and len(reqRoles) >= 5:
			await ctx.send(f'Sorry {ctx.message.author.mention}, but it seems you haven\'t posted an <#514555898648330260>. Please post one and try again!')

		else:
			await ctx.send(f'Sorry {ctx.message.author.mention}, but you seem to be missing some <#527307900662710297> and an <#514555898648330260>. Try again!')
	
@bot.command()
async def msg_back(ctx, arg1 : str, arg2):
	dawdle = get_server(bot.guilds,'dawdle')
	verifchannel = dawdle.get_channel(623016717429374986)
	if ctx.message.channel == verifchannel:
		if ctx.message.mentions:
			try: 
				memb = ctx.message.mentions[0]
				await memb.send(f"{arg2}")
				await ctx.send(f'Message sent to {memb}.')
			except Forbidden:
				await verifchannel.send("Sorry, could not find that member or member has server DMs disabled")
				pass
		else:
			await ctx.send('You did not mention a member.')


@bot.command()
async def vent(ctx,arg : str):
	dawdle = get_server(bot.guilds,'dawdle')
	botChannel = dawdle.get_channel(654787316665286714)
	check_emoj = await dawdle.fetch_emoji(609771973341610033)
	cross_emoj = await dawdle.fetch_emoji(609771973102534687)
	ventChannel = dawdle.get_channel(514561071441248266)
	staffrole = dawdle.get_role(519616340940554270)
	if not ctx.message.guild:
		embedVent = discord.Embed(title='Vent',description = arg, color=0xffb6c1,timestamp = datetime.datetime.utcnow())
		embedVent.set_footer(text=ctx.message.author.id)
		ventMess = await botChannel.send(content=f'{staffrole.mention} Anonymous Vent',embed=embedVent)
		await ventMess.add_reaction(check_emoj)
		await ventMess.add_reaction(cross_emoj)
		try:
			await ctx.message.author.send('Your vent has been sent to staff for approval.')
		except:
			pass
	elif ctx.message.channel == ventChannel:
		for role in ctx.message.author.roles:
			if role == staffrole:
				ventMess = '<a:weewoo:598696151759192085> **Anonymous Venting** <a:weewoo:598696151759192085> \n \nHi I’m Dawdle! I’m here to forward any anonymous vents to our <#514561071441248266> channel. Some things before we get started is that this is entirely anonymous; staff will not see your name unless you do something that warrants us needing to know who you are. Please also note that this is __not__ a confessions bot and any sort of messages will be denied. This is meant for a more comfortable form of venting! Please read on for rules and instructions.  \n \n <a:weewoo:598696151759192085> **Anonymous Venting Rules** <a:weewoo:598696151759192085> \n \n <a:tinyheart:546404868529717270> 1. Any vent about another person in the server will be immediately denied. \n \n <a:tinyheart:546404868529717270> 2. Overtly sexual or explicit vents are not allowed. \n \n <a:tinyheart:546404868529717270> 3. __Dawdle rules apply__. Any suicide/self-harm references will be denied. \n \n <a:tinyheart:546404868529717270> 4. If you wish to vent and do not want any advice or responses write NA at the end of your vent. \n \n <a:tinyheart:546404868529717270> 5. While it is anonymous, staff can see user IDs and will warn/ban any user when necessary. \n \n <a:weewoo:598696151759192085> **Instructions on how to use** <a:weewoo:598696151759192085> \n \n <a:tinyheart:546404868529717270>  DM <@622553812221296696> using this format: \n >>> `/vent "Message"` \n \n__The double quotes around the message are important__, and make sure you __do not__ use double quotes elsewhere in the vent or I will get confused! \n \n `example:` /vent “Hello I am venting.” \n \n__You will get a confirmation message if the vent is sent to staff.__ If you do not get the confirmation message then you made a mistake in the command and should try again.'
				await ctx.send(ventMess)
				break


@bot.command()
async def check_intro(ctx):
	dawdle = get_server(bot.guilds,'dawdle')
	dotrole = dawdle.get_role(587397534469718022)
	introChannel = dawdle.get_channel(514555898648330260)
	botChannel = dawdle.get_channel(654787316665286714)
	verifiedRole = dawdle.get_role(481148097960083471)
	angelrole = dawdle.get_role(563814890184376331)
	if ctx.message.channel == botChannel:
		for mem in verifiedRole.members:
			has_intro = False
			async for intro in introChannel.history(limit=None):
				if intro.author == mem or mem.bot:
					has_intro = True
					break
			reqRoles = mem.roles
			for role in reqRoles:
				if role == verifiedRole or role == angelrole or role == dotrole:
					reqRoles.remove(role)
			if not (has_intro and len(reqRoles) > 5) and not mem.bot:
				try:
					await mem.add_roles(dotrole)
					await ctx.send(f'Gave dot role to {mem.mention}')
				except Forbidden:
					await ctx.send(f'I do not have permission to give dot role to {mem.mention}')
		await ctx.send('Done checking for intros and roles')

@bot.command()
async def kick_role(ctx,role,time : int):
	dawdle = get_server(bot.guilds,'dawdle')
	staffrole = dawdle.get_role(519616340940554270)
	saintrole = dawdle.get_role(490249474619211838)
	verifiedRole = dawdle.get_role(481148097960083471)
	isStaff = False
	for role in ctx.message.author.roles:
		if	role == staffrole or role == saintrole:
			isStaff = True
			break

	if isStaff and ctx.message.role_mentions:
		if ctx.message.role_mentions[0] != verifiedRole:
			mem_to_kick = []
			time_seconds = time*3600
			for mem in ctx.message.role_mentions[0].members:
				joined_duration = (datetime.datetime.utcnow() - mem.joined_at)
				joined_duration_sec = joined_duration.days*86400 + joined_duration.seconds
				if joined_duration_sec > time_seconds:
					mem_to_kick.append(mem)
			await ctx.send(f'Kick {len(mem_to_kick)} members with the {ctx.message.role_mentions[0].mention} role who joined before the past {time} hours? (yes/no)')
			def check(m):
				return m.author == ctx.message.author and m.channel == ctx.message.channel and (m.content.lower() == "yes" or m.content.lower() == "no")
			try:
				confirm = await bot.wait_for('message',check=check,timeout=60.0)
			
			except asyncio.TimeoutError:

				await ctx.send('Kick timed out.')
			
			else:
				if confirm.content.lower() == "yes":
					for mem in mem_to_kick:

						await dawdle.kick(user=mem)
						await ctx.send(f'Kicked {mem.name}')
					
					await ctx.send('Done kicking')

				else:
					await ctx.send('Kick cancelled.')
		else:
			await ctx.send('You cannot kick the verified role!')

@bot.command()
async def lockdown(ctx,arg : str):
	dawdle = get_server(bot.guilds,'dawdle')
	staffrole = dawdle.get_role(519616340940554270)
	saintrole = dawdle.get_role(490249474619211838)
	unverifrole = dawdle.get_role(479410607821684757)
	parlor = dawdle.get_channel(514550733732053012)
	foyer = dawdle.get_channel(514554494495752204)
	isStaff = False
	for role in ctx.message.author.roles:
		if	role == staffrole or role == saintrole:
			isStaff = True
			break
	if isStaff:
		if arg.lower() == "lock":
			await parlor.set_permissions(target=unverifrole,read_messages = False, send_messages =  False)
			await ctx.send('Parlor has been locked from unverified members. Use \`/lockdown unlock\` to undo this.')
			await foyer.send('[test] The main chat has been locked from unverified members due to a raid. Please be patient for staff to handle the issue.')

		elif arg.lower() == "unlock":
			await parlor.set_permissions(target=unverifrole,read_messages = True, send_messages =  True)
			await ctx.send('Parlor has been unlocked from unverified members. Use \`/lockdown lock\` to undo this.')
		else:
			await ctx.send('Please use \`/lockdown lock\` or \`/lockdown unlock\`')

# @bot.command()
# async def report(ctx, arg : str):
# 	dawdle = get_server(bot.guilds,'dawdle')
# 	botChannel = dawdle.get_channel(654787316665286714)
# 	staffrole = dawdle.get_role(623220291882975292)
# 	if not ctx.message.guild:
# 		embedReport = discord.Embed(title='',description = "", color=0xffb6c1,timestamp = datetime.datetime.utcnow())
# 		embedReport.add_field(name="Reporter",value=ctx.message.author.mention,inline=False)
# 		embedReport.add_field(name="Content",value=arg,inline=False)
# 		embedReport.set_footer(text=ctx.message.author)
# 		repMess = await botChannel.send(content=f'{staffrole.mention} Report',embed=embedReport)
# 		try:
# 			await ctx.message.author.send('Your report has been sent to staff.')
# 		except:
# 			pass

bot.run(token)




