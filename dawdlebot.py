import discord
import os
from dotenv import load_dotenv
load_dotenv()
#sys.path.append('/src')
from discord.ext.commands import Bot
from discord.ext import commands, tasks
from src.db_modules import db_birthdays,db_moderation,db_qotd,db_fuzzies,db_clean,db_verification,db_members,db_inventory,db_profile,db_warns,db_streaks
from src.db_modules import db_autoreact,db_roles,db_vent,db_VCtrack,db_welcomegoodbye,db_pins,db_info,db_responses,db_trivia,db_miscellaneous,db_games
from src.db_modules import SmartMember
from src.db_modules import is_mod
import json,typing,datetime,asyncio,random

def main():

	intents = discord.Intents(messages=True, guilds=True, members=True, reactions=True, voice_states=True, presences=True)
	bot = Bot(command_prefix = '~', intents=intents)

	token = os.getenv('dawdletoken')

	bot.add_cog(db_birthdays(bot))
	bot.add_cog(db_moderation(bot))
	bot.add_cog(db_qotd(bot))
	bot.add_cog(db_verification(bot))
	bot.add_cog(db_clean(bot))
	bot.add_cog(db_members(bot))
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
	bot.add_cog(db_inventory(bot))
	bot.add_cog(db_profile(bot))
	bot.add_cog(db_warns(bot))
	bot.add_cog(db_streaks(bot))
	bot.add_cog(db_games(bot))

	@bot.event
	async def on_ready():
		for guild in bot.guilds:
			if guild.name == "dawdle":
				dawdle = guild
				break
		print(f'{bot.user} has connected to Discord!', f'{dawdle.name}(id: {dawdle.id})')
		game = discord.Game("use ~info dawdlebot to see my commands!")
		await bot.change_presence(activity=game)

	@bot.event
	async def on_message(message):
		await bot.process_commands(message)

	@bot.command()
	@is_mod()
	async def logout(ctx):
		await ctx.send("Logging out.")
		await bot.logout()

	bot.run(token)

if __name__ == '__main__':

	main()
