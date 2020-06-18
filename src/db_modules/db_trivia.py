import discord
import json
import typing
import asyncio
import random
from discord.ext import commands, tasks
from .db_checks import is_mod,in_dawdle
# -*- coding: utf-8 -*-
#credit this to tinnyf#4688

class db_trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with open("src/data/trivia.json", "r") as json_file:
            try:
                self.trivlist = json.load(json_file)
            except json.decoder.JSONDecodeError:
                print ("Currently no trivia!")
                self.trivlist = {}

        with open("src/data/triviastreak.json", "r") as json_file:
            try:
                self.streak_dict = json.load(json_file)
            except json.decoder.JSONDecodeError:
                print("No streak dictionary!")
                self.streak_dict = {}

    def save_json_dict(self, dict):
        with open("src/data/trivia.json", "w") as json_file:
            json.dump(dict, json_file)

    @commands.group()
    @in_dawdle()
    @commands.cooldown(1, 15.0, commands.BucketType.member)
    async def trivia(self, ctx):
        if ctx.subcommand_passed is not None and ctx.invoked_subcommand is None:
            await ctx.send("No such command found!")

        elif ctx.subcommand_passed is None:
            question = random.choice(list(self.trivlist.keys()))
            answers = [self.trivlist[question]["correct"]]+self.trivlist[question]["wrong"]
            random.shuffle(answers)
            answer_str_list = []
            for num in range(0,len(answers)):
                answer_str = f"[{num+1}] {answers[num]}"
                answer_str_list.append(answer_str)

            triviaEmbed = discord.Embed(title = f"{ctx.author.name} is playing Trivia", color = 0xffb6c1)
            triviaEmbed.add_field(name="Question", value=question)
            triviaEmbed.add_field(name="Answers", value="\n".join(answer_str_list))

            triviaMess = await ctx.send(embed=triviaEmbed)
            reactionlist = ["<:pinknum:603710351434973200>", "<:pinknum:603710368371703808>", "<:pinknum:603710385752899614>", "<:pinknum:603710402664333333>"]
            for r in reactionlist:
                await triviaMess.add_reaction(r)

            def trivia_check(reaction, user):
                return str(reaction.emoji) in reactionlist and user == ctx.author

            try:
                reaction, user = await self.bot.wait_for('reaction_add', check = trivia_check, timeout = 15)
            except asyncio.TimeoutError:
                responseEmbed = discord.Embed(title = f"<:pinkx:609771973102534687> {ctx.author.name} timed out.", color =  0xffb6c1)
                responseEmbed.add_field(name = "Question", value = question)
                await triviaMess.clear_reactions()
                await triviaMess.edit(embed=responseEmbed)
                currentStreak = 0
            else:
                index = reactionlist.index(str(reaction.emoji))
                if answers[index] == self.trivlist[question]["correct"]:
                    responseEmbed = discord.Embed(title = f"<:pinkcheck:609771973341610033> {ctx.author.name} is correct!", color =  0xffb6c1)
                    responseEmbed.add_field(name = "Question", value = question)
                    try:
                        currentStreak = self.streak_dict[str(ctx.author.id)] + 1
                    except KeyError:
                        currentStreak = 1
                    responseEmbed.add_field(name = "Streak", value = str(currentStreak))
                #    triviaEmbed.title = f"<:pinkcheck:609771973341610033> {ctx.author.mention} is correct!"
                    await triviaMess.clear_reactions()
                    await triviaMess.edit(embed=responseEmbed)

                else:
                    responseEmbed = discord.Embed(title = f"<:pinkx:609771973102534687> {ctx.author.name} is incorrect.", color =  0xffb6c1)
                    responseEmbed.add_field(name = "Question", value = question)
                    #triviaEmbed.title = f"<:pinkx:609771973102534687> {ctx.author.mention} is incorrect"
                    await triviaMess.clear_reactions()
                    await triviaMess.edit(embed=responseEmbed)
                    currentStreak = 0

            self.streak_dict[str(ctx.author.id)] = currentStreak
            with open("src/data/triviastreak.json", "w") as json_file:
                json.dump(self.streak_dict, json_file)

    @trivia.command(aliases = ['lb'])
    async def leaderboard(self, ctx):
        sorted_lb = sorted(self.streak_dict.items(), key=lambda x: x[1], reverse=True)

        lb_str_list = []
        rank = 1
        for strk in sorted_lb:
            member = ctx.guild.get_member(int(strk[0]))
            if member and strk[1] > 0:
                lb_str = f"[{rank}] {member}".ljust(24)
                lb_str = lb_str+str(strk[1])
                lb_str_list.append(lb_str)
                rank += 1
            else:
                del self.streak_dict[strk[0]]
                with open("src/data/triviastreak.json", "w") as json_file:
                    json.dump(self.streak_dict, json_file)

        lbEmbed = discord.Embed(title = "Trivia Streak Leaderboard", description = "```"+"\n".join(lb_str_list)+"```", color = 0xffb6c1)
        await ctx.send(embed = lbEmbed)



    @trivia.command()
    @is_mod()
    async def add(self, ctx, *,question: str):
        embed = discord.Embed(title = question, color=0xffb6c1)
        embed.add_field(name = 'Prompt', value = 'Please input the correct answer to the question or type cancel to leave this menu')
        UI= await ctx.send(embed=embed)
        def triv_response(message):
            return message.author == ctx.author and message.channel == ctx.channel
        try:
            response = await self.bot.wait_for('message', check = triv_response, timeout = 120.0)
        except asyncio.TimeoutError:
            await ctx.send('Response timed out')
            await UI.delete(delay=1)
        else:
            if response.content.lower()== "cancel":
                await ctx.send('Command canceled')
                await UI.delete
            else:
                correct = response.content #not sure this is needed but I think it's safe to do it
                embed.add_field(name= 'Correct', value = response.content)
                embed.set_field_at(0, name = 'Prompt', value = 'Please input the incorrect answers to the question or type cancel to leave this menu')
                await UI.edit(embed=embed)
                wrong = []
                while len(wrong) < 3:
                    try:
                        other = await self.bot.wait_for('message', check = triv_response, timeout = 120.0)
                    except asyncio.TimeoutError:
                        await ctx.send('Response timed out')
                        await UI.delete(delay=1)
                    else:
                        if other.content.lower()== "cancel":
                            await ctx.send('Command canceled')
                            await UI.delete(delay=1)
                        else:
                            embed.add_field(name = 'Incorrect answer', value = other.content)
                            await UI.edit(embed=embed)
                            wrong.append(other.content)
                Answers = {"correct":correct, "wrong": wrong} #Assembles a list of answers for a given question
                self.trivlist[question] = Answers
                self.save_json_dict(self.trivlist)
                confirmation = discord.Embed(title = "Question added!", color=0xffb6c1)
                confirmation.add_field(name = "Question", value = question)
                confirmation.add_field(name = "Correct answer", value = correct)
                confirmation.add_field(name = "Wrong answer", value = "\n".join(wrong))
                index = len(self.trivlist)
                confirmation.add_field(name= "Index", value = index)
                await ctx.send(embed = confirmation)
                await UI.delete(delay=1)

    @trivia.command() #Simply lists all trivia. Put an @ismod here
    @is_mod()
    async def list(self, ctx):

        embedList = []
        nembeds = int(len(self.trivlist)/25) + 1
        for n in range(1,nembeds+1):
            currentEmbed = discord.Embed(title = f"List of Questions {n}", color=0xffb6c1)
            i = 1
            for quest in self.trivlist:
                if 25*n - i >= 0 and 25*(n-1) - i < 0:
                    currentEmbed.add_field(name = str(i), value = f"{quest}")
                i += 1
            embedList.append(currentEmbed)

        embedIndex = 0
        listmess = await ctx.send(embed = embedList[embedIndex])
        await listmess.add_reaction("<a:pinkarrowleft:722535337531932742>")
        await listmess.add_reaction("<a:pinkarrowright:722927504373055548>")
        def resp_check(reaction, user):
            return (str(reaction.emoji) == "<a:pinkarrowright:722927504373055548>" or str(reaction.emoji) == "<a:pinkarrowleft:722535337531932742>") and not user.bot
        keepGoing = True
        while keepGoing:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check = resp_check, timeout = 120)
            except asyncio.TimeoutError:
                keepGoing = False
                await listmess.clear_reactions()
            else:
                await reaction.remove(user)
                if str(reaction.emoji) == "<a:pinkarrowright:722927504373055548>":
                    try:
                        embedIndex = embedIndex + 1
                        await listmess.edit(embed = embedList[embedIndex % len(embedList)])
                    except IndexError:
                        pass

                elif str(reaction.emoji) == "<a:pinkarrowleft:722535337531932742>":
                    try:
                        embedIndex = embedIndex - 1
                        await listmess.edit(embed = embedList[embedIndex % len(embedList)])
                    except IndexError:
                        pass

    @trivia.command() #Accesses the editing UI
    @is_mod()
    async def edit(self, ctx,*, question : typing.Union[int, str]):
        if isinstance(question,int):
            index = question
        else:
            m = 1
            for quest in self.trivlist:
                if question.lower() in quest.lower():
                    index = m
                    break
                m += 1

        n = 0
        Active = {}
        for i in self.trivlist:
            n = n + 1
            if n == index:
                Active = i
        embed = discord.Embed(title = Active, color=0xffb6c1)
        nn = 1
        embed.add_field(name = "Correct answer", value = "[%r]: %r "%(nn, self.trivlist[Active]["correct"]))
        for j in self.trivlist[Active]["wrong"]:
            nn = nn + 1
            embed.add_field(name = "Wrong answer", value ="[%r]: %r"%(nn, j))
        embed.add_field(name = "Controls", value = "React 1,2,3, or 4 to edit that element, tick to finish, or x to delete.")
        UI= await ctx.send(embed=embed)
        await UI.add_reaction('<:pinkcheck:609771973341610033>')#('<:pinkcheck:609771973341610033>')
        await UI.add_reaction('<:pinkx:609771973102534687>')#('<:pinkx:609771973102534687>')
