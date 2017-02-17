class LanguageChain(object):
    def __init__(self):
        self.rules = []
        self.method = None
    
    def addRule(self, rule):
        self.rules.append(rule)
        
    def setMethod(self, method):
        self.method = method