import tweepy
from tweepy import OAuthHandler

import tag_listening

#twitter api keys to authanticate
consumer_key = "pke9j4KeQyIsK7teZV3AogAqC"
consumer_secret = "JIPuxtYYk9IcNPVDz1FBxaPD9qEGqxR6y6ToF8RJxNzSRvOqvr"

access_token = "773843946-2jSxy9cTtQ2fKyitiqyPm4c09eU6vzu6v5b1z89H"
access_token_secret = "0bMfMGZtox4gUC5ozXH213DEdOkzQrmYXpHHQbiveO6Cg"

#authentication sections
auth = OAuthHandler(consumer_key, consumer_secret)
print("First auth done")
auth.set_access_token(access_token, access_token_secret)
print("2nd auth done")

#tracked word
WORDS = ['#apple', '#samsung', '#huawei', '#xiaomi']

#from listening library, StreamListener object created
listener = tag_listening.StreamListener(api=tweepy.API(wait_on_rate_limit=True))
#from tweepy library, Stream begins
streamer = tweepy.Stream(auth=auth, listener=listener)

print("Tracking: " + str(WORDS))
streamer.filter(track=WORDS, languages=["en"]) #filtering keywords