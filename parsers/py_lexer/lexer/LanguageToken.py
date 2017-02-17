class LanguageToken(object):
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value
        
    def __repr__(self):
        return "<%s '%s'>" % (self.identifier, self.value)