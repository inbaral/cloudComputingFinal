class UnsupportedMediaTypeException(Exception):
    
    def __init__(self, message="Request body type is unsupported") -> None:
        self.message = message
        super().__init__(self.message)