#        await UI.add_reaction('<:AAAAHHH:586561885629841408>')
        reactionlist = ["<:pinknum:603710351434973200>", "<:pinknum:603710368371703808>", "<:pinknum:603710385752899614>", "<:pinknum:603710402664333333>"]
        await UI.add_reaction('<:pinknum:603710351434973200>')
        await UI.add_reaction('<:pinknum:603710368371703808>')
        await UI.add_reaction('<:pinknum:603710385752899614>')
        await UI.add_reaction('<:pinknum:603710402664333333>')
        n=1
        while n != 2 : #I'm worried about this, might be worth checking it with Amer [Is there a better way to loop using async or something]
            def react_check(reaction, user):
                return user == ctx.author and reaction.message.channel == ctx.channel
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check = react_check, timeout = 30)
            except asyncio.TimeoutError:
                await ctx.send('Timed out!')
                break
            else:
                message = reaction.message

                async def EditAnswer(self, index, message, embed):
                    embed.set_field_at(index, name = 'Active', value = 'Type the new answer below')
                    await message.edit(embed=embed)
                    def check (message):
                        return (ctx.author == message.author and message.channel == ctx.channel)
                    try:
                        response = await self.bot.wait_for('message', check = check, timeout = 120.0)
                    except asyncio.TimeoutError:
                        await ctx.send('Response timed out')

                    else:
                        temp = int(index + 1)
                        embed.set_field_at(index, name = 'Updated Answer', value = '[%r]: %r' %(temp,response.content))
                        await message.edit(embed=embed)
                        return(response.content)


                for k in reaction.message.reactions:
                    if k.count == 2:
                        response = 'temp'
                        if (str(k.emoji)) == '<:pinkcheck:609771973341610033>': #check
                            self.save_json_dict(self.trivlist)
                            await ctx.send ("Saved!")
                            await message.delete(delay = 1)
                            n=2 #Must be a better way of leaving a loop but meh
                            break
                        elif (str(k.emoji)) == '<:pinkx:609771973102534687>': #x
                            del self.trivlist[Active]
                            self.save_json_dict(self.trivlist)
                            await ctx.send("Deleted!")
                            await message.delete(delay = 1)
                            n=2
                        elif (str(k.emoji)) == '<:pinknum:603710351434973200>':
                            response = await EditAnswer(self, 0, reaction.message, embed) #1
                            self.trivlist[Active]["correct"]= response
                            await reaction.remove(user)
                            break
                        elif (str(k.emoji)) == '<:pinknum:603710368371703808>': #2
                            response = await EditAnswer(self, 1, reaction.message, embed)
                            self.trivlist[Active]["wrong"][0]= response
                            await reaction.remove(user)
                            break
                        elif (str(k.emoji)) == '<:pinknum:603710385752899614>': #3
                            response = await EditAnswer(self, 2, reaction.message, embed)
                            self.trivlist[Active]["wrong"][1]= response
                            await reaction.remove(user)
                            break
                        elif (str(k.emoji)) == '<:pinknum:603710402664333333>': #4
                            response = await EditAnswer(self, 3, reaction.message, embed)
                            self.trivlist[Active]["wrong"][2]= response
                            await reaction.remove(user)
                            break
#                        elif (str(k.emoji)) == '<:AAAAHHH:586561885629841408>':
#                            embed.title = reaction.message

    @edit.error
    async def trivia_edit_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Question index needed! Use `~trivia list` to see the index for the queston you'd like to edit.")

    @trivia.error
    async def trivia_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"You are on trivia cooldown. You can retry after {round(error.retry_after)} seconds.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("Check failed: Either you're trying this outside the server or you're using a mod-only command.")
        else:
            await ctx.send(f"Error: {str(error)}")
