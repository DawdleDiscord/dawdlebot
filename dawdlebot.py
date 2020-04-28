import discord
import datetime
import asyncio
import math
from discord.ext.commands import Bot
from discord.ext import commands, tasks
import gn_mess_dict
import random
from dawdle_vars import dawdletoken
from db_birthdays import birthdays
from db_moderation import moderation
from db_qotd import qotd
from db_fuzzies import fuzzies
from db_clean import clean
import json,typing

bot = Bot(command_prefix = '/')
#List for times
userAndDate = {}
#Time at start up.
botStartup = datetime.datetime.now()
token = dawdletoken
GUILD1 = 'dawdle'
GUILD2 = 'amertestserver'

adminroles = [490249474619211838, 514556928655884298, 623220291882975292]
modroles = adminroles.append(519632663246536736)

def get_server(guilds,server):
	for guild in guilds:
		if guild.name == server:
			return guild
			break

def is_staff():
	async def is_staff_predicate(ctx):
		dawdle = ctx.guild
		isStaff = False
		for role in ctx.author.roles:
			if role.id == 519616340940554270 or role.id == 490249474619211838:
				isStaff = True
				break
		return isStaff
	return commands.check(is_staff_predicate)


bot.add_cog(birthdays(bot))
bot.add_cog(moderation(bot))
bot.add_cog(qotd(bot))
bot.add_cog(clean(bot))

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error,commands.errors.CommandNotFound):
		await ctx.send('Huh?')
	else:
		testserver = get_server(bot.guilds, 'dawdle bot')
		errorchannel = testserver.get_channel(701622624526139402)
		errorEmbed = discord.Embed()
		errorEmbed.add_field(name = 'User', value = ctx.author, inline = False)
		errorEmbed.add_field(name= 'Message', value = ctx.message.content, inline = False)
		errorEmbed.add_field(name= 'Error', value = error, inline = False)
		await errorchannel.send(embed = errorEmbed)
		print(error)

with open('fuzzies.json', 'r') as json_f_r:
	fuzz_dict = json.load(json_f_r)
if fuzz_dict['onoff']:
	bot.add_cog(fuzzies(bot))

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
		verifrole = dawdle.get_role(481148097960083471)
		unverifrole = dawdle.get_role(479410607821684757)
		dotRole = dawdle.get_role(587397534469718022)
		check_emoj = await dawdle.fetch_emoji(609771973341610033)
		cross_emoj = await dawdle.fetch_emoji(609771973102534687)
		date_emoj = await dawdle.fetch_emoji(630533105903730689)
		dawd_emoj = await dawdle.fetch_emoji(586767353740656656)
		name_emoj = await dawdle.fetch_emoji(598695827891945472)

		for vr in verifMess.reactions:
			if vr.count == 2 and verifMess.mentions and "verify" in verifMess.content:
				userM = verifMess.mentions[0]
				if vr.emoji == check_emoj:
				
					await userM.add_roles(verifrole)
					await userM.add_roles(dotRole)
					await userM.remove_roles(unverifrole)
					await userM.send("Thank you for verifying! You’ve successfully completed this process, you are now able to see the majority of the server. Please proceed to get some <#694994576791961630> and to post an <#514555898648330260>! No formats are necessary for introductions, just a little snippet will do. When you are done with both, type \"/done\" (without the quotes) in <#514560994337620008>.")

				elif verifEmoj == cross_emoj:
				
					await userM.send("Sorry, but the pictures you provided do not follow our outlines as described in <#479407137060028449>. Please review and try again!")

				elif verifEmoj == date_emoj:

					await userM.send("You’re missing today’s date on the selfie picture!")

				elif verifEmoj == dawd_emoj:

					await userM.send("You're missing the server name on the selfie picture!")
			
				elif verifEmoj == name_emoj:

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
	ventChannel = dawdle.get_channel(514561071441248266)
	if srcChannel == verifchannel:
		ventMess = await srcChannel.fetch_message(payload.message_id)
		if ventMess.embeds and ventMess.embeds[0].title=='Vent' and (verifEmoj.id == 609771973341610033 or verifEmoj.id == 609771973102534687):
			for vr in ventMess.reactions:
				if vr.emoji == verifEmoj and vr.count == 2:
					if verifEmoj.id == 609771973341610033:
						embedVent = ventMess.embeds[0]
						embedVent.title = ''
						embedVent.set_footer(text='')
						await ventChannel.send(embed=embedVent)
					elif verifEmoj.id == 609771973102534687:
						ventMemb = await dawdle.fetch_member(ventMess.embeds[0].footer.text)
						await ventMemb.send('<a:weewoo:598696151759192085> **Anonymous Venting** <a:weewoo:598696151759192085> \n \nHi I’m Dawdle! I’m here to forward any anonymous vents to our <#514561071441248266> channel. Some things before we get started is that this is entirely anonymous; staff will not see your name unless you do something that warrants us needing to know who you are. Please also note that this is __not__ a confessions bot and any sort of messages will be denied. This is meant for a more comfortable form of venting! Please read on for rules and instructions.  \n \n <a:weewoo:598696151759192085> **Anonymous Venting Rules** <a:weewoo:598696151759192085> \n \n <a:tinyheart:546404868529717270> 1. Any vent about another person in the server will be immediately denied. \n \n <a:tinyheart:546404868529717270> 2. Overtly sexual or explicit vents are not allowed. \n \n <a:tinyheart:546404868529717270> 3. __Dawdle rules apply__. Any suicide/self-harm references will be denied. \n \n <a:tinyheart:546404868529717270> 4. If you wish to vent and do not want any advice or responses write NA at the end of your vent. \n \n <a:tinyheart:546404868529717270> 5. While it is anonymous, staff can see user IDs and will warn/ban any user when necessary. \n \n <a:weewoo:598696151759192085> **Instructions on how to use** <a:weewoo:598696151759192085> \n \n <a:tinyheart:546404868529717270>  DM <@622553812221296696> using this format: \n >>> `/vent Message` \n \n `example:` /vent Hello I am venting. \n \n__You will get a confirmation message if the vent is sent to staff.__ If you do not get the confirmation message then you made a mistake in the command and should try again.')


