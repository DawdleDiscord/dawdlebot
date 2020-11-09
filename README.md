# dawdlebot

This is a bot made with discordpy for the Discord server [Dawdle](discord.gg/dawdle).

The server it was built for is hardcoded into the bot, but if you still somehow find any bits of it useful you're welcome to take it.

### Contribution Guide

* DM amer first with an idea you think would benefit dawdlebot keeping the server needs in mind.
* If the idea is approved, you'll be added as a contributor.
* Put all new code either in a new or (if applicable) existing cog in [`/src/db_modules/`](https://github.com/DawdleDiscord/dawdlebot/tree/master/src/db_modules)
* Add your cog to the [`__init__.py`](https://github.com/DawdleDiscord/dawdlebot/blob/master/src/db_modules/__init__.py)
* Import it and add the appropriate `bot.add_cog()` line in [`dawdlebot.py`](https://github.com/DawdleDiscord/dawdlebot/blob/master/dawdlebot.py)
* Open a PR 


### Some Current Features

* Welcome/goodbye messages
* Photo verification system
* Cleaning identifying posts of former members
* Counting VC time
* Goodnight messages
* Checking that all members have intro/required roles
* Anonymous posting
* Reporting
* Role changes
* Birthdays
* Mass role kicking based on join time
* Sending server information

## Commands: All Members
Required arguments are denoted by `<argument>`, optional arguments are denoted by `[argument]`.

`~info [topic] [subtopic]` displays information relevant to that (sub)topic. If a topic is not included all topics will be listed.

`~vent <text>` sends an anonymous vent for staff approval. If staff approves it will be posted in the vent channel.

`~report <text>` sends the text of the report to staff. Images can be included.

`~done` will check if you have your roles and intro, and if so it will remove your `.` role 

`~birthday <day> <month>` adds your birthday.

`~birthdaymonth <month>` displays all birthdays for that month.

`~trivia` lets you play a game of trivia!

`~trivia leaderboard` shows the current leaderboard of trivia streaks.

`~inventory` to see your item inventory from lootboxes.

`~inventory info <item>` shows information about `item`.

`~profile [member]` see your (if no member put) or `member`'s Dawdle profile.

`~editprofile` brings up a menu to edit the **about** section of your profile.

`~editbanner` brings up a menu to enter a link to the image you would like to use for your profile's banner. You need to include the `https://` and it will only work for as long as that link is valid.

## Commands: Staff Only

Required arguments are denoted by `<argument>`, optional arguments are denoted by `[argument]`.

All `member` arguments work by ID, mention, username, or nickname. nick/usernames can be found by partial matches and are not case sensitive.

### Moderation

`~ban <member/userid> [rule #]` Bans the member/user. If a rule number is included an admonition is posted as

```<member/user> was banned by <you> (Rule [rule #])```

`~kick <member>` Kicks the member

`~unban <userID>` Unbans the user.

`~postadmonition <text>` Posts the text as an admonition.

`~prune <# of messages> [member/userID]` Prunes the given number of messages. Including a member or userID will prune only those messages sent by that user.

### Warnings

`~warn <member> <rule #> [yes/no]` Will create a warning for `member`. It will ask for context, once you reply the warning will be saved. You can include attachments in the reply. `Yes/no` tells it whether or not to post an admonition. The default option is `yes`. 

`~warnings <member>` Will pull up all warnings of `member`. Reference the warning number to edit/delete warnings.

`~editwarning <member> <warning number>` Edit the context of the `warning number` warning for `member`. Reference `~warning` to find the number. (Cannot edit attachments at this time.)

`~deletewarning <member> <warning number>` (alias: `~delwarning`) Delete the `warning number` warning for `member`. Reference `~warning` to find the number.

### Members

`~members clean [member]` cleans messages in identifying channels sent by users no longer in the server. If `member` is given it deletes messages only from that member.

`~members check` makes sure that every member has an intro and required roles.

### Roles

`~roles color <role> <newcolor>` changes the color of the role to `newcolor`.

`~roles mentionable <role>` toggles making the role mentionable

`~roles sidebar <role>` toggles displaying the role on the sidebar

`~roles position <role> <new position>` moves the role to the new integer position. Tip: use `~roles info` to see the position of other roles.

`~roles info <role>` gives information about the role

`~roles members <role>` lists all members who have the role.

`~roles give <member> <role>` gives the member the role

`~roles remove <member> <role>` removes the role from the member

`~roles kick <role> <hours>` This is the former `kick_role`. It will kick anyone with `role` who joined more than `hours` ago. Only works for @unverified  and @. roles.

### Bot Cleaning

`~clean botadd <botname> <botprefix>` adds that prefix as a command prefix.

`~clean botremove <botname>` removes the bot and its prefix

`~clean botlist` displays all added bots and prefixes

`~clean channeladd` adds that channel to be cleaned

`~clean channelremove` removes that channel from being cleaned

`~clean channellist` lists channels that are cleaned

### QOTD

The bot will check once per hour if the current hour is 17 UTC time. If so, then it will post the next question in the queue.

`~qotd add <question>` adds a question to the queue

the bot will post next question in the queue every day, then delete it from the queue

`~qotd get <number>` gets the number of qotd questions specified in the queue. if you put a number greater than the number of questions it'll just give you all the questions it has

`~qotd remove <number>` removes the question at the number in the queue. You can reference the numbers next to the questions in `~qotd get`

`~qotd edit <number>` allows you to replace the question at the number in the queue. You can reference the numbers next to the questions in `~qotd get`

`~qotd post` force the bot to post a qotd. should be used if the normal time passes and no qotds were added

### Autoreacts

`~autoreact add <channel> <emoji 1> <emoji 2> ...` adds the channel and emojis for the bot to autoreact.

`~autoreact remove <channel>` removes the channel from the autoreact list.

`~autoreact list`shows all added channels and corresponding emojis.

### Info

`~sendinfo <member> <topic> [subtopic]` DMs the member the information in the (sub) topic.

`~editinfo addtopic <topic>` Adds the topic.

`~editinfo removetopic <topic>` Removes the topic.

`~editinfo addsubtopic <topic> <subtopic>` Adds the subtopic under the topic, and also will ask you to input the information. This can also be used to update information, as it will replace the old subtopic and give a warning before doing so. **To input general topic information, name the subtopic the same as the topic.**

`~editinfo removesubtopic <topic> <subtopic>` Removes the subtopic from the topic.

### Birthdays

`~addbirthday <member> <day> <month>` manually inputs the member's birthday.

`~birthdayclean` removes any birthdays of members no longer in the server if they are not deleted automatically.

### Trivia

`~trivia add <question>` Starts a menu for adding the correct and incorrect answers to the question, then saves it.

`~trivia list` Lists all current trivia questions. Use the arrows to go between pages.

`~trivia edit <question>` Starts an interface to edit or delete the question. Question can either be specified by the question text or the index next to it in `~trivia list`. Be careful of ambiguities between those two possibilities.

### Welcome/Goodbye

`~setwelcome` and `~setgoodbye` Brings up a menu to change the welcome/goodbye message. It requires putting a name in the new message, either as a mention, name#xxxx, or just name. 

Mention: `{ment}`

name#xxxx: `{user}`

name: `{name}`

Ex: Welcome {ment} to Dawdle!

### Inventories

`~editinv add <item_name>` add the item with the given item name to the list of givable items.

`~editinv remove <item_name>` remove the item with the given item name from the list of giveable items.

`~editinv list` list all givable items

`~inv give <member> <number> <item>` give the `member` the `number` amount of `item`.

`~inv take <member> <number> <item>` remove the `number` of `item` from `member`

`~inv show <member>` shows the inventory of another member.

### Profiles

`~givebadge <member_or_role> <emoji 1> <emoji 2> ...` gives either `member` or every member in `role` those emojis as badges.

`~takebadge <member_or_role> <emoji 1> <emoji 2> ...` removes from  either `member` or every member in `role` those emojis as badges.

`~cleanbadges <member_or_role>` will remove and badges whose emoji has been deleted or is otherwise not found.

`~cleanprofiles` will delete profile information of any members who left.