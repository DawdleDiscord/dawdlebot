import discord
from .db_checks import is_mod
from discord.ext import commands,tasks
import time
from .db_converters import SmartMember
import asyncio

class db_members(commands.Cog):
	def __init__(self,bot):
		self.bot = bot


	@commands.group()
	@is_mod()
	async def members(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.send('Invalid members command')

	@members.command()
	async def check(self, ctx):
		if ctx.guild:
			dawdle = ctx.guild
			verifiedrole = dawdle.get_role(481148097960083471)
			introchannel = dawdle.get_channel(514555898648330260)
			await ctx.send('Checking for roles and intros... this may take a bit.')
			def emoji_response(check):
				if check == True:
					return '<:pinkcheck:609771973341610033>'
				else:
					return '<:pinkx:609771973102534687>'
			for mem in verifiedrole.members:

				hasIntro = False

				async for mess in introchannel.history(limit=None):
					if mem == mess.author:
						hasIntro = True
						break

				age_roles = [481138497856602113, 480080787253755905, 481138992151003156, 481138740484505611]
				pronoun_roles = [551901787297284096, 551901739700322324, 551901812677017611, 836781368084004864]
				dm_roles = [479410113115979805, 479410060804751371, 479410091905253376]
				loc_roles = [481135072427376641, 481135146129424415, 481135185497423900, 481135221572501516, 481135414321610763, 481135465399844882, 481136198014861336]
				check_age, check_pronoun, check_dm, check_loc, has_dot = (False,)*5
				dot_role = dawdle.get_role(587397534469718022)

				for role in mem.roles:
					if role.id in age_roles: check_age = True
					if role.id in pronoun_roles: check_pronoun = True
					if role.id in dm_roles: check_dm = True
					if role.id in loc_roles: check_loc = True
					if role == dot_role: has_dot = True

				role_check = check_age and check_pronoun and check_dm and check_loc

				intro_emoji = emoji_response(hasIntro)
				role_emoji = emoji_response(role_check)
				if not mem.bot and (not hasIntro or not role_check):
					if has_dot:
						await ctx.send(f'{mem.mention} already has dot role. Intro: {intro_emoji} Roles: {role_emoji}')
					else:
						await mem.add_roles(dot_role)
						await ctx.send(f'Gave dot role to {mem.mention}. Intro: {intro_emoji} Roles: {role_emoji}')

			await ctx.send('Done checking for intros and roles')
	@members.command()
	async def clean(self, ctx):
		if ctx.guild:
			dawdle = ctx.guild
			message_clean_dict = {
				514555898648330260 : [], #intro
				514556004822941696 : [], #selfies
				514556101052858378 : []  #animals
			}
			to_send = ""
			delete_any = False
			await ctx.send("Beep boop calculating how much to delete...")
			def is_not_member(message) -> bool:
				return not isinstance(message.author,discord.Member)
			for ch_id, messages in message_clean_dict.items():
				channel = dawdle.get_channel(ch_id)
				async for mess in channel.history(limit=None):
					if is_not_member(mess):
						messages.append(mess)
						delete_any = True
				to_send += f"Will delete {len(messages)} messages from {channel.mention}\n\n"
			if delete_any:
				to_send += f"{ctx.author.mention}, do I proceed?"
				await ctx.send(to_send)
				def delete_response(m):
					return m.author == ctx.author and m.channel == ctx.channel and (m.content.lower() == "yes" or m.content.lower() == "no")
				try:
					response = await self.bot.wait_for("message",  check = delete_response, timeout = 60.0)
				except asyncio.TimeoutError:
					await ctx.send('Response timed out.')
				else:
					if response.content.lower() == "yes":
						async with ctx.typing():
							for ch_id, messages in message_clean_dict.items():
								channel = dawdle.get_channel(ch_id)
								try:
									for message in messages:
										await message.delete()
										time.sleep(3)
								except Exception as e:
									await ctx.send(f'Failed to delete posts in {channel.mention}. Reason: {e}')
								else:
									await ctx.send(f'Purged {len(messages)} posts in {channel.mention}')

							await ctx.send('Done cleaning.')
					else:
						await ctx.send("Clean canceled.")
			else:
				await ctx.send("Nothing for me to clean :(")
				
