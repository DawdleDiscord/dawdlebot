import discord
import json
import typing
import asyncio
import random
from discord.ext import commands, tasks
from .db_checks import is_mod
# -*- coding: utf-8 -*-
#Target structure: trivlist{ question: { correct: <correct>, other: [<others>] }


class db_trivia(commands.Cog):
    def __init__(self, bot): #I'm not exactly sure what this does yet so I'm just leaving it here
        self.bot = bot

        with open("src/data/trivia.json", "r") as json_file:
            try:
                self.trivlist = json.load(json_file)
            except json.decoder.JSONDecodeError:
                print ("Currently no trivia!")
                self.trivlist = {}

    def save_json_dict(self, dict):
        with open("src/data/trivia.json", "w") as json_file:
            json.dump(dict, json_file)

    @commands.group()
    @is_mod()
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
                reaction, user = await self.bot.wait_for('reaction_add', check = trivia_check, timeout = 60)
            except asyncio.TimeoutError:
                triviaEmbed.title = f"{ctx.author.name}'s game timed out."
                await triviaMess.edit(embed=triviaEmbed)
            else:
                index = reactionlist.index(str(reaction.emoji))
                if answers[index] == self.trivlist[question]["correct"]:
                    responseEmbed = discord.Embed(title = f"<:pinkcheck:609771973341610033> {ctx.author.name} is correct!", color =  0xffb6c1)
                    responseEmbed.add_field(name = "Question", value = question)
                    responseEmbed.add_field(name = "Your answer", value = answers[index])
                #    triviaEmbed.title = f"<:pinkcheck:609771973341610033> {ctx.author.mention} is correct!"
                    await triviaMess.clear_reactions()
                    await triviaMess.edit(embed=responseEmbed)

                else:
                    responseEmbed = discord.Embed(title = f"<:pinkx:609771973102534687> {ctx.author.name} is incorrect.", color =  0xffb6c1)
                    responseEmbed.add_field(name = "Question", value = question)
                    responseEmbed.add_field(name = "Your answer", value = answers[index])
                    #triviaEmbed.title = f"<:pinkx:609771973102534687> {ctx.author.mention} is incorrect"
                    await triviaMess.clear_reactions()
                    await triviaMess.edit(embed=responseEmbed)



    @trivia.command()
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
                confirmation.add_field(name = "Question", value = question, inline = False)
                confirmation.add_field(name = "Correct answer", value = correct, inline = False)
                confirmation.add_field(name = "Wrong answer", value = "\n".join(wrong), inline = False)
                await ctx.send(embed = confirmation)
                await UI.delete(delay=1)

    @trivia.command() #Simply lists all trivia. Put an @ismod here
    async def list(self, ctx):
        embed = discord.Embed(title="List of Questions", color=0xffb6c1)
        n = 1
        for i in self.trivlist:
            embed.add_field(name="[%r]"%(n), value="%r"%(i))
            n = n + 1
        embed.add_field(name="Controls", value = "Type ~trivia edit <Index> to edit a question!", inline = True)
        await ctx.send(embed=embed)


    @trivia.command() #Accesses the editing UI
    async def edit(self, ctx, index : int):
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
        await UI.add_reaction('✔')#('<:pinkcheck:609771973341610033>')
        await UI.add_reaction('❌')#('<:pinkx:609771973102534687>')
        await UI.add_reaction('1️⃣')
        await UI.add_reaction('2️⃣')
        await UI.add_reaction('3️⃣')
        await UI.add_reaction('4️⃣')
        n=1
        while n != 2 : #I'm worried about this, might be worth checking it with Amer [Is there a better way to loop using async or something]
            try:
                reaction, user = await self.bot.wait_for('reaction_add',timeout = 60)
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
                        if (str(k.emoji)) == '✔':
                            self.save_json_dict(self.trivlist)
                            await ctx.send ("Saved!")
                            await message.delete(delay = 1)
                            n=2 #Must be a better way of leaving a loop but meh
                            break
                        elif (str(k.emoji)) == '❌':
                            del self.trivlist[Active]
                            self.save_json_dict(self.trivlist)
                            await ctx.send("Deleted!")
                            await message.delete(delay = 1)
                            n=2
                        elif (str(k.emoji)) == '1️⃣':
                            response = await EditAnswer(self, 0, reaction.message, embed)
                            self.trivlist[Active]["correct"]= response
                            await reaction.remove(user)
                            break
                        elif (str(k.emoji)) == '2️⃣':
                            response = await EditAnswer(self, 1, reaction.message, embed)
                            self.trivlist[Active]["wrong"][0]= response
                            await reaction.remove(user)
                            break
                        elif (str(k.emoji)) == '3️⃣':
                            response = await EditAnswer(self, 2, reaction.message, embed)
                            self.trivlist[Active]["wrong"][1]= response
                            await reaction.remove(user)
                            break
                        elif (str(k.emoji)) == '4️⃣':
                            response = await EditAnswer(self, 3, reaction.message, embed)
                            self.trivlist[Active]["wrong"][2]= response
                            await reaction.remove(user)
                            break

    @edit.error
    async def trivia_edit_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Question index needed! Use `~trivia list` to see the index for the queston you'd like to edit.")



    #def Trivia(): #Handles the actual trivia channel
