from flask_restful import Resource
from Models.RatingsCollection import RatingsCollection

class Top(Resource):
    def __init__(self, ratingsCollection: RatingsCollection) -> None:
        self._ratingsCollection = ratingsCollection()
        
    def get(self) -> tuple:
        print("Called GET on Top resource")
        try:
            return self._ratingsCollection.getTopRatedBooks(), 200

        # TODO: Do all exceptions has exception.args in python? stringify the args?        
        except Exception as exception:
            return "Unexpected error: " + exception.args, 500