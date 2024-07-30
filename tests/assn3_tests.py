import requests

BASE_URL = "http://127.0.0.1:5001"
ids = []
def test_post_books():
    books = [
        {"title": "Adventures of Huckleberry Finn", "ISBN": "9780520343641", "genre": "Fiction"},
        {"title": "The Best of Isaac Asimov", "ISBN": "9780385050784", "genre": "Science Fiction"},
        {"title": "Fear No Evil", "ISBN": "9780394558783", "genre": "Biography"}
    ]
    for book in books:
        response = requests.post(f"{BASE_URL}/books", json=book)
        assert response.status_code == 201
        response_json = response.json()
        ids.append(response_json["ID"])
    assert len(ids) == 40

def test_get_book1():
    book_id = ids[0]
    response = requests.get(f"{BASE_URL}/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["authors"] == "Mark Twain"

def test_get_books():
    response = requests.get(f"{BASE_URL}/books")
    assert response.status_code == 200
    assert len(response.json()) == 3

def test_post_invalid_book():
    book4 = {"title": "No such book", "ISBN": "0000001111111", "genre": "fakeness"}
    response = requests.post(f"{BASE_URL}/books", json=book4)
    assert response.status_code in [400, 422, 500]

def test_delete_book2():
    book_id = ids[1]
    response = requests.delete(f"{BASE_URL}/books/{book_id}")
    assert response.status_code == 200

def test_get_deleted_book2():
    book_id = ids[1]
    response = requests.get(f"{BASE_URL}/books/{book_id}")
    assert response.status_code == 404

def test_post_book5():
    book5 = { "title":"The Greatest Joke Book Ever", "authors":"Mel Greene", "ISBN":"9780380798490", "genre":"Jokes" }
    response = requests.post(f"{BASE_URL}/books", json=book5)
    assert response.status_code == 422