from pymongo import MongoClient
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

# MongoDB connection is established and configured
connection = MongoClient('localhost', 27017)
db = connection.StreamData
collection = db.tweets
regex_str = [
     r'<[^>]+>',
     r'(?:(?:\d+,?)+(?:\.?\d+)?)',
     r"(?:[a-z][a-z'\-_]+[a-z])",
     r'(?:[\w_]+)',
]
data = []
try:
    rows = collection.find({'brand': 2,  "x": 1})
    print('\n All data from Database \n')
    for row in rows:
        line = re.sub(r"http\S+", "",(row['text']))
        line = re.sub(r'''[.,"!']+''', '', line)  # removes the characters specified
        line = re.sub(r'[0-9]', '', line)  # removes RT
        line = re.sub(r'[:,#]\S+', '', line)
        line = re.sub("[^a-zA-Z]", " ", line)
        data.append(line)
        #print(line)
    print(len(data))
    print(data)

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(data)

    true_k = 5
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=30000, n_init=1)
    model.fit(X)

    print("Top terms per cluster:")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()

    for i in range(true_k):
        print("Cluster %d:" % i),
        for ind in order_centroids[i, :7]:
            print(' %s' % terms[ind]),
        print
except:
    print('yat')

#print("\n")
#print("Prediction")

#Y = vectorizer.transform(["chrome browser to open."])
#prediction = model.predict(Y)
#print(prediction)

#Y = vectorizer.transform(["My cat is hungry."])
#prediction = model.predict(Y)
#print(prediction)