@bot.event
async def on_member_join(member):
	dawdle = get_server(bot.guilds,'dawdle')
	unverifrole = dawdle.get_role(479410607821684757)
	foyerchannel = dawdle.get_channel(514554494495752204)
	if member.guild == dawdle:
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
				embedVar.add_field(name="Link",value=f"[Link to image]({a.url})")
				embedVar.set_footer(text=f"ID: {message.author.id}")
				verifImage = await verifchannel.send(embed=embedVar)

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

	if "😂" in message.content.lower():
		try:
			await message.delete()
		except:
			pass


	await bot.process_commands(message)

@bot.event
async def on_member_remove(member):
	dawdle = get_server(bot.guilds,'dawdle')
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
			verifChannel = get_server(bot.guilds,'dawdle').get_channel(623016717429374986)
			noKoins = False
			async for mess in verifChannel.history(limit=200):
				if mess.embeds and mess.embeds[0].title == "VC Koins" and mess.author.id == 622553812221296696:
					if  mess.embeds[0].footer.text == str(member.id) and (datetime.datetime.utcnow() - mess.embeds[0].timestamp).days < 1:
						noKoins = True
						break
			if not noKoins:
				voiceEmbed = discord.Embed(title= "VC Koins",description=f"{member.mention} was in VC for {mt}. Give them koins!",color=0xffb6c1,timestamp = datetime.datetime.utcnow())
				voiceEmbed.set_footer(text=f'{member.id}')
				await verifChannel.send(embed=voiceEmbed)
		#If they haven't been in VC for 10 minutes just remove them from the list
		elif(minutes<20 and userAndDate[member.id]):
			del userAndDate[member.id]


