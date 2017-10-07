import urllib, time, sys
from bs4 import BeautifulSoup as Soup
import tweepy, dircache, os
from random import randint

from secrets import *

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

    return "The time is %s:%s %s" % (now_hour, now_minute, ampm)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

#print "Redacted Thought bot up and running..."

site = "http://www.reddit.com/r/oneliners"
oneliners  = []

running = True

while(running):
    interval = randint(3600, 10800)#between 1 and 3 hours

    opener = urllib.FancyURLopener({})
    pageurl = opener.open(site)
    html = pageurl.read()
    soup = Soup(html, "html.parser")

    f = open("./backupthoughts.txt", 'r')
    backupcontent = f.readlines()
    f.close()

    f = open('./usedthoughts.txt', 'r')
    usedcontent = f.readlines()
    f.close()

    #grab all headlines from reddit
    for headline in soup.find_all('p', {'class': 'title'}):
        try:
            line = headline.get_text()
            if (str(line[:2]) == "!!" or str(line[:2]) == "/r"):
                continue
            oneliners.append(line[:-17])
        except:
            pass
    try:
        #pull a random headline to start
        tweet = (oneliners[randint(0, len(oneliners)-1)] + '\n')
    except:
        #handle exceptions when bot requests too often
        print "botting too fast..."
        tweet = backupcontent[randint(0, len(backupcontent)-1)]

    #add all possibilities to backup list
    for line in oneliners:
        backupcontent.append(line + '\n')
    backupset = set(backupcontent)
    backupset = "".join(backupset)
    f = open('./backupthoughts.txt', 'w')
    f.write(backupset.encode('ascii', 'ignore'))
    f.close()

    #if it's been used before, find another tweet
    if (tweet in usedcontent):
        f = open('./backupthoughts.txt', 'r')
        backupcontent = f.readlines()
        while (tweet in usedcontent):
            tweet = backupcontent[randint(0, len(backupcontent)-1)]
        backupcontent.remove(tweet)
        f.close()
        f = open('./backupthoughts.txt', 'w')
        backupcontent = "".join(backupcontent)
        f.write(backupcontent)

    #write tweet to used file
    usedcontent.append(tweet)
    usedcontent = "".join(usedcontent)
    f = open('./usedthoughts.txt', 'w')
    f.write(usedcontent.encode('ascii', 'ignore'))
    f.close()

    #and finally tweet it
    print get_time()
    print tweet.encode('ascii', 'ignore')
    print "(next tweet in " + str(interval/60) + " minutes)"
    api.update_status(tweet)

    #file cleanup
    f = open('./usedthoughts.txt', 'r')
    usedthoughts = f.readlines()
    f.close()

    f = open('./backupthoughts.txt', 'r')
    backupthoughts = f.readlines()
    f.close()

    for used_line in usedthoughts:
        for backup_line in backupthoughts:
            if(used_line == backup_line):
                backupthoughts.remove(backup_line)

    f = open('./backupthoughts.txt', 'w')
    backupthoughts = "".join(backupthoughts)
    f.write(backupthoughts)
    f.close()

    time.sleep(interval)
