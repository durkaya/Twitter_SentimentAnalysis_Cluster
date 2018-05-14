from pymongo import MongoClient
import tweepy
import json
from textblob import TextBlob

# MongoDB connection is established and configured
connection = MongoClient('localhost', 27017)
db = connection.StreamData
db.tweets.create_index("id", unique=True, dropDups=True)
collection = db.labeled

# organizing tweet information
class StreamListener(tweepy.StreamListener):

    def on_connect(self):
        print("Tweet streaming begin.")

    def on_error(self, status):
        print('Error Type: ' + status)
        return False

    def on_data(self, raw):
        data = json.loads(raw)
        tweet_id = data['id_str']  # The ID of tweet from Twitter in string format
        time = data['created_at']  # The time of creation of the tweet
        username = data['user']['screen_name']  # The Tweet author's username
        text = data['text']  # The entire body of the Tweet


        try:
            if data["text"].find('RT @') is -1:  # if not exist
                sample = TextBlob(text)
                polarity = sample.sentiment.polarity
                subjectivity = sample.sentiment.subjectivity
                print(tweet_id + '\t' + time + '\t' + username + '\n' + text + '\n' +
                      'Sentiment Result: polarity = ' + str(polarity) +
                      ', subjectivity = ' + str(subjectivity) + '\n\n')
                # Create object in json format
                # tweet = {'id': tweet_id, 'created_at': time, 'username': username, 'text': text, 'x': x}
                # 'polarity': polarity, 'subjectivity': subjectivity

                if polarity > 0:
                    x = 1
                elif polarity < 0:
                    x = -1
                else:
                    x = 0

                if subjectivity < 0.3:
                    y = 0
                elif subjectivity > 0.7:
                    y = 1
                else:
                    y = 0.5

                if 'Apple' in text or 'apple' in text:
                    brand = 1
                elif 'Samsung' in text or 'samsung' in text:
                    brand = 2
                elif 'Huawei' in text or 'huawei' in text:
                    brand = 3
                elif 'Xiaomi' in text or 'xiaomi' in text:
                    brand = 5
                else:
                    brand = 0
                tweet = {'id': tweet_id, 'text': text, 'x': x, 'y': y, 'brand': brand}
                collection.save(tweet)
                # Pretty print
                # print(json.dumps(tweet, indent=4, sort_keys=True))
                # Insert Tweet data to MongoDB

        except Exception as e:
                    print(e)
        return True