@bot.command()
@is_staff()
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
@cleanmembers.error
async def cleanmembers_error(ctx,error):
	if isinstance(error,commands.errors.CheckFailure):
		await ctx.send('You do not have permissions to do this.')
	else:
		await ctx.send(f'I had an unknown error {str(error)}')

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
		age_roles = [dawdle.get_role(481138497856602113), dawdle.get_role(480080787253755905), dawdle.get_role(481138992151003156), dawdle.get_role(481138740484505611)]
		pronoun_roles = [dawdle.get_role(551901787297284096),dawdle.get_role(551901739700322324),dawdle.get_role(551901812677017611)]
		dm_roles = [dawdle.get_role(479410113115979805),dawdle.get_role(479410060804751371),dawdle.get_role(479410091905253376)]
		loc_roles = [dawdle.get_role(481135072427376641), dawdle.get_role(481135146129424415), dawdle.get_role(481135185497423900), dawdle.get_role(481135221572501516), dawdle.get_role(481135414321610763), dawdle.get_role(481135465399844882), dawdle.get_role(481136198014861336)]
		check_age, check_pronoun, check_dm, check_loc, has_dot = (False,)*5
		for role in ctx.message.author.roles:
			if role in age_roles: check_age = True
			if role in pronoun_roles: check_pronoun = True
			if role in dm_roles: check_dm = True
			if role in loc_roles: check_loc = True
		role_check = check_age and check_pronoun and check_dm and check_loc
		async for mess in introChannel.history(limit=None):
			if ctx.message.author == mess.author:
				hasIntro = True
				break
		if hasIntro and role_check:
			await ctx.message.author.remove_roles(dotRole)
			await ctx.send(f'Well done {ctx.message.author.mention}! You’ve completed everything that needs to be done, enjoy your stay!')

		elif hasIntro and not role_check:
			await ctx.send(f'Sorry {ctx.message.author.mention}, but you seem to be missing some <#694994576791961630>. Try again!')
		elif not hasIntro and role_check:
			await ctx.send(f'Sorry {ctx.message.author.mention}, but it seems you haven\'t posted an <#514555898648330260>. Please post one and try again!')

		else:
			await ctx.send(f'Sorry {ctx.message.author.mention}, but you seem to be missing some <#694994576791961630> and an <#514555898648330260>. Try again!')
	
@bot.command(aliases=['mb','msgback','msg','message'])
@is_staff()
async def msg_back(ctx, member : discord.Member,*, message : str):
	dawdle = get_server(bot.guilds,'dawdle')
	verifchannel = dawdle.get_channel(623016717429374986)
	if ctx.message.channel == verifchannel:
		await member.send(message)
		await ctx.send(f'Message sent to {member}.')
@msg_back.error
async def msg_back_error(ctx,error):
	if isinstance(error,discord.Forbidden) or isinstance(error,discord.HTTPException):
		await ctx.send('I was unable to send the message.')
	elif isinstance(error,commands.errors.BadArgument):
		await ctx.send('I could not find that member or too many members with that name.')
	else:
		await ctx.send(f'I had an unknown error {str(error)}.')
		
@bot.command()
async def vent(ctx,*,vent_text : str):
	dawdle = get_server(bot.guilds,'dawdle')
	verifChannel = dawdle.get_channel(623016717429374986)
	check_emoj = await dawdle.fetch_emoji(609771973341610033)
	cross_emoj = await dawdle.fetch_emoji(609771973102534687)
	ventChannel = dawdle.get_channel(514561071441248266)
	staffrole = dawdle.get_role(519616340940554270)
	if not ctx.message.guild:
		embedVent = discord.Embed(title='Vent',description = vent_text, color=0xffb6c1,timestamp = datetime.datetime.utcnow())
		embedVent.set_footer(text=ctx.message.author.id)
		ventMess = await verifChannel.send(content=f'{staffrole.mention} Anonymous Vent',embed=embedVent)
		await ventMess.add_reaction(check_emoj)
		await ventMess.add_reaction(cross_emoj)
		try:
			await ctx.message.author.send('Your vent has been sent to staff for approval. Sometimes although your vent may be fine, staff will wait to approve if someone else has vented recently.')
		except:
			pass
	elif ctx.message.channel == ventChannel:
		for role in ctx.message.author.roles:
			if role == staffrole:
				await ctx.message.delete()
				ventMess = '<a:weewoo:598696151759192085> **Anonymous Venting** <a:weewoo:598696151759192085> \n \nHi I’m Dawdle! I’m here to forward any anonymous vents to our <#514561071441248266> channel. Some things before we get started is that this is entirely anonymous; staff will not see your name unless you do something that warrants us needing to know who you are. Please also note that this is __not__ a confessions bot and any sort of messages will be denied. This is meant for a more comfortable form of venting! Please read on for rules and instructions.  \n \n <a:weewoo:598696151759192085> **Anonymous Venting Rules** <a:weewoo:598696151759192085> \n \n <a:tinyheart:546404868529717270> 1. Any vent about another person in the server will be immediately denied. \n \n <a:tinyheart:546404868529717270> 2. Overtly sexual or explicit vents are not allowed. \n \n <a:tinyheart:546404868529717270> 3. __Dawdle rules apply__. Any suicide/self-harm references will be denied. \n \n <a:tinyheart:546404868529717270> 4. If you wish to vent and do not want any advice or responses write NA at the end of your vent. \n \n <a:tinyheart:546404868529717270> 5. While it is anonymous, staff can see user IDs and will warn/ban any user when necessary. \n \n <a:weewoo:598696151759192085> **Instructions on how to use** <a:weewoo:598696151759192085> \n \n <a:tinyheart:546404868529717270>  DM <@622553812221296696> using this format: \n >>> `/vent Message` \n \n `example:` /vent Hello I am venting. \n \n__You will get a confirmation message if the vent is sent to staff.__ If you do not get the confirmation message then you made a mistake in the command and should try again.'
				await ctx.send(ventMess)
				break

