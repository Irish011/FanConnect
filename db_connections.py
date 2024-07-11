import pymongo

# url = 'mongodb://localhost:27017'
url = ''
client = pymongo.MongoClient(url)

db = client['FanConnect']
user_collection = db['users']
club_collection = db['clubs']
matches_collection = db['matches']
predictions_collections = db['prediction']
