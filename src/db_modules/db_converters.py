import discord
from discord.ext import commands
import asyncio

class SmartMember(commands.Converter):

	async def convert(self, ctx, arg):
		def try_int(string):
			try:
				int(string)
				return True
			except ValueError:
				return False
		def try_lower(string):
			try:
				return string.lower()
			except AttributeError:
				return ""
		is_id = try_int(arg)
		if is_id: 

			member = ctx.guild.get_member(int(arg))
			if member:
				return member
			else:
				raise commands.BadArgument
		elif ctx.message.mentions:
			return ctx.message.mentions[0]

		else:
	
			member_iterator = filter(lambda m: arg.lower() in str(m).lower() or arg.lower() in try_lower(m.nick), ctx.guild.members)
			memberlist = list(member_iterator)
			if len(memberlist) == 0:
				raise commands.BadArgument
			if len(memberlist) == 1:
				return memberlist[0]
			else:
				memberlist_str = []
				for mem in range(len(memberlist)):
					num = mem + 1
					mem_str = f"[{num}] {memberlist[mem]}"
					memberlist_str.append(mem_str)
				memberlistEmbed = discord.Embed(title="Select a member or type 'cancel'.", description = '\n'.join(memberlist_str), color=0xffb6c1)
				await ctx.send(embed=memberlistEmbed)

				def member_pick(m):
					return m.author == ctx.author and m.channel == ctx.channel and (try_int(m.content) or m.content.lower() == "cancel")
				try:
					confirm = await ctx.bot.wait_for('message', check=member_pick, timeout = 60.0)
				except asyncio.TimeoutError:
					await ctx.send('Member select timed out')
					raise commands.BadArgument
				else:
					if confirm.content.lower() == "cancel":
						await ctx.send('Selection canceled.')
						raise commands.BadArgument
					else:
						return memberlist[int(confirm.content) - 1]