@vent.error
async def vent_error(ctx,error):
	if isinstance(error,commands.errors.MissingRequiredArgument):
		await ctx.send('It looks like you are sending a vent. You need text after the `/vent`!')

@bot.command(aliases=['checkintro'])
@is_staff()
async def check_intro(ctx):
	dawdle = get_server(bot.guilds,'dawdle')
	dotrole = dawdle.get_role(587397534469718022)
	introChannel = dawdle.get_channel(514555898648330260)
	botChannel = dawdle.get_channel(654787316665286714)
	verifiedRole = dawdle.get_role(481148097960083471)

	age_roles = [dawdle.get_role(481138497856602113), dawdle.get_role(480080787253755905), dawdle.get_role(481138992151003156), dawdle.get_role(481138740484505611)]
	pronoun_roles = [dawdle.get_role(551901787297284096),dawdle.get_role(551901739700322324),dawdle.get_role(551901812677017611)]
	dm_roles = [dawdle.get_role(479410113115979805),dawdle.get_role(479410060804751371),dawdle.get_role(479410091905253376)]
	loc_roles = [dawdle.get_role(481135072427376641), dawdle.get_role(481135146129424415), dawdle.get_role(481135185497423900), dawdle.get_role(481135221572501516), dawdle.get_role(481135414321610763), dawdle.get_role(481135465399844882), dawdle.get_role(481136198014861336)]

	if ctx.message.channel == botChannel:
		def emoji_response(check):
			if check == True: return '<:pinkcheck:609771973341610033>'
			else: return '<:pinkx:609771973102534687>'	
		for mem in verifiedRole.members:
			has_intro = False
			async for intro in introChannel.history(limit=None):
				if intro.author == mem or mem.bot:
					has_intro = True
					break

			check_age, check_pronoun, check_dm, check_loc, has_dot = (False,)*5
			for role in mem.roles:
				if role in age_roles: check_age = True
				if role in pronoun_roles: check_pronoun = True
				if role in dm_roles: check_dm = True
				if role in loc_roles: check_loc = True
				if role == dotrole: has_dot = True 
			role_check = check_age and check_pronoun and check_dm and check_loc
			intro_emoji = emoji_response(has_intro)
			role_emoji = emoji_response(role_check)
			if not mem.bot and (not has_intro or not role_check):
				if has_dot:
					await ctx.send(f'{mem.mention} already has dot role. Intro: {intro_emoji} Roles: {role_emoji}')
				else:
					try:
						await mem.add_roles(dotrole)
					except:
						await ctx.send(f'I could not give dot role to {mem.mention}')
					else:
						await ctx.send(f'Gave dot role to {mem.mention}. Intro: {intro_emoji} Roles: {role_emoji}')
		await ctx.send('Done checking for intros and roles')
@check_intro.error
async def check_intro(ctx,error):
	if isinstance(error,commands.errors.CheckFailure):
		await ctx.send('You do not have permissions to do this.')
	else:
		await ctx.send(f'I had an unknown error {str(error)}')

