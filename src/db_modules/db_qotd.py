import discord
import json
import datetime
from .db_checks import is_mod

from discord.ext import commands,tasks

class qotd(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
		self.qotdcheck.start()
	@commands.group()
	@is_mod()
	async def qotd(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.send('Invalid qotd command')

	@qotd.command()
	@is_mod()
	async def add(self, ctx, *, question : str):
		with open('src/data/qotd.json', 'r') as json_file_r0:
			qotdlist = json.load(json_file_r0)

		qotdlist.append(question)

		with open('src/data/qotd.json', 'w') as json_file_w0:
			json.dump(qotdlist,json_file_w0)

		await ctx.send('Question added!')

	@qotd.command()
	async def get(self, ctx, num : int):
		with open('src/data/qotd.json', 'r') as json_file_r1:
			qotdlist = json.load(json_file_r1)
		qotdReq = qotdlist[:num]
		qotdReqStr = ''
		nDone = False
		for n in range(num):
			qotdReqStr += f'[{n+1}] {qotdlist[n]} \n'
			if n == (len(qotdReq) - 1):
				break
		#qotdReqStr = '\n<a:flashingstars:598698378359996419> '.join(qotdReq)
		qotdEmbed = discord.Embed(title = 'QOTD', description = qotdReqStr, color=0xffb6c1)
		await ctx.send(embed=qotdEmbed)

	@get.error
	async def get_error(self,ctx, error):
		if isinstance(error,commands.errors.CommandInvokeError):
			await ctx.send("You don't have any questions set up!")

	@qotd.command()
	async def remove(self, ctx, num : int):
		with open('src/data/qotd.json', 'r') as json_file_r3:
			qotdlist = json.load(json_file_r3)

		await ctx.send(f'Are you sure you want to delete the following question? (yes/no)\n "{qotdlist[num-1]}"')
		def qotd_check(m):
			return m.author == ctx.author and m.channel == ctx.channel and (m.content.lower() == "yes" or m.content.lower() == "no")
		try:
			confirm = await self.bot.wait_for('message',check=qotd_check,timeout=60.0)
		except asyncio.TimeoutError:
			await ctx.send('QOTD delete request timed out.')
		else:
			if confirm.content.lower() == 'yes':
				del qotdlist[num-1]

				await ctx.send('question deleted')

			else:
				await ctx.send('deletion cancelled')

		with open('src/data/qotd.json', 'w') as json_file_w3:
			json.dump(qotdlist,json_file_w3)

	@qotd.command()
	async def edit(self, ctx, num : int):
		with open('src/data/qotd.json', 'r') as json_file_r4:
			qotdlist = json.load(json_file_r4)

		await ctx.send(f'replace the following question by typing your new question below\n "{qotdlist[num-1]}"')
		def qotd_check(m):
			return m.author == ctx.author and m.channel == ctx.channel
		try:
			newq = await self.bot.wait_for('message',check=qotd_check,timeout=60.0)
		except asyncio.TimeoutError:
			await ctx.send('QOTD edit request timed out.')
		else:
			qotdlist[num-1] = newq.content
			await ctx.send('question edited')

		with open('src/data/qotd.json', 'w') as json_file_w3:
			json.dump(qotdlist,json_file_w3)

	@qotd.command()
	async def post(self, ctx):
		dawdle = ctx.guild
		with open('src/data/qotd.json', 'r') as json_file_r5:
			qotdlist = json.load(json_file_r5)

		if qotdlist:
			qotdchannel = dawdle.get_channel(687707466179411981)
			qotdbanner = discord.File("src/images/qotdbanner.png")
			await qotdchannel.send(file=qotdbanner)
			qotdbanner = discord.File("src/images/qotdbanner.png")
			allpins = await qotdchannel.pins()
			for mess in allpins:
				if mess.author.bot:
					await mess.unpin()
			qotdmess = await qotdchannel.send(content=f'**Question of the Day**\n \n{qotdlist[0]}',file=qotdbanner)
			del qotdlist[0]
			await ctx.send('qotd posted!')
			await qotdmess.pin()

			with open('src/data/qotd.json', 'w') as json_file_w2:
					json.dump(qotdlist, json_file_w2)
		else:
			commandchannel = dawdle.get_channel(654787316665286714)
			await commandchannel.send("I didn't have a QOTD to post today! you'll have to do it manually")

	@tasks.loop(hours=1.0)
	async def qotdcheck(self):
		rightnow = datetime.datetime.utcnow()
		if rightnow.hour == 17:
			for guild in self.bot.guilds:
				if guild.name == 'dawdle':
					dawdle = guild
					break
			qotdchannel = dawdle.get_channel(687707466179411981)
			with open('src/data/qotd.json', 'r') as json_file_r2:
				qotdlist = json.load(json_file_r2)

			if qotdlist:
				qotdbanner = discord.File("src/images/qotdbanner.png")
				await qotdchannel.send(file=qotdbanner)
				qotdbanner = discord.File("src/images/qotdbanner.png")
				allpins = await qotdchannel.pins()
				for mess in allpins:
					if mess.author.bot:
						await mess.unpin()
				qotdmess = await qotdchannel.send(content=f'**Question of the Day** \n \n{qotdlist[0]}',file=qotdbanner)
				await qotdmess.pin()
				del qotdlist[0]

				with open('src/data/qotd.json', 'w') as json_file_w2:
					json.dump(qotdlist, json_file_w2)
			else:
				commandchannel = dawdle.get_channel(654787316665286714)
				await commandchannel.send("I didn't have a QOTD to post today! you'll have to do it manually")
