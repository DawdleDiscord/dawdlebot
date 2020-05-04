import discord
import datetime
import asyncio
import math
import sys
#sys.path.append('/src')
from discord.ext.commands import Bot
from discord.ext import commands, tasks
import gn_mess_dict
import random
from dawdle_vars import dawdletoken
from src.db_modules import birthdays,moderation,qotd,fuzzies,clean,verification,members,db_autoreact,db_roles,db_vent,db_VCtrack,db_welcomegoodbye,db_pins
from src.db_modules import SmartMember

import json,typing

bot = Bot(command_prefix = '~')

token = dawdletoken


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
bot.add_cog(verification(bot))
bot.add_cog(clean(bot))
bot.add_cog(members(bot))
bot.add_cog(db_autoreact(bot))
bot.add_cog(db_roles(bot))
bot.add_cog(db_vent(bot))
bot.add_cog(db_VCtrack(bot))
bot.add_cog(db_welcomegoodbye(bot))
bot.add_cog(db_pins(bot))

# with open('src/data/db_config.json', 'r') as json_file:
# 	config = json.load(json_file)
# del json_file

# cog_list = [birthdays, moderation, qotd, verification, clean, members, db_autoreact, db_roles, db_vent, db_VCtrack, db_welcomegoodbye]
# for cog in cog_list:
# 	if config[str(cog)]:
# 		bot.add_cog(cog(bot))
# for key in bot.cogs.keys():
# 	print(f'Loaded {key}')

# @bot.group()
# async def module(ctx):
# 	if ctx.invoked_subcommand is None:
# 		await ctx.send('Invalid module command')

# @module.command()
# async def add(ctx, name : str)


#with open('src/data/db_config.json', 'w') as json_file:
#	json.dump(config, json_file)

@bot.command()
async def sayhi(ctx, member : SmartMember):
	await ctx.send(f'hi {member.mention}')

# @bot.event
# async def on_command_error(ctx, error):
# 	if isinstance(error,commands.errors.CommandNotFound):
# 		await ctx.send('Huh?')
# 	else:
# 		testserver = get_server(bot.guilds, 'dawdle bot')
# 		errorchannel = testserver.get_channel(701622624526139402)
# 		errorEmbed = discord.Embed()
# 		if ctx.author:
# 			errorEmbed.add_field(name = 'User', value = ctx.author, inline = False)
# 		if ctx.message.content:
# 			errorEmbed.add_field(name= 'Message', value = ctx.message.content, inline = False)
# 		errorEmbed.add_field(name= 'Error', value = error, inline = False)
# 		await errorchannel.send(embed = errorEmbed)
# 		print(error)

with open('src/data/fuzzies.json', 'r') as json_f_r:
	fuzz_dict = json.load(json_f_r)
if fuzz_dict['onoff']:
	bot.add_cog(fuzzies(bot))

@bot.event
async def on_ready():
	dawdle = get_server(bot.guilds,'dawdle')
	print(f'{bot.user} has connected to Discord!', f'{dawdle.name}(id: {dawdle.id})')
	game = discord.Game("say 'nini dawdle' for a goodnight message!")
	await bot.change_presence(activity=game)




