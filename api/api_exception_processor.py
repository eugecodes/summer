import shelve


class ApiExceptionProcessor:

    FILE_NAME = 'tmp/exceptions.bin'

    def __init__(self):
        self._index = 0

    def clear(self):
        with shelve.open(self.FILE_NAME) as db:
            db.clear()
            self._index = 0
        return self

    def saveHandler(self, handler):
        with shelve.open(self.FILE_NAME) as db:
            db[str(self._index)] = handler
            self._index += 1
        return True

    def getHandlers(self):
        handlers = {}
        with shelve.open(self.FILE_NAME) as db:
            handlers = {key: db[key] for key in db}
        return handlers

    def removeHandler(self, key):
        with shelve.open(self.FILE_NAME) as db:
            del db[key]
