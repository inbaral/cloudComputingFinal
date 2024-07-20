from flask import Flask
from flask_restful import Api
from Resources.Books import Books
from Resources.Id import Id
from Resources.RatingsId import RatingsId
from Resources.Ratings import Ratings
from Resources.Top import Top
from Resources.Values import Values
from Container import Container
from dependency_injector.wiring import inject
import os

@inject
def main() -> None:
    # TODO: Should API_KEY be in "secrets"?
    os.environ["API_KEY"] = "AIzaSyDZ-DCljJFFfiKF7gKJIZIvOQg4NijXY4k"
    
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Books, '/books', resource_class_kwargs={'booksCollection': container.booksCollection, 'dataValidator': container.dataValidator})
    api.add_resource(Id, '/books/<string:id>', resource_class_kwargs={'booksCollection': container.booksCollection, 'dataValidator': container.dataValidator})
    api.add_resource(Ratings, '/ratings', resource_class_kwargs={'ratingsCollection': container.ratingsCollection})
    api.add_resource(RatingsId, '/ratings/<string:id>', resource_class_kwargs={'ratingsCollection': container.ratingsCollection})
    api.add_resource(Top, '/top', resource_class_kwargs={'ratingsCollection': container.ratingsCollection})
    api.add_resource(Values, '/ratings/<string:id>/values', resource_class_kwargs={'ratingsCollection': container.ratingsCollection, 'dataValidator': container.dataValidator})
    
    app.run(host='0.0.0.0', port=5001, debug=True)
    
if __name__ == '__main__':
    container = Container()
    container.wire(modules=[__name__])
    print("Running the server")
    main()
