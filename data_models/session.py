from constants import Constants
import ai_models

class SessionData:
    
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionData, cls).__new__(cls)
            cls._instance._data = {}
            cls._instance._data[Constants.CHAT_HISTORY] = []
        return cls._instance

    def set(self, key, value):
        self._data[key] = value

    def get(self, key, default=None):
        return self._data.get(key, default)

    def remove(self, key):
        if key in self._data:
            del self._data[key]

    def clear(self):
        self._data.clear()

    def insertChats(self, chat):
        if self.get(Constants.CHAT_HISTORY) == None:
            self.set(Constants.CHAT_HISTORY, [])

        self.get(Constants.CHAT_HISTORY).append(chat)
    
    def get_model(self):
        #Default to llama
        
    
        return ai_models.llama_models.llama




if __name__ == '__main__':
    print(SessionData._instance)