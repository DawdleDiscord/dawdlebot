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
	game = discord.Game("ping amer if I'm not working")
	await bot.change_presence(status="saint's true fave",activity=game)

@bot.event
async def on_raw_reaction_add(payload):
	dawdle = get_server(bot.guilds,'dawdle')
	verifchannel = dawdle.get_channel(623016717429374986)
	userR = bot.get_user(payload.user_id)	
	verifEmoj = payload.emoji
	channelR = dawdle.get_channel(payload.channel_id)
#verification code	
	if channelR == verifchannel and not userR.bot and (str(verifEmoj) == '<:pinktick:609771973341610033>' or str(verifEmoj) == '<:pinkno:609771973102534687>'):
		verifMess = await verifchannel.fetch_message(payload.message_id)
		userM = verifMess.mentions[0]
		verifrole = dawdle.get_role(481148097960083471)
		unverifrole = dawdle.get_role(479410607821684757)
		dotRole = dawdle.get_role(587397534469718022)

		Ntick = 0
		Ncross = 0
		for vr in verifMess.reactions:
			if str(vr.emoji) == '<:pinktick:609771973341610033>':
				Ntick = vr.count
			elif str(vr.emoji) == '<:pinkno:609771973102534687>':
				Ncross = vr.count

		if str(verifEmoj) == '<:pinktick:609771973341610033>' and Ntick==2:
			await userM.add_roles(verifrole)
			await userM.add_roles(dotRole)
			await userM.remove_roles(unverifrole)
			await userM.send("Thank you for verifying! You’ve successfully completed this process, you are now able to see the majority of the server. Please proceed to get some <#527307900662710297> and to post an <#514555898648330260>! No formats are necessary for introductions, just a little snippet will do. When you are done with both, type \"/done\" (without the quotes) in <#514560994337620008>.")
		elif str(verifEmoj) == '<:pinkno:609771973102534687>' and Ncross==2:
			await userM.send("Sorry, but the pictures you provided do not follow our outlines as described in <#479407137060028449>. Please review and try again!")

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
	#Get disboard bot user
	bumpbot = dawdle.get_member(302050872383242240)
	#Check if disboard sent the message
	if(message.author.id == bumpbot.id):
		#Grab the embed from the message if there is an embed
		if(message.embeds):
			disboardEmbed = message.embeds[0]
			#Use the URL of the bump image to check if the bot had a successful bump.
			imageURL = 'https://disboard.org/images/bot-command-image-bump.png'
			if(disboardEmbed.image.url == imageURL):
				#Get the message directly before the bump as it should be whoever bumped it
				async for prevmessage in message.channel.history(limit=1, before=message.id):
					#Check if the message is a bump command
					if(prevmessage.content = '!d bump'):
						#Check if whoever sent the message is staff or not
						for r in prevmessage.author.roles:
							if r != staffrole:
								#Do whatever here to alert staff that someone bumped that wasn't staff
					
			
	if dawdle.get_member(message.author.id):
		userM = dawdle.get_member(message.author.id)
		unverified = False
		for r in userM.roles:
			if r == unverifrole:
				unverified = True
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
				await verifchannel.send(f'{staffrole.mention}, verify {userM}?')
				await message.author.dm_channel.send('Your message has been successfully submitted. Please wait patiently for a staff member to review your pictures.')
	
		elif message.channel == verifchannel and message.mentions and message.author.bot:
			await message.add_reaction('<:pinktick:609771973341610033>')
			await message.add_reaction('<:pinkno:609771973102534687>')
	
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
	
	#VC Tracker
async def on_voice_state_update(member, before, after):
    global botStartup
    global userAndDate
    #Check if they joined a voice channel
    if before.voice.voice_channel is None and after.voice.voice_channel is not None:
        currentTime = datetime.datetime.now()
        #Set the time for when they joined
        userAndDate[message.server.id] = currentTime
    #Check if they left a voice channel
    elif before.voice.voice_channel is not None and after.voice.voice_channel is None:
        #Set time for when they left
        currentTime = datetime.datetime.now()
        #Set the time for when they joined to bot startup in case of bot crashing, if they are in the list
        #Set the time for when they actually joined
        lastJoin = botStartup
        if message.server.id in serverAndDate:
            lastJoin = userAndDate[member.id]
        #Math the fuck out of some time for easy time differentiating
        diff = currentTime - lastJoin
        hours = math.floor(diff.seconds/3600)
        minutes = math.floor((diff.seconds - hours * 3600)/60)
        seconds = diff.seconds - hours * 3600 - minutes * 60
        #Formatted string for minutes
        mt = "{} minutes".format(minutes)
        #If they've been in VC for more than 10 minutes send to staff
        if (minutes>=10):
            userAndDate.remove(member.id)
            staffChannel = client.get_channel('641796475470217264')
            await staffChannel.send('{} was in VC for {}'.format(member.mention,mt))
        #If they haven't been in VC for 10 minutes just remove them from the list
        elif(minutes<=9):
            userAndDate.remove(member.id)
@bot.command()
async def cleanmembers(ctx,arg):
	dawdle = get_server(bot.guilds,'dawdle')
	staffrole = dawdle.get_role(519616340940554270)
	saintrole = dawdle.get_role(490249474619211838)
	introChannel = dawdle.get_channel(514555898648330260)
	selfieChannel = dawdle.get_channel(514556004822941696)
	museumChannel = dawdle.get_channel(564613278874075166)
	animalsChannel = dawdle.get_channel(514556101052858378)
	herNSFWChannel = dawdle.get_channel(600720351684591646)
	himNSFWChannel = dawdle.get_channel(600720380801449985)
	themNSFWChannel = dawdle.get_channel(600720406902734858)


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
			deletedNSFWher = await herNSFWChannel.purge(limit=None,check=is_member)
			deletedNSFWhim = await himNSFWChannel.purge(limit=None,check=is_member)
			deletedNSFWthem = await themNSFWChannel.purge(limit=None,check=is_member)
			deletedMuseum = await museumChannel.purge(limit=None,check=is_member)
			deletedAnimals = await animalsChannel.purge(limit=None,check=is_member)
			deletedIntro = await introChannel.purge(limit=None,check=is_member)
			
			numDelNSFW = len(deletedNSFWthem) + len(deletedNSFWhim) + len(deletedNSFWher)
			await ctx.send(f'{ctx.message.author.mention} deleted {len(deletedSelfies)} selfies, {len(deletedIntro)} intros, {len(deletedMuseum)} museum posts, {len(deletedAnimals)} animal posts, and {numDelNSFW} NSFW posts')
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
		for role in ctx.message.author.roles:
			if role == verifrole or role == angelrole or role == dotRole:
				reqRoles.remove(role)

		async for mess in introChannel.history(limit=50):
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
	#if arg1[2] == "!":
	#	memb_id = int(arg1[3:lastchar])
	#else:
	#	memb_id = int(arg1[2:lastchar])
	if ctx.message.channel == verifchannel:
		if ctx.message.mentions:
			try: 
				memb = ctx.message.mentions[0]
				await memb.send(f"{arg2}")
				await ctx.send(f'Message sent to {memb}.')
			except:
				await verifchannel.send("Sorry, could not find that member or member has server DMs disabled")
				pass
		else:
			await ctx.send('You did not mention a member.')


bot.run(token)




