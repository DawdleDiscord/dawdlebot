import discord
from discord.ext import commands
from .db_checks import is_mod
import datetime
from .db_converters import SmartMember,SmartRole
import asyncio
import json

class db_roles(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		try:
			with open("src/data/rolewatch.json", "r") as json_file:
				self.rolewatch_list = json.load(json_file)
		except json.decoder.JSONDecodeError:
			print ("Currently no role watch list.")
			self.rolewatch_list = []

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
	async def give(self, ctx, member : SmartMember, *, role : SmartRole):

		await member.add_roles(role)
		returnEmbed = discord.Embed(title =f"Gave {role} role to {member}", color = 0xffb6c1)
		await ctx.send(embed=returnEmbed)

	@roles.command()
	async def take(self, ctx, member : SmartMember, *, role : SmartRole):

		await member.remove_roles(role)
		returnEmbed = discord.Embed(title = f"Removed {role} role from {member}", color = 0xffb6c1)
		await ctx.send(embed=returnEmbed)

	@roles.command()
	async def members(self, ctx, *,role : SmartRole):
		if len(role.members) > 0:
			member_mentions = (mem.mention for mem in role.members)
			returnEmbed = discord.Embed(title = f"Members of `{role}` role", description ="\n".join(member_mentions), color = 0xffb6c1)
		else:
			returnEmbed = discord.Embed(title = f"No members with `{role}` role.", color = 0xffb6c1)
		await ctx.send(embed = returnEmbed)

	@roles.group()
	async def watch(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.send('Invalid roles watch command')

	@watch.command()
	async def add(self, ctx, role : SmartRole):
		if role.id not in self.rolewatch_list:
			self.rolewatch_list.append(role.id)
			with open("src/data/rolewatch.json", "w") as json_file:
				json.dump(self.rolewatch_list, json_file)
			await ctx.send(f"`{role}` will now be watched.")
		else:
			await ctx.send("This role is already being watched.")

	@watch.command()
	async def remove(self, ctx, role : SmartRole):
		if role.id in self.rolewatch_list:
			self.rolewatch_list.remove(role.id)
			with open("src/data/rolewatch.json", "w") as json_file:
				json.dump(self.rolewatch_list, json_file)
			await ctx.send(f"`{role}` will no longer be watched.")
		else:
			await ctx.send("This role was already not watched.")	



	@watch.command()
	async def list(self, ctx):
		if self.rolewatch_list:
			rolewatch_list_str = []
			for id in self.rolewatch_list:
				rolewatch_list_str.append(ctx.guild.get_role(id).name)
			roleEmbed = discord.Embed(title = "Role Watch List", description = "\n".join(rolewatch_list_str), color = 0xffb6c1)
			await ctx.send(embed=roleEmbed)
		else:
			await ctx.send("No roles are being watched.")

	@commands.Cog.listener()
	async def on_member_update(self, before, after):
		if before.guild.id == 475584392740339712 and before.roles != after.roles:
			dawdle = before.guild
			dawdlechannel = dawdle.get_channel(623016717429374986)
			for id in self.rolewatch_list:
				irole = dawdle.get_role(id)
				if len(before.roles) > len(after.roles) and irole in before.roles and irole not in after.roles:
					roleEmbed = discord.Embed(title = "Role Update", description = f"{after.mention} no longer has the role `{irole}`.", color = 0xffb6c1)
					await dawdlechannel.send(embed=roleEmbed)
				elif len(before.roles) < len(after.roles) and irole not in before.roles and irole in after.roles:
					roleEmbed = discord.Embed(title = "Role Update", description = f"{after.mention} now has the role `{irole}`.", color = 0xffb6c1)
					await dawdlechannel.send(embed=roleEmbed)


	async def cog_command_error(self, ctx, error):

		if isinstance(error, commands.BadArgument):
			await ctx.send('I could not find this role or member.')
		elif isinstance(error, commands.CheckFailure):
			await ctx.send('You do not have permissions to do this.')
		else:
			await ctx.send(f'Error: {str(error)}')
			print(error)
