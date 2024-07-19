from bson import ObjectId
from Exceptions.EmptyCollectionException import EmptyCollectionException
from Exceptions.NoMatchingItemException import NoMatchingItemException
from Exceptions.InvalidRequestBodyException import InvalidRequestBodyException
from Services.DataProcessor import DataProcessor
from Models.RatingsCollection import RatingsCollection
from Services.mongodb import MongoDBManager

class BooksCollection:
    def __init__(self, dataProcessor: DataProcessor, ratingsCollection: RatingsCollection) -> None:
        self.mongo_manager = MongoDBManager("books")
        self._dataProcessor = dataProcessor
        self._ratingsCollection = ratingsCollection

    def insertBookAndReturnId(self, requestBody: dict) -> str:
        print(f"Inside 'insertBookAndReturnId' (function of 'BooksCollection'). requestBody is: {requestBody}")
        fullBookData = self._dataProcessor.constructFullBookData(requestBody)
        insert_result = self.mongo_manager.insert_document(fullBookData)
        inserted_id = str(insert_result.inserted_id)
        fullBookData['id'] = inserted_id

        self._ratingsCollection.createNewRating(fullBookData)
        return inserted_id

    def getCollectionFilteredByQuery(self, query: dict) -> list:
        print(f"Inside 'getCollectionFilteredByQuery' (function of 'BooksCollection'). with query: {query}")
        results = list(self.mongo_manager.find_documents(query))

        if not results:
            raise EmptyCollectionException("There are no books matching your criteria")

        for book in results:
            book['id'] = str(book.pop('_id'))

        return results

    def getBookById(self, id: str) -> dict:
        print(f"Entered 'getBookById' (function of 'BooksCollection') with id: {id}")

        if not self.is_valid_objectid(id):
            print(f"Invalid object id: {id}")
            raise InvalidRequestBodyException("Invalid object id")

        book = self.mongo_manager.find_document_by_id(id)

        if book:
            book['id'] = str(book.pop('_id'))
            return book
        else:
            raise NoMatchingItemException(f"There is no matching book to the provided id: {id}")

    def doBookWithGivenIsbnAlreadyExist(self, isbn: str) -> bool:
        print(f"Inside 'doBookWithGivenIsbnAlreadyExist' (function of 'BooksCollection') with ISBN: {isbn}")
        book = self.mongo_manager.find_document({'ISBN': isbn})
        return bool(book)

    def deleteBookById(self, id: str) -> str:
        print(f"Inside 'deleteBookById' (function of 'BooksCollection') with id: {id}")

        if not self.is_valid_objectid(id):
            raise InvalidRequestBodyException("Invalid object id")

        delete_result = self.mongo_manager.delete_document(id)
        if delete_result.deleted_count == 0:
            raise NoMatchingItemException(f"The id which was asked to be deleted ({id}) doesn't exist")

        self._ratingsCollection.deleteRating(id)
        return id

    def updateSpecificDocumentFromCollection(self, idOfDocumentToUpdate: str, requestBody: dict) -> str:
        print(f"Inside 'updateSpecificDocumentFromCollection' (function of 'BooksCollection') with idOfDocumentToUpdate: {idOfDocumentToUpdate} and requestBody: {requestBody}")
        if 'id' not in requestBody:
            raise InvalidRequestBodyException("The request body has no 'id' field.")
        updatedResourceId = requestBody['id']
        self.mongo_manager.update_document({'_id': ObjectId(idOfDocumentToUpdate)}, {'$set': requestBody})
        valuesList = self.__getRatingsValuesList(idOfDocumentToUpdate)
        self._ratingsCollection.createNewRating(requestBody, valuesList)
        return updatedResourceId

    def __getRatingsValuesList(self, id: str) -> list:
        print(f"Inside '__getRatingsValuesList' (function of 'BooksCollection') with id: {id}")
        return self._ratingsCollection.getRatingById(id)["values"]

    def __isQueryParameterSatisfiedByDocument(self, document: dict, queryKey: str, queryValue: str) -> bool:
        print(f"Inside '__isQueryParameterSatisfiedByDocument' (function of 'BooksCollection') with document: {document} and query: {queryKey}={queryValue}")
        documentValue = document.get(queryKey)
        if type(documentValue) is list:
            return queryValue in documentValue
        return documentValue == queryValue

    def is_valid_objectid(self, objectid):
        return ObjectId.is_valid(objectid)