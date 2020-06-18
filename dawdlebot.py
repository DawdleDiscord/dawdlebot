import discord
import os
from dotenv import load_dotenv
load_dotenv()
#sys.path.append('/src')
from discord.ext.commands import Bot
from discord.ext import commands, tasks
from src.db_modules import birthdays,moderation,qotd,fuzzies,clean,verification,members
from src.db_modules import db_autoreact,db_roles,db_vent,db_VCtrack,db_welcomegoodbye,db_pins,db_info,db_responses,db_trivia,db_miscellaneous
from src.db_modules import SmartMember

import json,typing

def main():

	bot = Bot(command_prefix = '~')

	token = os.getenv('dawdletoken')


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
	bot.add_cog(db_info(bot))
	bot.add_cog(db_responses(bot))
	bot.add_cog(db_trivia(bot))
	#bot.add_cog(fuzzies(bot))
	bot.add_cog(db_miscellaneous(bot))

	@bot.event
	async def on_ready():
		dawdle = get_server(bot.guilds,'dawdle')
		print(f'{bot.user} has connected to Discord!', f'{dawdle.name}(id: {dawdle.id})')
		game = discord.Game("use `~info` to learn more about the server!")
		await bot.change_presence(activity=game)


	@bot.event
	async def on_message(message):

		await bot.process_commands(message)



	bot.run(token)

if __name__ == '__main__':

	main()
