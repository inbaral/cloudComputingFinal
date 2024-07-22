from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId

class MongoDBManager:
    # TODO: Change filename, make sure data is daved inside mongo, go through mongo implementation
    def __init__(self, collection):
        self.client = MongoClient("mongodb://mongodb:27017")

        try:
            # Send a ping to confirm the connection
            self.client.admin.command('ping')
            print("Connected to MongoDB successfully!")
        except ConnectionFailure:
            print("Failed to connect to MongoDB server.")

        self.db = self.client['library']
        self.collection = self.db[collection]

    def find_document(self, query):
        print(query)
        return self.collection.find_one(query)

    def find_documents(self, query):
        return self.collection.find(query)
    # TODO: Input tests for all those functions?
    def find_document_by_id(self, document_id):
        return self.collection.find_one({'_id': ObjectId(document_id)})

    def insert_document(self, document):
        return self.collection.insert_one(document)

    def update_document(self, query, new_values):
        return self.collection.update_one(query, {'$set': new_values})

    def delete_document(self, document_id):
        return self.collection.delete_one({'_id': ObjectId(document_id)})