### some miscellaneous things
@bot.event
async def on_message(message):

	dawdle = get_server(bot.guilds,'dawdle')
	#Hearting posts in intro, selfies, museum
	introchannel = dawdle.get_channel(514555898648330260)
	if message.channel == introchannel:
		def is_old_intro(mess2):
			return mess2.author == message.author and mess2.id != message.id and mess2.author.id != 381507393470857229 
		deleted_intro = await introchannel.purge(limit=None,check=is_old_intro)

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
		await information.send(file=discord.File('src/images/Disclaimer_-_1000_wd.png'))
		await information.send("<a:korbstar:546733206007840778> **Welcome to Dawdle** <a:korbstar:546733206007840778> \n \nWe pride ourselves on being an adult-ONLY server that emphasizes a wholesome, non-toxic atmosphere that is welcoming to all. Our priorities are to foster a supportive environment to create lasting friendships. \n \nPlease read all rules carefully, as ignorance to the rules is not an excuse for violating them. Please use common sense in areas not explicitly covered by rules and ask staff if you are unsure.")
		await information.send(file=discord.File('src/images/Rules_-_1000_wd.png'))
		await information.send("<a:pinkstar:663174593376419890> `Rule 1` **Accounts** \n > <:dotmid:611226754123563008> You must be 18+ to be in the server, and you must verify to stay in the server, no exceptions will be allowed. \n > <:dotdark:611226752466813040> After verifying, you need to get <#694994576791961630> and an <#514555898648330260>, when both of these are done type `/done` in <#514560994337620008> to complete the verifying process. If you lack a profile picture, you will be asked to get one at this time. \n > <:dotmid:611226754123563008> Alt accounts are not permitted. Do not try to bypass bans or mutes. \n<a:pinkstar:663174593376419890> `Rule 2` **Content** \n > <:dotdark:611226752466813040> Any form of hateful or discriminatory speech is not allowed.\n > <:dotmid:611226754123563008> Spamming is not permitted. This includes an excess amount of emojis, pictures, and individual lines of text. \n > <:dotdark:611226752466813040> Any credible threats to life, be it suicide or criminal violence, will not be tolerated in the server. We do not have appropriate resources to deal with topics of this magnitude and cannot be held responsible for someone’s physical well-being.\n > <:dotmid:611226754123563008> Jokes about being underaged are not tolerated, regardless if you are verified.")
		await information.send("<a:pinkstar:663174593376419890> `Rule 3` **Conduct** \n > <:dotdark:611226752466813040> Check peoples roles. Respect people’s pronouns and dm preferences. \n > <:dotmid:611226754123563008> Being obnoxious, overbearing, and edgy is prohibited. This includes VC *and* chat. \n > <:dotdark:611226752466813040> Being creepy is not allowed. This includes sending unsolicited messages, and being overtly sexual constantly. \n > <:dotmid:611226754123563008> Leaving will reset your levels and require reverification. Leaving repeatedly will result in a ban. \n > <:dotdark:611226752466813040> Mass pinging unnecessarily will result in a ban. \n > <:dotmid:611226754123563008> Welcoming new members and saying hello to others is common courtesy here. Being cliquey is discouraged. Be nice to others, be nice to yourself. \n<a:pinkstar:663174593376419890> `Rule 4` **Channels** \n > <:dotmid:611226754123563008> <#514550733732053012> is strictly SFW. NSFW topics belong in <#529879816208384010>. \n > <:dotdark:611226752466813040> Keep channels on topic. Check channel descriptions for more details. \n > <:dotmid:611226754123563008> Our NSFW channels are for lvl 20+ members only. Inactivity in other channels or creepy behavior will get permissions revoked. NSFW permissions are granted at staff discretion, please dm staff for details. \n<a:pinkstar:663174593376419890> `Rule 5` **Advertising** \n > <:dotdark:611226752466813040> Self advertisement is not allowed, this includes dm advertisements. Asking for followers on social media and posting social media profiles are also prohibited. \n > <:dotmid:611226754123563008> No name dropping non-partnered servers or slandering partnered servers. \n<a:pinkstar:663174593376419890> `Rule 6` **Terms of Service** \n > <:dotdark:611226752466813040> Do not violate Discord's Terms of Service. \n > <:dotmid:611226754123563008> Doing so will result in staff reporting you to discord, as well as getting banned from here.")
		await information.send(file=discord.File("src/images/Moderation_-_1000_wd.png"))
		await information.send(f">>> <a:pinkstar:663174593376419890> Three warnings will result in a ban. While each situation is different, it is important to report situations that are against our rules. Please DM <@622553812221296696> with `/report <message>`. Images can be included if `/report` is sent in the text. If the situation is sensitive please DM a staff member. \n \n <a:pinkstar:663174593376419890> With all of that said, the server owner has the right to ban you for whatever they feel necessary. \n \n <a:pinkstar:663174593376419890> Inactive people will be pinged by staff in order to be checked in on, failure to answer to multiple pings will result in a kick for being a lurker.")
		await information.send(file=discord.File("src/images/Verification_-_1000_wd.png"))
		await information.send(">>> Verification of being 18+ ensures the security and safety of our members and our community as a whole from catfishing or other identity-related issues. To verify, send the items detailed below to <@622553812221296696>. You are able and encouraged to delete these pictures after verifying. \n \n`First Photo` You holding a piece of paper/sticky note with our server name, your discord tag (Name#0001), and the current date (MM/DD/YYYY). \n \n`Second Photo` A picture of your blurred-out ID with only your DOB and photo showing. All other information should be crossed out.")
		await information.send(file=discord.File('src/images/image0.jpg'))
		await information.send(file=discord.File('src/images/Partners_-_1000_wd.png'))
		await information.send("We will partner with servers regardless of member count. If your server follows the requirements below, please contact <@291682666246307841> or <@381507393470857229>. \n > <:dotdark:611226752466813040> We will not ping, ever. \n > <:dotmid:611226754123563008> All NSFW content must be behind a wall of verification. \n > <:dotdark:611226752466813040> Must follow Terms of Service. \n > <:dotmid:611226754123563008> If you wish to stay as a representative of your server, you must verify. \n > <:dotdark:611226752466813040> If your link expires, it will be deleted. \n > <:dotmid:611226754123563008> All partners must follow the rules of the server, no exceptions will be made.")
		await information.send(file=discord.File('src/images/Levels_-_1000_wd.png'))
		await information.send("Levels are obtained by being active in channels. \n > <:dotdark:611226752466813040> **lvl 10** add reactions, access selfies, museum, and vc \n > <:dotmid:611226754123563008> **lvl 20** create instant invite, image perms \n > <:dotdark:611226752466813040> **lvl 30** check audit log, link perms \n > <:dotmid:611226754123563008> **lvl 40** select a color from roles \n > <:dotdark:611226752466813040> **lvl 50** go live perms")
		await information.send(file=discord.File('src/images/Extra_-_1000_wd.png'))
		await information.send(embed=extra)


@bot.command()
@is_staff()
async def flashfuzzies(ctx, onoff : str, chnnl : typing.Optional[discord.TextChannel]):
	with open('src/data/fuzzies.json', 'r') as json_f_r:
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

			with open('src/data/fuzzies.json', 'w') as json_f_w:
				json.dump(fuzz_dict, json_f_w)
		else:
			fuzz_dict['onoff'] = False
			await ctx.send('Fuzzies has been turned off')
			try: 
				bot.remove_cog('fuzzies')
			except:
				pass
			with open('src/data/fuzzies.json', 'w') as json_f_w:
				json.dump(fuzz_dict, json_f_w)
	elif old_onoff == onoff:
		if old_onoff:
			await ctx.send('Fuzzies is already turned on')
		else: 
			await ctx.send('Fuzzies is already off')


bot.run(token)




