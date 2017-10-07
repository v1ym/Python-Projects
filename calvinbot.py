#tutorial from https://scotch.io/tutorials/build-a-tweet-bot-with-python
#tutorial from https://dototot.com/how-to-write-a-twitter-bot-with-python-and-tweepy/

import tweepy, time, sys
import random, dircache, os

from PIL import Image
from PIL import ImageFile
from secrets import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

print "Calvin Bot up and running..."
tweetcount = 0

#path = "./test/test.gif"
#api.update_with_media(path)

dir = "./images"
lastimage = ""
running = True
while (running):
    while True:
        filename = random.choice(dircache.listdir(dir))
        path = os.path.join(dir, filename)
        if (path != lastimage):
            break
    lastimage = path

    api.update_with_media(path)
    tweetcount += 1
    print "Tweeted %i images since running" % (tweetcount)

    interval = 60 * 60 * 6 #tweets every 6 hours
    time.sleep(interval)
