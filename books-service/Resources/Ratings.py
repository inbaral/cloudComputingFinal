from flask_restful import Resource, reqparse
from Models.RatingsCollection import RatingsCollection
from Exceptions.NoMatchingItemException import NoMatchingItemException
from flask import request

class Ratings(Resource):
    def __init__(self, ratingsCollection: RatingsCollection) -> None:
        self._ratingsCollection = ratingsCollection()
        self._parser = reqparse.RequestParser()
        self.__addArgumentsToParser()
        
    def get(self) -> tuple:
        query = self._parser.parse_args()
        print(f"Called GET on Rating resource with query: {query}")
        try:
            if "id" in query:
                id = query["id"]
                rating = self._ratingsCollection.getRatingById(id)
                rating.pop('_id')
                return rating, 200
            else:
                return self._ratingsCollection.getAllRatings(), 200
        
        except NoMatchingItemException as exception:
            return "No matching item: " + exception.message, 404
        
        except Exception as exception:
            return "Unexpected error: " + str(exception.args), 500
        
    def __addArgumentsToParser(self) -> None:
        actual_args = request.args
        allowed_args = ['id']

        for arg_name in actual_args:
            if arg_name in allowed_args:
                self._parser.add_argument(arg_name, location='args', required=False)