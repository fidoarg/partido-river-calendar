from abc import ABC

class Scrapper(ABC):

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def execute(self):
        pass

    def close(self):
        pass

class BatchParser(ABC):
    
    def execute(self):
        pass

class Parser(ABC):
    
    def execute(self):
        pass

class Entity(ABC):

    def create(self):
        pass

    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def exists(self):
        pass
