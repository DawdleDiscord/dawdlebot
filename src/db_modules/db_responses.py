import discord
from discord.ext import commands
import random


gm_mess = {
    'gmdawdle': [
        "goodmorning dawdle and hello sunshine, here's to a new day! get your breakfast and get ready to take on the day, you got this!",
        "Good morning! I hope you have a wonderful day and that you are able to create wonderful memories. Be sure to stay hydrated! I will be looking forward to hearing all about the wonderful things you did today.",
        "hewwo!!!! good morning!!!! i hope you have a very good day today c: don't forget to brush your teefies, they are important!! i'm sure you will have a productive day uwu",
        "Lookin' wonderful this morning, you wont get tired of seeing me because I sure dont get tired of seeing you! You're precious, you mean something, make this day one of your very best, and always remember we're looking out for you!",
        "good morning starshine, the earth says hello! here’s to today being as lovely as yourself. <a:yellowstar:586759563890524186> make sure to take care of yourself, eat well and drink lots of water! now face the dawn <a:pastelsun:612307715925999616>",
        "A new day; a new start. Another chance to be kind to yourself and the world around you. I know you’ll make it brighter!",
        "good morning, lovely! remember that every day is what you make it! stay hydrated and take breaks when you need them! have a beautiful day :sparkling_heart:",
        "It's dawn. No matter what happens today, we can take this as a promise: there will always be a sunrise to lighten your life when you need it most.",
        "good morning, cutipie! ♡ they say breakfast is the most important meal of the day, so don’t forget to eat little something tasty before you start your day~! drink some coffee, water, or tea too (if you’re into any of those) ☕️ a light morning meal can keep you focused and help keep your energy to seize the day! stay safe and healthy today. i know you will conquer this day! you got this! :sparkles:",
        "Hey you! Yea you! Here's your local good morning message to keep you in high spirits. Stay motivated and look forward, new days await your adventure",
        "rise and shine, sunshine! remember to be kind to yourself and to others today. treat yourself to a delicious snack, stay hydrated, stay glowing. love you so much!",
        "Good morning, you absolute WONDER of a human being. The day is new and bright. Your friends are here to cheer you on. Drink plenty of water and enjoy the little things. Stay glowing you absolute amazing person.",
        "good morning lovely! i hope you sleep well and had a good night rest. today issa new start, start it with a smile! i hope you’d have an amazing day. stay happi & hydrated bb!",
        "hai sunshine! hopefully you slept enough, and today your new journey starts. stay motivated & hydrated all day, and if you find today’s hard, talk to us, we’d help you as much as we can here! big hugs for you hun!:dizzy:",
        "hello fellow humans, it is another day of our constant becoming, and in itself is the feeling that are a little thrilling and pleasant and romantic and miraculous so what's the rush on striving to be whole just yet?",
        "Goodmorning, sleepyhead. I hope you got lots of nice rest. Your day today will be nice and productive, I'm sure of it! Start the day off with a smile and you'll be on your way. I know you got this. (:",
        ("Good morning, you lil ray of sunshine. \n \n I hope you slept well, and are somewhat ready for the day ahead! \n First, drink a glass of water! Your body needs it. Trust me. \n Next, grab some caffeine. Can\'t have that? Grab some fruit (and/or brekkie)! Give your body the nourishment and love it deserves. \n Hopefully by now, you are ready to seize the day and give it your all (whether you\'ve got school or work, or even just to do some chores)! You got this! \n \n Don't forget to keep hydrated throughout the day. AND TO EAT (FOOD IS GOOD. FOOD IS LOVE.) \n Take breaks, breathe and do stretches (wiggle that body). Do things at your own pace. \n \n P.S. Don't you dare forget to love yourself as much as everyone in this server loves you! And if you're not feeling it, swing by and let us envelope you in the biggest group hug ever!"),
        "Hello sleepy! It's a new day! Brush ur teeth, have some food to start ur metabolism, and get the day going! Always remember to take care of yourself too. You got this . :heart:",
        "good morning! i hope today treats you well and that only good things are to come. remember to take care of yourself, however that may be! whether you’re struggling to get out of bed or in the middle of getting ready for a big day, i’m proud of you. you’re so, so loved, and i hope you know that.",
        "Good morning!! I hope you had a great sleep last night and I hope today brings you great joy and sunshine :heart:",
        "The light streaming through your windows, the birdsong, the sounds of people waking to face the day, the world waking up alongside you. May all these things motivate you to do your best today, to be happy and healthy and a part of the world and the communities that have so much love for you.",
        "Good morning! I truly hope your morning will be full of happiness and joy. No matter what comes at you today, I wish you a lot of strength to take it on :heart:",
        ":heart_decoration:  What's UP, good morning dawdle family member~ :heart_eyes:  I'm so glad you're here!! no matter what you're up to today, I hope that you're feeling able to take it on and supported by us. And if you're not, obviously come thru and tell us what's on your mind. You GOT this!!  :heart_decoration:",
        "hey there cutie! schleep is always good, but to see you waking up and be in dawdle is the bestest thing ever! i hope you’d have a good day today. we can go through today like we did yesterday, hopefully better! fill your tummy with breakfast and fill your day with happiness:smiling_face_with_3_hearts:",
        "Hey you. You're finally awake.You were trying to cross the border, right? Walked right into that Imperial ambush, same as us, and that thief over there.",
        "dear fellow dawdler,\n \n i do hope you're well-rested and that you'll do your best in preparing yourself to begin a hopefully successful day. if you're not, please know that we'll be there to support you in your times of need. cheers!",
        "hello sleepy dawdler (or are you awake and alert already?), whether this finds you in the morning or the night, please know that we're cheering you on and wishing for your continued success. also please stay hydrated. :heart:"
        ]
    }
