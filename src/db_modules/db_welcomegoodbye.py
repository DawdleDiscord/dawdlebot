import discord
from discord.ext import commands

class db_welcomegoodbye(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_member_join(self, member):
		dawdle = self.bot.get_guild(475584392740339712)
		unverifrole = dawdle.get_role(479410607821684757)
		foyerchannel = dawdle.get_channel(514554494495752204)
		if member.guild == dawdle:
			await foyerchannel.send(f'Welcome to dawdle, {member.mention}. Please read <#479407137060028449> to know how to access the rest of the server! Enjoy your stay.')
			await member.add_roles(unverifrole)
			try:
				await member.send(f'Hi {member.name}, welcome to Dawdle! We\'re so happy to have you! Please read <#479407137060028449> for details on how to get verified so that the rest of the server can be opened up to you.\n \nVerification is required to stay, but we understand if you can\'t do it right away. <#514550733732053012> is open for you to talk and say hi before you verify so you can meet some of the great folks that we have! \n \n**When you\'re ready to verify, please send your items to me (this bot) so that a member of staff can review it and you can access more of the server!**')
			except:
				pass
		countchannel = dawdle.get_channel(705498700771754054)
		await countchannel.edit(name=f'members: {dawdle.member_count}')

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		dawdle = self.bot.get_guild(475584392740339712)
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
		countchannel = dawdle.get_channel(705498700771754054)
		await countchannel.edit(name=f'members: {dawdle.member_count}')
