from helpers import *

tweetString = "first!\nhttps://www.youtube.com/watch?v=-lHtIhq7Ncg" # change this
twitterHandle = "paulwombo" # change this

tweeted = False
previousDates = []
dots = 1

while not tweeted:
    try:
        tweeted = getTweets([twitterHandle], maxTweets=1, previousDates=previousDates, tweetString=tweetString, sendSMS=False)
    except Exception as e:
        print(str(e) + '\nSleeping' + (dots%4)*'.')
        dots+=1
