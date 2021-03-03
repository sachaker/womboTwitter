import config
from twilio.rest import Client

def sendText(textBody):
    client = Client(config.twilio_api_key, config.twilio_auth_token)

    message = client.messages \
        .create(
        body=textBody,
        from_=config.twilio_from,
        to=config.twilio_to
    )

    return message

def getTweets(listOfUsers, consumerKey=config.twitter_api_key, \
              consumerSecret=config.twitter_secret_key, accessToken=config.twitter_access_token, \
              accessTokenSecret=config.twitter_access_token_secret, maxTweets=10, previousDates=[],
              tweetString="", sendSMS=False):

    import tweepy

    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth, wait_on_rate_limit=False) # change flag
    output={}

    for user in listOfUsers:
        data = [
            {
                'timestamp' : tweet.created_at.strftime("%m/%d/%Y %H:%M:%S"),
                'tweet text' : tweet.full_text.replace('\n', ' '),
                'username' : tweet.user.screen_name,
                'tweet URL' : 'https://twitter.com/twitter/statuses/' + str(tweet.id),
                'tweet ID' : str(tweet.id)
              }
                  for tweet in tweepy.Cursor(api.user_timeline, id=user, lang="en", tweet_mode='extended').items(maxTweets)
                ]

        for i, datum in enumerate(data):
            output[i] = datum # key = index, value = twitter data

            if (datum['timestamp'] not in previousDates) and (len(previousDates) >= maxTweets):
                print(datum['tweet URL'])
                print("NEW TWEET!!")
                api.update_status(status="@" + user + " " + tweetString, in_reply_to_status_id=datum['tweet ID'])
                if sendSMS:
                    sendText("Replied to @" + user + " successfully!")
                return True
            else:
                try:
                    previousDates = list(set(previousDates.append(datum['timestamp'])))

                except:
                    continue

    return False