import discord
from discord.ext import commands
from .db_checks import is_mod
import datetime
from .db_converters import SmartMember,SmartRole
import asyncio

class db_roles(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.group()
	@is_mod()
	async def roles(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.send('Invalid roles command')

	@roles.command()
	async def color(self, ctx, role : SmartRole, newcolor : discord.Colour):
		oldcolor = role.color
		await role.edit(color=newcolor)
		returnEmbed = discord.Embed(title=f"Changed the role color for {role.name} to {str(newcolor)}. Old color: {str(oldcolor)}.",color=newcolor)
		await ctx.send(embed=returnEmbed)

	@roles.command()
	async def mentionable(self, ctx,*, role : SmartRole):
		if role.mentionable:
			await role.edit(mentionable = False)
			roleEmbed = discord.Embed(title= f"{role} is no longer mentionable.", color = 0xffb6c1)
		else:
			await role.edit(mentionable = True)
			await ctx.send(f"{role} is now mentionable.")
			roleEmbed = discord.Embed(title = f"{role} is now mentionable.",color = 0xffb6c1)
		await ctx.send(embed=roleEmbed)


	@roles.command()
	async def sidebar(self, ctx,*, role : SmartRole):
		if role.hoist:
			await role.edit(hoist=False)
			message = f"{role} will no longer show on the sidebar"
		else:
			await role.edit(hoist=True)
			message = f"{role} will now show on the sidebar"
		roleEmbed =discord.Embed(title = message, color = 0xffb6c1)
		await ctx.send(embed=roleEmbed)

	@roles.command()
	async def name(self, ctx, role : SmartRole,*, newname : str):
		oldname = role.name
		await role.edit(name = newname)
		returnEmbed = discord.Embed(title= f"`{oldname}` was changed to `{newname}`")
		await ctx.send(embed=returnEmbed)

	@roles.command()
	async def position(self, ctx, role : SmartRole, newposition : int):
		oldposition = role.position
		await role.edit(position = newposition)
		returnEmbed = discord.Embed(title = f"{role} was moved to position {newposition}")
		await ctx.send(embed=returnEmbed)

	@roles.command()
	async def kick(self, ctx, role : SmartRole, hours : int):
		dawdle = ctx.guild
		unverifiedrole = dawdle.get_role(479410607821684757)
		dotrole = dawdle.get_role(587397534469718022)
		if role == unverifiedrole or role == dotrole:
			mem_to_kick = []
			time_seconds = hours*3600
			for mem in role.members:
				joined_duration = (datetime.datetime.utcnow() - mem.joined_at)
				joined_duration_sec = joined_duration.days*86400 + joined_duration.seconds
				if joined_duration_sec > time_seconds:
					mem_to_kick.append(mem)
			await ctx.send(f'Kick {len(mem_to_kick)} members with the {role.mention} role who joined before the past {hours} hours? (yes/no)')
			def check(m):
				return m.author == ctx.author and m.channel == ctx.channel and (m.content.lower() == "yes" or m.content.lower() == "no")
			try:
				confirm = await self.bot.wait_for('message',check=check,timeout=60.0)

			except asyncio.TimeoutError:

				await ctx.send('Kick timed out.')

			else:
				if confirm.content.lower() == "yes":
					for mem in mem_to_kick:

						await dawdle.kick(user=mem)
						await ctx.send(f'Kicked {mem.name}')

					await ctx.send('Done kicking')

				else:
					await ctx.send('Kick cancelled.')
		else:
			await ctx.send(f"You can only kick {unverifiedrole.mention} or {dotrole.mention}.")

	@roles.command()
	async def info(self, ctx,*, role : SmartRole):
		infoEmbed = discord.Embed(title = "", description = "", color = role.color)
		infoEmbed.add_field(name="Name", value = role.mention)
		infoEmbed.add_field(name="Number of Members", value = len(role.members))
		infoEmbed.add_field(name="Color", value=role.color)
		infoEmbed.add_field(name = "Mentionable", value = role.mentionable)
		infoEmbed.add_field(name = "Sidebar", value = role.hoist)
		infoEmbed.add_field(name = "Position", value=role.position)
		infoEmbed.set_footer(text=role.id)
		await ctx.send(embed=infoEmbed)

	@roles.command()
	async def give(self, ctx, role : SmartRole, *, member : SmartMember):

		await member.add_roles(role)
		returnEmbed = discord.Embed(title =f"Gave {role} role to {member}", color = 0xffb6c1)
		await ctx.send(embed=returnEmbed)

	@roles.command()
	async def remove(self, ctx, role : SmartRole, *, member : SmartMember):

		await member.remove_roles(role)
		returnEmbed = discord.Embed(title = f"Removed {role} role from {member}", color = 0xffb6c1)
		await ctx.send(embed=returnEmbed)

	async def cog_command_error(self, ctx, error):

		if isinstance(error, commands.BadArgument):
			await ctx.send('I could not find this role or member.')
		elif isinstance(error, commands.CheckFailure):
			await ctx.send('You do not have permissions to do this.')
		else:
			await ctx.send(f'Error: {str(error)}')
			print(error)