@bot.command(aliases=['kickrole'])
@is_staff()
async def kick_role(ctx,role,time : int):
	dawdle = get_server(bot.guilds,'dawdle')
	staffrole = dawdle.get_role(519616340940554270)
	saintrole = dawdle.get_role(490249474619211838)
	verifiedRole = dawdle.get_role(481148097960083471)
	if ctx.message.role_mentions:
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
@kick_role.error
async def kick_role_error(ctx, error):
	if isinstance(error,commands.errors.CheckFailure):
		await ctx.send('You do not have permissions to do this.')
	else: pass

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
			await foyer.send('The main chat has been locked from unverified members due to a raid. Please be patient for staff to handle the issue.')

		elif arg.lower() == "unlock":
			await parlor.set_permissions(target=unverifrole,read_messages = True, send_messages =  True)
			await ctx.send('Parlor has been unlocked from unverified members. Use \`/lockdown lock\` to undo this.')
		else:
			await ctx.send('Please use \`/lockdown lock\` or \`/lockdown unlock\`')

@bot.command()
async def report(ctx, *, report_text : str):
	dawdle = get_server(bot.guilds,'dawdle')
	verifChannel = dawdle.get_channel(623016717429374986)
	staffrole = dawdle.get_role(519616340940554270)
	if not ctx.message.guild:
		embedReport = discord.Embed(title='Report',description = "", color=0xffb6c1,timestamp = datetime.datetime.utcnow())
		embedReport.add_field(name="Reporter",value=ctx.message.author.mention,inline=False)
		embedReport.add_field(name="Content",value=report_text,inline=False)
		embedReport.set_footer(text=ctx.message.author.id)
		repMess = await verifChannel.send(content=f'{staffrole.mention} Report',embed=embedReport, )
		for a in ctx.message.attachments:
			embedReport = discord.Embed(title='Report',description = "", color=0xffb6c1,timestamp = datetime.datetime.utcnow())
			embedReport.add_field(name="Reporter",value=ctx.message.author.mention,inline=False)
			embedReport.set_image(url=a.url)
			embedReport.set_footer(text=ctx.message.author.id)
			await verifChannel.send(content=f'{staffrole.mention} Report',embed=embedReport)
		try:
			await ctx.message.author.send('Your report has been sent to staff.')
		except:
			pass

@report.error
async def report_error(ctx,error):
	if isinstance(error,commands.errors.MissingRequiredArgument):
		await ctx.send('It looks like you are sending a report. You need text after the `/report`. If you are sending images, then include `/report Image`')

