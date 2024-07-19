import requests
from Exceptions.NoMatchingItemsInApiGetCallException import NoMatchingItemsInApiGetCallException
from Exceptions.InternalServerException import InternalServerException
import os

class ApiInvoker:
    def sendGetRequestToGoogleBooksApiAndReturnBookData(self, isbn: str) -> dict:
        print(f"inside 'sendGetRequestToGoogleBooksApiAndReturnBookData'. Invoking an api call with ISBN:{isbn}")
        googleBooksUrl = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}'
        response = requests.get(googleBooksUrl)
        try:
            googleBooksData = response.json()['items'][0]['volumeInfo']
            print(f'googleBooksData is: {googleBooksData}')
        except Exception as exception:
            print(f'exception is: {exception.args} and response.json is: {((response.json())["totalItems"]) == 0}')
            if ((response.json())["totalItems"]) == 0:
                raise NoMatchingItemsInApiGetCallException(f"No items returned from Google Book API for given ISBN number ({isbn})")
            if exception == "unable to connect to Google":
                raise InternalServerException("Unable to connect to google") 
            raise exception       
                
        bookData = {
        "authors": googleBooksData.get("authors"),
        "publisher": googleBooksData.get("publisher"),
        "publishedDate": googleBooksData.get("publishedDate")
        }
        
        return bookData
