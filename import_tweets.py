from pymongo import MongoClient

connection = MongoClient('localhost', 27017)
db = connection.StreamData
collection = db.tweets

try:
    rows = collection.find()
    print('\n All data from Database \n')
    for row in rows:

        tweets = open('tweets.txt', 'a', encoding="utf-8")
        tweets.write(str(row) + "\n")
        tweets.close()

except Exception as e:
    print(e)