@bot.command(aliases=['info'])
async def information(ctx):
	if ctx.message.author.id == 267209579929141249:
		dawdle = get_server(bot.guilds,'dawdle')
		staffrole = dawdle.get_role(519616340940554270)
		information = dawdle.get_channel(479407137060028449)
		extra = discord.Embed(title="",description="<:dotmid:611226754123563008> [FAQ](https://discordapp.com/channels/475584392740339712/514560994337620008/685682260091076618)\n<:dotmid:611226754123563008> [Channel guide](https://discordapp.com/channels/475584392740339712/514560994337620008/686350526891294895) \n<:dotmid:611226754123563008> [How the economy works](https://discordapp.com/channels/475584392740339712/514560994337620008/693974955980881962)\n<:dotmid:611226754123563008> [Add your birthday to the bot!](https://discordapp.com/channels/475584392740339712/514560994337620008/685684422980272275)\n<:dotmid:611226754123563008> Couple roles are available to two consenting individuals in the server. \n<:dotmid:611226754123563008> Check channel descriptions, they can clear up any confusion regarding what can be posted in that channel. \n<:dotmid:611226754123563008> Nitro boosting allows you to add emojis to the server and to pick a color in roles.",color=0xffb6c1)
		#extra.add_field(name='[FAQ]{https://discordapp.com/channels/475584392740339712/514560994337620008/685682260091076618}', value=' ', inline=False)
		#extra.add_field(name='[How the economy works]{https://discordapp.com/channels/475584392740339712/514560994337620008/669961792058818600}', value=' ', inline=False)
		#extra.add_field(name='[Add your birthday to the bot!]{https://discordapp.com/channels/475584392740339712/514560994337620008/685684422980272275}', value=' ', inline=False)
		#extra.add_field(name='Check channel descriptions, they can clear up any confusion regarding what can be posted in that channel.', value=' ', inline=False)
		#extra.add_field(name='Nitro boosting allows you to add emojis to the server and to pick a color in roles.', value=' ', inline=False)

		def only_true(message):
			return True
		await information.purge(check=only_true)
		await information.send(file=discord.File('Disclaimer_-_1000_wd.png'))
		await information.send("<a:korbstar:546733206007840778> **Welcome to Dawdle** <a:korbstar:546733206007840778> \n \nWe pride ourselves on being an adult-ONLY server that emphasizes a wholesome, non-toxic atmosphere that is welcoming to all. Our priorities are to foster a supportive environment to create lasting friendships. \n \nPlease read all rules carefully, as ignorance to the rules is not an excuse for violating them. Please use common sense in areas not explicitly covered by rules and ask staff if you are unsure.")
		await information.send(file=discord.File('Rules_-_1000_wd.png'))
		await information.send("<a:pinkstar:663174593376419890> `Rule 1` **Accounts** \n > <:dotmid:611226754123563008> You must be 18+ to be in the server, and you must verify to stay in the server, no exceptions will be allowed. \n > <:dotdark:611226752466813040> After verifying, you need to get <#694994576791961630> and an <#514555898648330260>, when both of these are done type `/done` in <#514560994337620008> to complete the verifying process. If you lack a profile picture, you will be asked to get one at this time. \n > <:dotmid:611226754123563008> Alt accounts are not permitted. Do not try to bypass bans or mutes. \n<a:pinkstar:663174593376419890> `Rule 2` **Content** \n > <:dotdark:611226752466813040> Any form of hateful or discriminatory speech is not allowed.\n > <:dotmid:611226754123563008> Spamming is not permitted. This includes an excess amount of emojis, pictures, and individual lines of text. \n > <:dotdark:611226752466813040> Any credible threats to life, be it suicide or criminal violence, will not be tolerated in the server. We do not have appropriate resources to deal with topics of this magnitude and cannot be held responsible for someone’s physical well-being.\n > <:dotmid:611226754123563008> Jokes about being underaged are not tolerated, regardless if you are verified.")
		await information.send("<a:pinkstar:663174593376419890> `Rule 3` **Conduct** \n > <:dotdark:611226752466813040> Check peoples roles. Respect people’s pronouns and dm preferences. \n > <:dotmid:611226754123563008> Being obnoxious, overbearing, and edgy is prohibited. This includes VC *and* chat. \n > <:dotdark:611226752466813040> Being creepy is not allowed. This includes sending unsolicited messages, and being overtly sexual constantly. \n > <:dotmid:611226754123563008> Leaving will reset your levels and require reverification. Leaving repeatedly will result in a ban. \n > <:dotdark:611226752466813040> Mass pinging unnecessarily will result in a ban. \n > <:dotmid:611226754123563008> Welcoming new members and saying hello to others is common courtesy here. Being cliquey is discouraged. Be nice to others, be nice to yourself. \n<a:pinkstar:663174593376419890> `Rule 4` **Channels** \n > <:dotmid:611226754123563008> <#514550733732053012> is strictly SFW. NSFW topics belong in <#529879816208384010>. \n > <:dotdark:611226752466813040> Keep channels on topic. Check channel descriptions for more details. \n > <:dotmid:611226754123563008> Our NSFW channels are for lvl 20+ members only. Inactivity in other channels or creepy behavior will get permissions revoked. NSFW permissions are granted at staff discretion, please dm staff for details. \n<a:pinkstar:663174593376419890> `Rule 5` **Advertising** \n > <:dotdark:611226752466813040> Self advertisement is not allowed, this includes dm advertisements. Asking for followers on social media and posting social media profiles are also prohibited. \n > <:dotmid:611226754123563008> No name dropping non-partnered servers or slandering partnered servers. \n<a:pinkstar:663174593376419890> `Rule 6` **Terms of Service** \n > <:dotdark:611226752466813040> Do not violate Discord's Terms of Service. \n > <:dotmid:611226754123563008> Doing so will result in staff reporting you to discord, as well as getting banned from here.")
		await information.send(file=discord.File("Moderation_-_1000_wd.png"))
		await information.send(f">>> <a:pinkstar:663174593376419890> Three warnings will result in a ban. While each situation is different, it is important to report situations that are against our rules. Please DM <@622553812221296696> with `/report <message>`. Images can be included if `/report` is sent in the text. If the situation is sensitive please DM a staff member. \n \n <a:pinkstar:663174593376419890> With all of that said, the server owner has the right to ban you for whatever they feel necessary. \n \n <a:pinkstar:663174593376419890> Inactive people will be pinged by staff in order to be checked in on, failure to answer to multiple pings will result in a kick for being a lurker.")
		await information.send(file=discord.File("Verification_-_1000_wd.png"))
		await information.send(">>> Verification of being 18+ ensures the security and safety of our members and our community as a whole from catfishing or other identity-related issues. To verify, send the items detailed below to <@622553812221296696>. You are able and encouraged to delete these pictures after verifying. \n \n`First Photo` You holding a piece of paper/sticky note with our server name, your discord tag (Name#0001), and the current date (MM/DD/YYYY). \n \n`Second Photo` A picture of your blurred-out ID with only your DOB and photo showing. All other information should be crossed out.")
		await information.send(file=discord.File('image0.jpg'))
		await information.send(file=discord.File('Partners_-_1000_wd.png'))
		await information.send("We will partner with servers regardless of member count. If your server follows the requirements below, please contact <@291682666246307841> or <@381507393470857229>. \n > <:dotdark:611226752466813040> We will not ping, ever. \n > <:dotmid:611226754123563008> All NSFW content must be behind a wall of verification. \n > <:dotdark:611226752466813040> Must follow Terms of Service. \n > <:dotmid:611226754123563008> If you wish to stay as a representative of your server, you must verify. \n > <:dotdark:611226752466813040> If your link expires, it will be deleted. \n > <:dotmid:611226754123563008> All partners must follow the rules of the server, no exceptions will be made.")
		await information.send(file=discord.File('Levels_-_1000_wd.png'))
		await information.send("Levels are obtained by being active in channels. \n > <:dotdark:611226752466813040> **lvl 10** add reactions, access selfies, museum, and vc \n > <:dotmid:611226754123563008> **lvl 20** create instant invite, image perms \n > <:dotdark:611226752466813040> **lvl 30** check audit log, link perms \n > <:dotmid:611226754123563008> **lvl 40** select a color from roles \n > <:dotdark:611226752466813040> **lvl 50** go live perms")
		await information.send(file=discord.File('Extra_-_1000_wd.png'))
		await information.send(embed=extra)

