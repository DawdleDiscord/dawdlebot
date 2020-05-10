import discord
from discord.ext import commands
import datetime

class db_pins(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.excluded_channels = [514556004822941696, 600720406902734858, 612399078525108253, 564613278874075166]

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):


		if payload.emoji.id == 491736157844144129 and payload.guild_id == 475584392740339712 and not payload.channel_id in self.excluded_channels:
			korbIndex = 3
			dawdle = self.bot.get_guild(475584392740339712)
			srcChannel = dawdle.get_channel(payload.channel_id)
			pinchannel = dawdle.get_channel(623016818709233678)
			pinEmoj = await dawdle.fetch_emoji(491736157844144129)
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
							embedmess = discord.Embed(title="",value="",color=0xffb6c1,timestamp = srcMess.created_at)
							embedmess.set_thumbnail(url=r.message.author.avatar_url)
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
