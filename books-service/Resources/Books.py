from Models.BooksCollection import BooksCollection
from Services.DataValidator import DataValidator
from flask_restful import Resource, reqparse
from flask import request
from Exceptions.InvalidRequestBodyException import InvalidRequestBodyException
from Exceptions.UnsupportedMediaTypeException import UnsupportedMediaTypeException
from Exceptions.InternalServerException import InternalServerException
from Exceptions.EmptyCollectionException import EmptyCollectionException
from Exceptions.NoMatchingItemsInApiGetCallException import NoMatchingItemsInApiGetCallException

class Books(Resource):        
    def __init__(self, booksCollection: BooksCollection, dataValidator: DataValidator) -> None:
        self._booksCollection = booksCollection()
        self._dataValidator = dataValidator()
        self._parser = reqparse.RequestParser()
        self.__addArgumentsToParser()
    
    def post(self) -> tuple:
        try:
            requestBody = request.get_json(silent=True)
            print(f"Called POST on Books resource with requestBody: {requestBody}")
            self._dataValidator.validateBooksPostRequestBody(requestBody)
            if self._booksCollection.doBookWithGivenIsbnAlreadyExist(requestBody["ISBN"]):
                raise InvalidRequestBodyException("A book with the same ISBN already exist in the collection")
            newBookId = self._booksCollection.insertBookAndReturnId(requestBody)
            return {"ID": newBookId}, 201
        
        except InvalidRequestBodyException as exception:
            print(exception.message)
            return "Unprocessable Content: " + exception.message, 422
        
        except NoMatchingItemsInApiGetCallException as exception:
            return "No matching items in api get call: " + exception.message, 400
        
        except UnsupportedMediaTypeException as exception:
            return "Unsupported media type: " + exception.message, 415
        
        except InternalServerException as exception:
            return "Internal server error: " + exception.message, 500
        
        except Exception as exception:
            return "Unexpected error: " + str(exception.args), 500

            
    def get(self) -> tuple:
        try:
            query = self._parser.parse_args()
            print(f"Called GET on Books resource with query: {query}")
            collection = self._booksCollection.getCollectionFilteredByQuery(query)
            return collection, 400

        except InvalidRequestBodyException as exception:
            return "Unprocessable Content: " + exception.message, 422

        except EmptyCollectionException as exception:
            return "Empty collection: " + exception.message, 404
        
        except InternalServerException as exception:
            return "Internal server error: " + exception.message, 500
        
        except Exception as exception:
            print(exception)
            return "Unexpected error: ", 500

    def __addArgumentsToParser(self) -> None:
        actual_args = request.args
        allowed_args = ['title', 'ISBN', 'genre', 'authors', 'publisher', 'publishedDate', 'id', 'language']

        for arg_name in actual_args:
            if arg_name in allowed_args:
                self._parser.add_argument(arg_name, location='args', required=False)

