#!/usr/bin/python
import praw
import re
import os
import pickle
import random

# This list contains the epithets that are associated with certain scores. The first six are for when a user gets a very low number in a particular ability score. The order goes as follows: Strength, Dexterity, Constitution, Intelligence, Wisdom, and Charisma. The next six are for when players get a particularly high number for a particular ability score. Order is the same as for the first six. The final six are for when a player gets the highest possible result, an 18, for an ability score. Order is the same as the last two.

epithets = ['Noodle-Arm', 'Sloth', 'Sickly', 'Witless', 'Naive', 'Frightener of Young Children', 'Mighty', 'Swift of Foot', 'Bulwark', 'Clever', 'Sensible', 'Smooth-Talker', 'Living Battering Ram', 'Arrow-Catcher', 'Adamantine', 'Insufferable Genius', 'Sensei', 'Irresistible'] 

def rollAbility():
	#This rolls 3 six-sided dice to determine a user's ability score. I was originally going to do the traditional DnD method of rolling 4 six-sided dice and taking the 3 best rolls, but then I decided it would be funnier if there were a higher chance for absurdly low scores.
	ability = 0
	for i in xrange(1, 4):
		roll = random.randint(1,6)
		ability += roll
	return ability

def createCharacter(name):
	#Str = rollAbility()
	#Dex = rollAbility()
	#Con = rollAbility()
	#Int = rollAbility()
	#Wis = rollAbility()
	#Cha = rollAbility()
	#lowest = min(Str, Dex, Con, Int, Wis, Cha)
	#highest = max(Str, Dex, Con, Int, Wis, Cha)
	abilities = []
	for i in xrange(1, 6):
		abilites.append(rollAbility())
	highest = max(abilities)
	lowest = min(abilities)
	
	


	if (lowest == 10 or lowest == 11) and (highest == 10 or highest == 11):
		epithet =  "Outstandingly Mediocre"
	else if highest == 18:
		for i in xrange(0, 5):
			if abilities[i] == 18:
				epithet = epithets[i + 12]
	# The following else if statements are to determine which is more noteworthy, the user's lowest roll or his highest roll.
	else if (10 - lowest) > (highest - 10):
		for i in xrange(0, 5):
			if abilities[i] == lowest:
				epithet = epithets[i]
	else:
		for i in xrange(0, 5):
			if abilities[i] == highest:
				epithet = epithets[i + 6]
			
	
	reply = name + " the " + epithet + '\n'

if not os.path.isfile("dndme_config.txt"):
    print "You must create the file dndme_config.txt with the pickled credentials."
    exit(1)
else:
    print "Loading credentials"
    user_data = pickle.load( open("dndme_config.txt","rb"))
    #print user_data

user_agent = ("DnDMe_Bot 0.1 created by /u/Corellius.")
r = praw.Reddit(user_agent=user_agent)

r.login(user_data[0], user_data[1])
del user_data

print "Successfully logged in"

# Check for previous replies
if not os.path.isfile("replies.txt"):
    replies = []
else:
    print "Loading previous reply ids"
    with open("replies.txt", "r") as f:
        replies = f.read()
        replies = replies.split("\n")
        replies = filter(None, replies)

# Check for new items to reply to
subreddit = r.get_subreddit('umw_cpsc470Z')
print "Checking for new posts"
for submission in subreddit.get_hot(limit=10):
    print "Checking submission ", submission.id
    if submission.id not in replies:
        if re.search("dndme", submission.title, re.IGNORECASE) or re.search("dndme", submission.selftext, re.IGNORECASE):
            submission.add_comment(REPLY)
            print "Bot replying to submission: ", submission.id
            replies.append(submission.id)
    print "Checking comments"
    flat_comments = praw.helpers.flatten_tree(submission.comments)
    for comment in flat_comments:
        if comment.id not in replies: 
            if re.search("dndme", comment.body, re.IGNORECASE):
                print "Bot replying to comment: ", comment.id
                comment.reply(REPLY)
                replies.append(comment.id)

# Save new replies
print "Saving ids to file"
with open("replies.txt", "w") as f:
    for i in replies:
        f.write(i + "\n")
