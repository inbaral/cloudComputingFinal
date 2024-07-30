from flask_restful import Resource, reqparse
from Models.RatingsCollection import RatingsCollection
from Exceptions.NoMatchingItemException import NoMatchingItemException

class RatingsId(Resource):
    def __init__(self, ratingsCollection: RatingsCollection) -> None:
        self._ratingsCollection = ratingsCollection()
        self._parser = reqparse.RequestParser()
        self.__addArgumentsToParser()
        
    def get(self, id: str) -> tuple:
        print(f"Called get on RatingId resource with id: {id}")
        try:
            rating = self._ratingsCollection.getRatingById(id)
            rating.pop('_id')
            return rating, 200
        
        except NoMatchingItemException as exception:
            return "No matching item: " + exception.message, 404

        except Exception as exception:
            return "Unexpected error: " + str(exception.args), 500
    
    def __addArgumentsToParser(self) -> None:
        self._parser.add_argument('id', location='args', required=True)