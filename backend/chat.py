import itertools

class Chat:

    incremental_id = itertools.count()

    def __init__(self):
        self.id = next(Chat.incremental_id)

    def setTitle(self, title):
        self.title = title

        