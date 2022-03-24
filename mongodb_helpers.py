# Mongodb
from pymongo import MongoClient


class MongoDBHelpers():
    def __init__(self, host, port, db_name, collection_name):
        connection = MongoClient(host, port)
        self.db = connection[db_name]
        self.collection = self.db[collection_name]

    def set_colletion(self, collection_name):
        try:
            if collection_name in self.db.list_collection_names():
                self.collection = self.db.get_collection(collection_name)
            else:
                self.collection = self.db.create_collection(collection_name)
        except Exception as e:
            print("Failed to set collection")

    def insert(self, collection_name, data):
        try:
            self.set_colletion(collection_name)
            if len(data) > 1:
                self.collection.insert_many(data)
            else:
                self.collection.insert_one(data[0])
            return True
        except Exception as e:
            print("Failed to insert data:",e)

    def search(self, collection_name, query):
        try:
            self.set_colletion(collection_name)
            rs = self.collection.find(query)
            return rs
        except Exception as e:
            print("Failed to search data in Mongodb")

    def find(self, collection_name):
        try:
            self.set_colletion(collection_name)
            return self.collection.find()
        except Exception as e:
            print("Failed to find all document in collection:", e)

    def update_one(self, collection_name, query, data):
        try:
            self.set_colletion(collection_name)
            update = {'$set': data}
            self.collection.update_one(query, update)
            return True
        except Exception as e:
            print("Failed to update data into collection:", e)

    def delete_one(self, collection_name, query):
        try:
            self.set_colletion(collection_name)
            self.collection.delete_one(query)
            return True
        except Exception as e:
            print("Failed to delete a single document matching the query:", e)

    def delete_collection(self, collection_name):
        try:
            self.db.drop_collection(collection_name)
            return True
        except Exception as e:
            print("Failed to drop mongodb collection:", e)





