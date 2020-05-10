import discord
from discord.ext import commands
import datetime
import math

class db_VCtrack(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.userAndDate = {}
		self.botStartup = datetime.datetime.utcnow()

	@commands.Cog.listener()
	async def on_voice_state_update(self,member, before, after):
		dawdle = member.guild

		musicchannel = dawdle.get_channel(479408746955669524)
		afkchannel = dawdle.get_channel(533325041723506688)
		#Check if they joined a voice channel
		if before.channel is None and after.channel is not None and after.channel != musicchannel and after.channel != afkchannel:
			currentTime = datetime.datetime.utcnow()
			#Set the time for when they joined
			self.userAndDate[member.id] = currentTime
		#Check if they left a voice channel
		elif (before.channel is not None and after.channel is None and before.channel != musicchannel and before.channel != afkchannel):
			#Set time for when they left
			currentTime = datetime.datetime.utcnow()
			#Set the time for when they joined to bot startup in case of bot crashing, if they are in the list
			#Set the time for when they actually joined
			lastJoin = self.botStartup
			if member.id in self.userAndDate:
				lastJoin = self.userAndDate[member.id]
			else:
				self.userAndDate[member.id] = lastJoin
			#Math the fuck out of some time for easy time differentiating
			diff = currentTime - lastJoin
			#hours = math.floor(diff.seconds/3600)
			#minutes = math.floor((diff.seconds - hours * 3600)/60)
			#seconds = diff.seconds - hours * 3600 - minutes * 60
			minutes = math.floor(diff.seconds / 60)
			#Formatted string for minutes
			mt = "{} minutes".format(minutes)
			#If they've been in VC for more than 10 minutes send to staff
			if (minutes>=20 and self.userAndDate[member.id]):
				del self.userAndDate[member.id]
				noKoins = False
				verifChannel = dawdle.get_channel(623016717429374986)
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
			elif(minutes<20 and self.userAndDate[member.id]):
				del self.userAndDate[member.id]
