class EmptyCollectionException(Exception):
    
    def __init__(self, message="Books collection is empty") -> None:
        self.message = message
        super().__init__(self.message)