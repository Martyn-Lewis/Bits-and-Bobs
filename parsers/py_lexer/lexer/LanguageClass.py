import re
from .LanguageToken import LanguageToken

class LanguageWordclass(object):
    def __init__(self, wordclass, method, regex):
        self.wordclass = wordclass
        self.method = method
        self.regex = regex

    def getRegexString(self):
        return "(?P<%s>%s)" % (self.wordclass, self.regex)
        
class LanguageClass(object):
    def __init__(self, name):
        self.name = name
        self.rules = {}
        self.cregex = None
        self.skip_whitespace = False
        self.chains = []
    
    def addRuleMethod(self, wordclass, method):
        regex = method.__doc__
        rule = LanguageWordclass(wordclass, method, regex)
        
        self.rules[wordclass] = rule
        
    def addSingleCharacterRule(self, character, identifier):
        def cheap_method(stream, value):
            stream.advance(1)
            return LanguageToken(identifier, character)
        wordclass = LanguageWordclass('character_'+identifier, cheap_method, '[\\%s]' % (character))
        
        self.rules['character_' + identifier] = wordclass
        
    def addChain(self, chain):
        self.chains.append(chain)
        
    def shouldSkipWhitespace(self, state):
        self.skip_whitespace = state
        
    def getRegexString(self):
        return "(%s)" % ("|".join(x.getRegexString() for x in self.rules.values()))
        
    def compileRegexString(self):
        self.cregex = re.compile(self.getRegexString())
        
        return self.cregex