@bot.command()
@is_staff()
async def rolecolor(ctx, role : discord.Role, newcolor : discord.Colour):
	oldcolor = role.color
	await role.edit(color=newcolor)
	returnEmbed = discord.Embed(title=f"Changed the role color for {role.name} to {str(newcolor)}. Old color: {str(oldcolor)}.",color=newcolor)
	await ctx.send(embed=returnEmbed)
@rolecolor.error
async def rolecolor_error(ctx,error):
	if isinstance(error,commands.errors.BadArgument):
		await ctx.send('I could not find that role or color.')
	elif isinstance(error,commands.CommandInvokeError):
		await ctx.send('I do not have permissions to change this role')
	elif isinstance(error,commands.errors.CheckFailure):
		await ctx.send('You do not have permissions to do this.')
	else:
		await ctx.send(f'I had an unknown error: {str(error)}')

@bot.command()
@is_staff()
async def flashfuzzies(ctx, onoff : str, chnnl : typing.Optional[discord.TextChannel]):
	with open('fuzzies.json', 'r') as json_f_r:
		fuzz_dict = json.load(json_f_r)
	if fuzz_dict['onoff']:
		old_onoff = 'on'
	else:
		old_onoff = 'off'
	if old_onoff != onoff and (onoff.lower() == 'on' or onoff.lower() == 'off'):
		if onoff.lower() == 'on':
			try:
				fuzz_dict['channel'] = chnnl.id
				fuzz_dict['onoff'] = True
				try:
					bot.add_cog(fuzzies(bot))
				except discord.errors.ClientException:
					pass

				await ctx.send('Fuzzies has been turned on.')
			except AttributeError:
				await ctx.send('please specify a channel')

			with open('fuzzies.json', 'w') as json_f_w:
				json.dump(fuzz_dict, json_f_w)
		else:
			fuzz_dict['onoff'] = False
			await ctx.send('Fuzzies has been turned off')
			try: 
				bot.remove_cog('fuzzies')
			except:
				pass
			with open('fuzzies.json', 'w') as json_f_w:
				json.dump(fuzz_dict, json_f_w)
	elif old_onoff == onoff:
		if old_onoff:
			await ctx.send('Fuzzies is already turned on')
		else: 
			await ctx.send('Fuzzies is already off')

@bot.command()
@is_staff()
async def cleanrestart(ctx):
	bot.remove_cog('clean')
	bot.add_cog(clean(bot))

bot.run(token)




