import discord
import json
import datetime
from .db_checks import is_mod
from discord.ext import commands,tasks
from .db_converters import SmartMember

class birthdays(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
		self.birthdaycheck.start()
	
	def cog_unload(self):
		self.birthdaycheck.cancel()

	@tasks.loop(hours = 1.0)
	async def birthdaycheck(self):
		rightnow = datetime.datetime.utcnow()
		if rightnow.hour == 6:
			for guild in self.bot.guilds:
				if guild.name == 'dawdle':
					dawdle = guild
					break
			
			todaymonth = rightnow.month
			todayday = rightnow.day
			birthdayrole = dawdle.get_role(535390006374825984)
			for member in birthdayrole.members:
				await member.remove_roles(birthdayrole)
			with open('src/data/birthdays.json', 'r') as json_file_r0:
				bday_dict = json.load(json_file_r0)
			for memid in bday_dict:
				if bday_dict[memid]['month'] == todaymonth and bday_dict[memid]['day'] == todayday:
					membday = dawdle.get_member(int(memid))
					dawdlebotchannel = dawdle.get_channel(623016717429374986)
					await dawdlebotchannel.send(f"It's {membday.mention}'s birthday! Wish them happy birthday and give them koins.")
					await membday.add_roles(birthdayrole)

	@birthdaycheck.before_loop
	async def before_birthdaycheck(self):
		await self.bot.wait_until_ready()

	@commands.command(aliases=['bday'])
	async def birthday(self, ctx, day : int, month : int):
		dawdle = ctx.guild
		with open('src/data/birthdays.json', 'r') as json_file_r:
			bday_dict = json.load(json_file_r)
		if month > 0 and month < 13 and day > 0 and day < 32:
			if str(ctx.author.id) in bday_dict:
				await ctx.send(f'Your birthday was updated to {day}-{month}.')
			else:
				await ctx.send(f'Your birthday was added as {day}-{month}.')
			bday_dict[str(ctx.author.id)] = { 'day' : day,
											'month' : month}
			with open('src/data/birthdays.json', 'w') as json_file_w:
				json.dump(bday_dict, json_file_w)
		else:
			await ctx.send(f'Please enter a valid birthday in `<day> <month>` format.')

	@birthday.error
	async def birthday_error(self, ctx, error):
		if isinstance(error,commands.errors.MissingRequiredArgument) or isinstance(error,commands.errors.BadArgument):
			await ctx.send('Please enter your birthday as `<day> <month>`.')
		else:
			await ctx.send(f'I had an unknown error {str(error)}.')

	@commands.command(aliases=['addbday','addbd'])
	@is_mod()
	async def addbirthday(self, ctx, member : SmartMember, day : int, month : int):
		with open('src/data/birthdays.json', 'r') as json_file_r:
			bday_dict = json.load(json_file_r)
		if month > 0 and month < 13 and day > 0 and day < 32:
			if str(member.id) in bday_dict:
				await ctx.send(f'Birthday for {member.mention} was updated to {day}-{month}.')
			else:
				await ctx.send(f'Birthday for {member.mention} added as {day}-{month}.')
			bday_dict[str(member.id)] = { 'day' : day,
											'month' : month}
			with open('src/data/birthdays.json', 'w') as json_file_w:
				json.dump(bday_dict, json_file_w)
		else:
			await ctx.send(f'Please enter a valid birthday in `<day> <month>` format.')
	
	@addbirthday.error
	async def addbirthday_error(self, ctx, error):
		if isinstance(error,commands.errors.MissingRequiredArgument) or isinstance(error,commands.errors.BadArgument):
			await ctx.send('Please enter your birthday as `<day> <month>`.')
		else:
			await ctx.send(f'I had an unknown error {str(error)}.')


	@commands.command(aliases=['bdaymonth'])
	async def birthdaymonth(self, ctx, month : int):
		dawdle = ctx.guild
		bdaylist = []
		monthbdaydict = {}
		months = ['January', 'February', 'March', 'April', 'May',
					'June', 'July', 'August', 'September',
					'October', 'November', 'December']
		with open('src/data/birthdays.json', 'r') as json_file_2:
			bday_dict = json.load(json_file_2)
			for memid in bday_dict:
				if bday_dict[memid]['month'] == month:
					memname = dawdle.get_member(int(memid)).name
					memday = bday_dict[memid]['day']
					monthbdaydict[memname] = int(memday)
			for bd in sorted(monthbdaydict.items(), key=lambda x: x[1]):
				bdaylistname = f"❥ {bd[0]}"
				bdaylistname = bdaylistname.ljust(24)
				bdaylistname = bdaylistname+f"-{months[month-1][:3]} {bd[1]}"
				bdaylist.append(bdaylistname)
		s = '\n'
		
		if len(bdaylist) == 0:
			finalbdaylist = f'No birthdays in {months[month-1]}'
			await ctx.send(finalbdaylist)
		else:
			finalbdaylist = f"**Birthdays for {months[month-1]}** ```"+s.join(bdaylist)+"```"
			bdayEmbed = discord.Embed(title='',description = finalbdaylist,color=0xffb6c1)
			await ctx.send(embed=bdayEmbed)
	@birthdaymonth.error
	async def birthdaymont_error(self, ctx, error):
		await ctx.send('Error: Please enter a valid month')

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if member.guild.name == 'dawdle':
			dict_changed = False
			with open('src/data/birthdays.json', 'r') as json_file_r3:
				bday_dict = json.load(json_file_r3)
			try:
				del bday_dict[str(member.id)]
				dict_changed = True
			except KeyError:
				pass
			if dict_changed:
				with open('src/data/birthdays.json', 'w') as json_file_w3:
					json.dump(bday_dict, json_file_w3)

