from Exceptions.EmptyCollectionException import EmptyCollectionException
from Services.DataValidator import DataValidator
from Exceptions.NoMatchingItemException import NoMatchingItemException
from Services.mongodb import MongoDBManager
from bson import ObjectId


class RatingsCollection():
    def __init__(self, dataValidator: DataValidator) -> None:
        self.mongo_manager = MongoDBManager("ratings")
        self._dataValidator = dataValidator
        
    def getRatingById(self, bookId: str) -> dict:
        print(f"Inside 'getRatingsById' (function of RatingsCollection) with id: {bookId}")
        document = self.mongo_manager.find_document({"id": bookId})

        if document is not None:
            document['_id'] = str(document.pop('_id'))
            return document

        raise NoMatchingItemException(f"There is no book with the given id: {bookId}")
    
    def getTopRatedBooks(self) -> list:
        print("Inside 'getTopRatedBooks' (function of RatingsCollection)")
        pipeline = [
            {'$match': {'values': {'$exists': True, '$not': {'$size': 0}, '$gte': 3}}},
            {'$addFields': {'average': {'$avg': '$values'}}},
            {'$sort': {'average': -1}},
            {'$limit': 3}
        ]
        top_rated_books_cursor = self.mongo_manager.collection.aggregate(pipeline)
        top_rated_books = list(top_rated_books_cursor)

        return [{'id': rating['id'], 'title': rating['title'], 'average': rating['average']} for rating in top_rated_books]
    
    def createNewRating(self, data: dict, initialValues: list = None) -> None:
        print(f"Inside 'createNewRating' (function of RatingsCollection) with data: {data}.\ninitialValues is: {initialValues}")
        self._dataValidator.validateDataForCreateNewRating(data)
        values = initialValues if initialValues is not None else []
        average = 0 
        if initialValues is not None and initialValues != []:
            print(f'initialValues is: {initialValues}')
            average = round((sum(initialValues) / len(initialValues)), 2)
        self.mongo_manager.insert_document({"id": data["id"], "title": data["title"], "values": values, "average": average})
        

    def deleteRating(self, bookId: str) -> None:
        ratingId = str(self.getRatingById(bookId)["_id"])
        if self.mongo_manager.delete_document(ratingId) == 0:
            raise NoMatchingItemException(f"The id which was asked to be deleted ({bookId}) doesn't exist")
        
    def addRatingValueToBookAndReturnNewAverage(self, bookId: str, value: int) -> float:
        print(f"Inside 'addRatingValueToBookAndReturnNewAverage' (function of RatingsCollection) with id: {bookId} and value: {value}")
        rating = self.getRatingById(bookId)
        print(rating["values"])
        rating["values"].append(value)
        rating["average"] = round(sum(rating["values"]) / len(rating["values"]), 2)

        print(f"inside addRatingValueToBookAndReturnNewAverage - new rating is: {rating}")
        result = self.mongo_manager.update_document({"_id":ObjectId(rating['_id'])}, new_values={"values":rating["values"], "average":rating["average"]})
        print(f"result.matched_count {result.matched_count}")

        return rating["average"]
    
    def doRatingWithGivenIdAlreadyExist(self, bookId: str) -> bool:
        print(f"Inside 'doRatingWithGivenIdAlreadyExist' (function of RatingsCollection) with id: {bookId}")
        try:
            self.getRatingById(bookId)
            return True

        except NoMatchingItemException:
            return False

    def getAllRatings(self) -> list:
        print(f"Inside 'getAllRatings' (function of 'RatingsCollection')")
        results = list(self.mongo_manager.find_documents({}))

        if not results:
            raise EmptyCollectionException("There are no books matching your criteria")

        for rating in results:
            rating.pop('_id')

        return results