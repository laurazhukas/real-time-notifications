from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("")
db = client.test
collection = db.users

def create_new_user(user):
    collection.insert_one(user.__dict__)

def add_event_to_user(id, event):
    collection.update_one({'_id': ObjectId(id)}, {'$push' : {'events': event.__dict__}})

def get_user(id):
    user = collection.find_one({'_id': ObjectId(id)})
    return user

def get_user_id(first_name, last_name):
    user = collection.find({'first_name': first_name, 'last_name': last_name})
    cursor = user
    for doc in cursor:
        return doc['_id']

def print_collection():
    cursor = collection.find({})
    for doc in cursor:
        print(type(doc['_id']))