from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId
import uuid

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/libraryDatabase"
mongo = PyMongo(app)

# Helper function to convert ObjectId to string
def convert_objectid(entity):
    if isinstance(entity, dict):
        for key in entity:
            if isinstance(entity[key], ObjectId):
                entity[key] = str(entity[key])
    return entity

@app.route('/books', methods=['GET', 'POST', 'PUT', 'DELETE'])
def books():
    if request.method == 'POST':
        book_data = request.json
        book_data['id'] = str(uuid.uuid4())
        mongo.db.books.insert_one(book_data)
        return jsonify(message="Book added successfully!", id=book_data['id']), 201
    elif request.method == 'GET':
        books_cursor = mongo.db.books.find()
        books_list = [convert_objectid(book) for book in books_cursor]
        return jsonify(books=books_list), 200
    elif request.method == 'PUT':
        # Add your PUT request handling here
        pass
    elif request.method == 'DELETE':
        # Add your DELETE request handling here
        pass

@app.route('/ratings', methods=['GET', 'POST', 'PUT', 'DELETE'])
def ratings():
    if request.method == 'POST':
        rating_data = request.json
        rating_data['id'] = str(uuid.uuid4())
        mongo.db.ratings.insert_one(rating_data)
        return jsonify(message="Rating added successfully!", id=rating_data['id']), 201
    elif request.method == 'GET':
        ratings_cursor = mongo.db.ratings.find()
        ratings_list = [convert_objectid(rating) for rating in ratings_cursor]
        return jsonify(ratings=ratings_list), 200
    elif request.method == 'PUT':
        # Add your PUT request handling here
        pass
    elif request.method == 'DELETE':
        # Add your DELETE request handling here
        pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
