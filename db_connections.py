import pymongo

# url = 'mongodb://localhost:27017'
url = 'mongodb+srv://ajaybhartiirish:pYWWczuSxzfbrabX@fanconnect.kwpr27l.mongodb.net/'
client = pymongo.MongoClient(url)

db = client['FanConnect']
user_collection = db['users']
club_collection = db['clubs']
matches_collection = db['matches']
predictions_collections = db['prediction']