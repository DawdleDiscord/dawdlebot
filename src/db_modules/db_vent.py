import discord
from discord.ext import commands
import datetime

class db_vent(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def vent(self, ctx, *,vent_text : str):	
		dawdle = self.bot.get_guild(475584392740339712)
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
	async def vent_error(self, ctx,error):
		if isinstance(error,commands.errors.MissingRequiredArgument):
			await ctx.send('It looks like you are sending a vent. You need text after the `/vent`!')

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if payload.channel_id == 623016717429374986:
			dawdle = self.bot.get_guild(475584392740339712)
			srcChannel = dawdle.get_channel(payload.channel_id)
			verifEmoj = payload.emoji
			ventChannel = dawdle.get_channel(514561071441248266)
			ventMess = await srcChannel.fetch_message(payload.message_id)
			if ventMess.embeds and ventMess.embeds[0].title=='Vent' and (verifEmoj.id == 609771973341610033 or verifEmoj.id == 609771973102534687):
				for vr in ventMess.reactions:
					if vr.emoji == verifEmoj and vr.count == 2:
						if verifEmoj.id == 609771973341610033:
							embedVent = ventMess.embeds[0]
							ventnum = 1
							async for dmess in ventChannel.history(limit=200):
								if dmess.author.bot and dmess.embeds and len(dmess.embeds[0].title) > 5:
									ventnum = int(dmess.embeds[0].title[16:]) + 1
									break

							embedVent.title = 'Anonymous Vent #'+str(ventnum)
							embedVent.set_footer(text='')
							await ventChannel.send(embed=embedVent)
						elif verifEmoj.id == 609771973102534687:
							ventMemb = await dawdle.fetch_member(ventMess.embeds[0].footer.text)
							await ventMemb.send('<a:weewoo:598696151759192085> **Anonymous Venting** <a:weewoo:598696151759192085> \n \nHi I’m Dawdle! I’m here to forward any anonymous vents to our <#514561071441248266> channel. Some things before we get started is that this is entirely anonymous; staff will not see your name unless you do something that warrants us needing to know who you are. Please also note that this is __not__ a confessions bot and any sort of messages will be denied. This is meant for a more comfortable form of venting! Please read on for rules and instructions.  \n \n <a:weewoo:598696151759192085> **Anonymous Venting Rules** <a:weewoo:598696151759192085> \n \n <a:tinyheart:546404868529717270> 1. Any vent about another person in the server will be immediately denied. \n \n <a:tinyheart:546404868529717270> 2. Overtly sexual or explicit vents are not allowed. \n \n <a:tinyheart:546404868529717270> 3. __Dawdle rules apply__. Any suicide/self-harm references will be denied. \n \n <a:tinyheart:546404868529717270> 4. If you wish to vent and do not want any advice or responses write NA at the end of your vent. \n \n <a:tinyheart:546404868529717270> 5. While it is anonymous, staff can see user IDs and will warn/ban any user when necessary. \n \n <a:weewoo:598696151759192085> **Instructions on how to use** <a:weewoo:598696151759192085> \n \n <a:tinyheart:546404868529717270>  DM <@622553812221296696> using this format: \n >>> `/vent Message` \n \n `example:` /vent Hello I am venting. \n \n__You will get a confirmation message if the vent is sent to staff.__ If you do not get the confirmation message then you made a mistake in the command and should try again.')
