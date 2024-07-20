from flask_restful import Resource
from Models.BooksCollection import BooksCollection
from Exceptions.NoMatchingItemException import NoMatchingItemException
from Exceptions.InvalidRequestBodyException import InvalidRequestBodyException
from Exceptions.UnsupportedMediaTypeException import UnsupportedMediaTypeException
from Services.DataValidator import DataValidator
from flask import request

class Id(Resource):
    def __init__(self, booksCollection: BooksCollection, dataValidator: DataValidator) -> None:
        self._booksCollection = booksCollection()
        self._dataValidator = dataValidator()
    
    def get(self, id: str) -> tuple:
        print(f"Called GET on Id with id: {id}")
        try:
            return self._booksCollection.getBookById(id), 200

        except InvalidRequestBodyException as exception:
            return "Unprocessable Content: " + exception.message, 422

        except NoMatchingItemException as exception:
            return "No matching item: " + exception.message, 404

        # TODO: Do all exceptions has exception.args in python?
        except Exception as exception:
            return "Unexpected error: " + str(exception.args), 500
        
    def delete(self, id: str) -> tuple:
        print(f"Called DELETE on Id with id: {id}")
        try:
            deletedBookId = self._booksCollection.deleteBookById(id)
            # TODO: Check if this is a json or a dictionary (relevant for all returns)
            return {"ID": deletedBookId}, 200

        except InvalidRequestBodyException as exception:
            return "Unprocessable Content: " + exception.message, 422

        except NoMatchingItemException as exception:
            return "No matching item: " + exception.message, 404
        
        # TODO: Do all exceptions has exception.args in python?
        except Exception as exception:
            return "Unexpected error: " + str(exception.args), 500
        
        
    def put(self, id: str) -> tuple:
        print(f"Called PUT on Id with id: {id}")
        try:
            requestBody = request.get_json(silent=True)
            self._dataValidator.validateIdPutRequestBody(requestBody)
            updatedDocumentId = self._booksCollection.updateSpecificDocumentFromCollection(id, requestBody)
            return {"ID": updatedDocumentId}, 200
        
        except InvalidRequestBodyException as exception:
            return "Unprocessable content: " + exception.message, 422
        
        except NoMatchingItemException as exception:
            return "No matching item: " + exception.message, 404
        
        except UnsupportedMediaTypeException as exception:
            return "Unsupported media type: " + exception.message, 415
        
        # TODO: Do all exceptions has exception.args in python?        
        except Exception as exception:
            return "Unexpected error: " + str(exception.args), 500

