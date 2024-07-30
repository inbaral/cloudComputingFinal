import uuid
from Services.ApiInvoker import ApiInvoker
from Exceptions.NoMatchingItemsInApiGetCallException import NoMatchingItemsInApiGetCallException
from Exceptions.InternalServerException import InternalServerException
from datetime import datetime

class DataProcessor():
    
    def __init__(self, apiInvoker: ApiInvoker) -> None:
        self._apiInvoker = apiInvoker
    
    def constructFullBookData(self, partialBookData: dict) -> dict:
        print(f"Inside 'constructFullBookData'. Constructing foll data to partialBookData: {partialBookData}")
        try:
            isbn = partialBookData["ISBN"]            
            bookData = self.__getBookData(isbn)

            fullData = self.__combineDataFromRequestAndApiCalls(partialBookData, bookData)
            self.__postProcessData(fullData)
            
            return fullData
            
        except NoMatchingItemsInApiGetCallException:
            raise
        
        except Exception as exception:
            raise InternalServerException(f"Unable to construct full data for partial book data {partialBookData}. Exception is: {exception.args}")
        
    def __combineDataFromRequestAndApiCalls(self, requestBody: dict, bookData: dict) -> dict:
        print(f"Inside '__combineDataFromRequestAndApiCalls' (private function of DataProcessor) with requestBody: {requestBody}, bookData: {bookData}")
        fullData = dict(requestBody)
        fullData.update(bookData)

        return fullData
    
    def __getBookData(self, isbn: str) -> dict:
        print(f"Inside '__getBookData' (private function of DataProcessor) with ISBN: {isbn}")
        bookData = self._apiInvoker.sendGetRequestToGoogleBooksApiAndReturnBookData(isbn)
        for key in bookData:
            if bookData[key] == "" or bookData[key] is None:
                bookData[key] = "missing"

        return bookData
    
    def __postProcessData(self, data: dict) -> None:
        print(f"Inside '__postProcessData (private function of DataProcessor) with data: {data}")
        data["publishedDate"] = self.__getValidDate(data["publishedDate"])
        data["authors"] = self.__concatenateListToString(data["authors"])
        return 
    
    def __getValidDate(self, dateString: str) -> str:
        print(f"Inside '__getValidDate' (private function of DataProcessor) with dateString: {dateString}")
        formats = ["%Y-%m-%d", "%Y"]
        for format in formats:
            try:
                datetime.strptime(dateString, format)
                return dateString
            except ValueError:
                pass
        return "missing"
    
    def __concatenateListToString(self, listToConcatenate: list) -> str:
        print(f"Inside '__concatenateListToString' (private function of DataProcessor) with listToConcatenate: {listToConcatenate}")
        return " and ".join(listToConcatenate)