#tutorial from https://scotch.io/tutorials/build-a-tweet-bot-with-python
#tutorial from https://dototot.com/how-to-write-a-twitter-bot-with-python-and-tweepy/

import time, sys, os
import dircache, tweepy

from random import randint
from secrets import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

def get_time():
    now = time.localtime(time.time())
    now_hour = now[3]
    now_minute = str(now[4])

    #ampm and 24 hour clock
    if now_hour == 12:
        ampm = "pm"
    elif now_hour > 12:
        ampm = "pm"
        now_hour -= 12
    else:
        ampm = "am"
    now_hour = str(now_hour)

    #formatting for single digit minutes
    if len(now_minute) == 1:
        now_minute = "0" + now_minute

    return "%s:%s %s" % (now_hour, now_minute, ampm)

print "Calvin Bot up and running..."
imagedir = "./images"

running = True
while (running):
    interval = randint(14400, 28800)#between 4 and 8 hours

    f = open('./dirlist.txt', 'r')
    dirlist = f.readlines()
    f.close()

    f = open('./usedlist.txt', 'r')
    usedlist = f.readlines()
    f.close()

    if (not dirlist):
        dirlist = usedlist
        f = open('./dirlist.txt', 'w')
        usedlist = "".join(usedlist)
        f.write(usedlist)
        usedlist = []
        f.close()

        f = open('./usedlist.txt', 'w')
        f.write("")
        f.close()

    revisedlist = []
    for file in dirlist:
        revisedlist.append(file[:-1])

    choice = revisedlist[randint(0, len(revisedlist)-1)]
    usedlist.append(choice+'\n')
    revisedlist.remove(choice)

    f = open('./usedlist.txt', 'w')
    usedlist = "".join(usedlist)
    f.write(usedlist)
    f.close()

    writinglist = []
    for item in revisedlist:
        writinglist.append(item + '\n')

    f = open('./dirlist.txt', 'w')
    writinglist = "".join(writinglist)
    f.write(writinglist)
    f.close()

    path = os.path.join(imagedir, choice)
    api.update_with_media(path)
    now = str(get_time())

    nexthour = str(interval/(60*60)) + "h"
    nextminute = str((interval % 3600)/60) + "m"
    nexttweet = nexthour + " " + nextminute

    print "tweeted %s at %s, next tweet in %s" % (choice, now, nexttweet)

    time.sleep(interval)