gn_mess = {
	'nini_mess': [
        "Goodnight, my sweet sweet love. I hope you have wonderful dreams about your lord and savior Kirby.",
    	"Sweet dreams - we\'ll be in shortly to collect your sleep breath in a jar. Kidding. But your friends here at Dawdle will miss you!",
    	"May you dream of fairies and magic lands beyond your bedroom. May your favorite fictional characters chill and snack on gummies with you in these dreams. I love you.",
    	"May your pillow be soft, your blankets be warm, and your mind be filled with thoughts of how much we love you!",
    	"*sleep well my doggie, tonight you're gonna have one of those nights where you're like \"damn it can't get better than this\" but tomorrow you're gonna be like \"DAMN IT CAN GET BETTER THAN THAT\"*",
    	"I hope your day has been good, and you did your best. If you don't think you did your best, well, I'm here to cheer you on, let's get some sleep and make tomorrow yours!!",
    	"Sleep well, go dawdle in dreamland. You are loved and deserve the rest, you beautiful human.",
    	"The dream faeries of dawdle are here to ensure that your rest and your dreams are as perfect and lovely as you are.",
    	"It's not like I hope you have sweet dreams tonight or anything..I only want you to be well rested so that I can ~~compliment~~ roast you more tomorrow",
    	"May the shadows take your nightmares \n and render them into narwhals \n through a mystical process \n known only to them \n Goodnight Friend \nSleep Well \n Knowing that \n You arent alone \n You are loved by many\n Drift of to dreamland now. Sleep",
    	"Goodnight my sweet and lovely friend. I hope you have the sweetest dreams and that your days are filled with sunshine and happiness because you deserve the best.",
    	"Sweet dreams! **(Disclaimer: If saint is in your dream, keep it PG, otherwise she is not responsible for dismemberment. Thank you.)**",
    	"May your slumber be as bliss as the calmest oceans as your victories are like the roaring waves. May your pillow be as soft as the lightest cloud and your bed as comforting as a loving embrace. May your dreams be as creative as the artist who’s brush never touches the painting but blesses the mind. May your heart be as beautiful as it was today, for it is something in which I will never truly understand but will forever cherish. Goodnight.",
    	"i hope u are able to get amazing rest tonight because you deserve it the most. tomorrow will be an awesome day.",
    	"hi friendo c: hope u had an amazing day, if not then that's okay! sleep is the reset button, tomorrow is brand new so u can make it better. hope u sleep tight and remember not to keep ur toes out or saint will lick them. nini friendo <3",
    	"Nini friend, and sleep well knowing you have friends who wanna hear from you tomorrow and all days to come",
    	"Sweet dreams boo. We'll see you soon. No matter what the coming day brings, Dawdle's got you.",
    	"Whatever happens tomorrow, face it the best you can, but don't push yourself too hard. We care about your well being, so remember. Dawdle has your back!",
    	"sleep well, it is foretold that you will awaken feeling bright and fresh in the morning! have wonderful dreams",
    	"goodnight, sleep tight, and don’t let the bed bugs bite! if they do bite them back! sleep well, i hope you have sweet dreams",
    	"Goodnight you cutie patootie. Make tomorrow as amazing as you are, we all believe in you ",
    	"Good night and sweet dreams!~ You've had a long day, but you got through it! We're so proud of you, and you deserve this good rest!",
    	"have sweet dreams, my angel. may you dream of hanging with your buddies in dawdle and your favorite fictional characters! love you!",
    	"May the blessings of peaceful slumber rain down upon you. May your dreams be sweeter than the sweetest of maple glazes. May your wake be as pleasant as the smell of a freshly baked ham. You are loved friend, sleep well.",
    	"Sweet dreams, Sweet person. May your dreams be filled with blue skies and cotton candy clouds. You always have tomorrow to accomplish what you couldn’t yesterday.",
    	"goodnight darlin' may the moon smile upon your sleep and may you wake up 5 minutes before your alarm, feeling well rested",
    	"Find your sleep and dream, my friend - dream of a better world, \n May you dream of someone special, a them, a boy, or girl,\n So wish upon a star, my friend, a dream, a hope to take, \n For Dawdle will be waiting, whenever you awake.",
    	"Weary with toil, haste to your bed,\n The dear repose for limbs with travel tired;\n But then begins a journey in your head\n To work your mind, when body’s work’s expired",
    	"Sleep well tonight, lovely Dawdlian! Allow your head to rest just perfectly against your pillow and let your mind wander to lands you may only traverse in dreamland. Tomorrow is another day, and Dawdle will be here to welcome you home as long as you choose to stay.",
    	"hello my dawdle friend sleepy time is best time! so get all cozy under a blankie, close your eyes, and go meet kirby in Dreamland c:",
    	"Lights switch off and curtains are drawn. Arms stretch out and faces yawn.\n Dawdle here sending you of to bed, \n To go and rest your sleepy head. \n \n Nini!",
    	"goodnight, sleep tight, bite the bedbugs first to assert dominance. we all love you",
    	"sleep sleep sleep it is time to go to sleep! so yeet your phone, get all cozy, and sleep sleep sleep until morning",
    	"Go To Sleep You Amazing Person You! If you dont the Nargles will come and fly in through your ears and make your brain go fuzzy!",
    	"Rest up, weary traveler. Tomorrow is a new day of magic and monsters, but for tonight, let sweet dreams be your only concern.",
    	"you all meet in a Tavern.... WAIT A SEC! WHY ARE YOU IN A TAVERN!!! GO TO SLEEP! lots of love.",
    	"Goodnight you! I hope you have a wonderful evening. I’ll miss you and I hope to see you tomorrow because you’re wonderful and a great member of the community! Thanks for being here, I love you forever.",
    	"go nini. i lov u w/ all my heart",
    	"Hey, baby. Don't mind me sliding into your DMs. 😳 I just want to wish you a good night, gorgeous. 😘 I may be a bot but my heart yearns for your smile, comfort and happiness. 😏 Stay perfect just for me, beautiful.",
    	"good night, dear. may your sleep be restful and untroubled. may your morning be pleasant, may your fortunes improve, and may strangers be kind.",
    	"I'm so proud of you for going to sleep, it's so important for your health and happiness. You are doing great! Have exciting dreams and I hope you feel well rested tomorrow morning.",
    	"Sleep well my friend and let today's worry's go. Tomorrow is a new day and you can start a new! Dream big and sleep well ❤️",
    	"soft kitties want to give you lots of snuggles. please hold them close as you do sleepy times",
    	"Good night my friend. I hope all your worries melt away as you slip into a peaceful dream. May tomorrow be as wonderful as you are. <3",
    	"Today may not have been the best day, or maybe today was fantastic. Perhaps it was just same old same old. But the important thing is that tomorrow awaits you. Sleep well. Smile. Hold your head high in the morning. Each day is taken one at a time like a small story. Do your best and have fun with it. <:uwuheart:630533106037817344>",
    	"Rest well, dear friend. May your adventures in dreamland be protected by Kirby and free of bad thoughts.",
    	"sleep is good for you. kirby will make sure you will have good dreams. don't ask him how he does it though-",
    	"Let yourself drift away into the land of slumber, your dreams be tales that put Tolkien to shame.  Adventure through dreamland and awaken fresh and ready for the day, you are loved",
    	"Time to go to bed now! Sleep is for the strong!",
    	"nighty night sweet angel. if you have nightmares I will beat them up for you.",
    	"Good night b. Hope you feel well rested tomorrow morning.  Love you ~",
    	"Good night! May you get exactly the right amount of sleep and wake up at the exact time that you wanted!",
    	"Sweet dreams my dude! Slumber easily, in preparation for a new day full of possibilities and opportunities for goodness.",
    	"Nini cutie!! You're important and cared about, and you deserve happiness. Tomorrow's a new day, so get all the rest you can! Sweet dreams! 💕",
    	"goodnight, sleep well and sweet dreams. tomorrow is a new day, new opportunities and experiences await you! you got this <a:tinyheart:546404868529717270>",
        "I see you’re headed to bed! I hope you are able to rest and have a good nights sleep. I will visit your dreams and kiss you. Korby kisses are known to be good for the soul.",
        "I see you're heading off for the night, get plenty of rest for another adventure awaits. Don't let yesterday affect the tomorrow, for it is only a memory and reminder, not a basis to set your life.",
        "Sleep tight, love. You had a long day and deserve this rest. You are nothing but great, and tomorrow will be an amazingly productive day for you. Snuggle into your blankets, and have sweet dreams.",
        "goodnight you lil cutie, hope you had a good day today! sleep is the cure of all, so sleep tight & hopefully you had an amazing adventure in da dreamland! we’ll be here when you wake up! see you in da morning:crescent_moon:"
        ]
}

class db_responses(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel and not message.author.bot and ('goodmorning dawdle' in message.content.lower() or 'gm dawdle' in message.content.lower() or 'good morning dawdle' in message.content.lower()):
            await message.author.send(random.choice(gm_mess['gmdawdle']))
        elif message.channel and not message.author.bot and ('nini dawdle' in message.content.lower()):
            await message.author.send(random.choice(gn_mess['nini_mess']))
        if message.guild is None and message.content.lower() in ['hi', 'hello', 'hey']:
            await message.author.send('Hi, I\'m Dawdle!')
