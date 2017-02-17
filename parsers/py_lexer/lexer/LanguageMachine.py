from .LanguageTokenStream import LanguageTokenStream

class LanguageMachine(object):
    def __init__(self, language):
        self.language = language
        
    def createStream(self, buffer):
        return LanguageTokenStream(self, buffer)