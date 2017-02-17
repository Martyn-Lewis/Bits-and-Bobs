from . import LanguageException
from .LanguageToken import LanguageToken

class LanguageTokenStream(object):
    def __init__(self, machine, buffer):
        self.machine = machine
        self.buffer = buffer
        self.offset = 0
        self.cregex = self.machine.language.compileRegexString()
        self.tokens = []
        self.token_offset = 0
        
    def advance(self, offset):
        self.offset += offset
    
    def rewind(self, offset):
        self.offset -= offset
        
    def getch(self):
        val = self.buffer[self.offset]
        self.offset += 1
        return val
        
    def peek(self):
        return self.buffer[self.offset]
        
    def generator(self):
        duplicate = LanguageTokenStream(self.machine, self.buffer)
        return duplicate.rest()
        
    def rest(self):
        def generator_function():
            while True:
                token = self.next()
                
                yield token
                if token.identifier == 'eof':
                    break
        return generator_function()
        
    def next(self):
        token = self.consume_token()
        
        # Chain rule logic.
        # It's quite the mess, but it should work. Probably.
        initial_offset = self.token_offset
        do_again = True
        while do_again:
            do_again = False
            for x in self.machine.language.chains:
                if x.rules[0] == token.identifier:
                    # Try to apply this rule.
                    self.token_offset = initial_offset
                    for rule in x.rules[1:]:
                        next_token = self.next()
                        if next_token.identifier != rule:
                            # Nope
                            self.token_offset = initial_offset
                            break
                    if self.token_offset != initial_offset:
                        # We applied a rule.
                        offset = initial_offset - 1
                        consumed = self.tokens[offset:offset + len(x.rules)]
                        accidents = self.tokens[offset + len(x.rules):]
                        self.tokens = self.tokens[:offset]
                        self.tokens.append(x.method(self, consumed))
                        token = self.tokens[-1]
                        if len(accidents):
                            for v in accidents:
                                self.tokens.append(v)
                        self.token_offset = offset + 1
                        do_again = True
                        break
                    
        return token
                    
        
    def consume_token(self):
        if self.token_offset < len(self.tokens):
            self.token_offset += 1
            return self.tokens[self.token_offset - 1]
    
        if self.machine.language.skip_whitespace:
            while self.offset < len(self.buffer) and self.buffer[self.offset] in ' \t':
                self.offset += 1
    
        if self.offset >= len(self.buffer):
            return LanguageToken('eof', '')
        
        # See if we get any matches at all.
        match = self.cregex.match(self.buffer[self.offset:])
        if not match:
            # TODO:
            #error = LanguageException.SyntaxError()
            #error.source = self.buffer
            #error.offset = self.offset
            #error.stream = self
            #error.machine = self.machine
            #error.reason = "no match on input"
            raise LanguageException.SyntaxError("no match on input from offset %d" % (self.offset))
        
        # Find the wordclass for this match.
        # I feel like there is a much better way to do this.
        groups = match.groupdict()
        wordclass = None
        for k, v in groups.items():
            if v:
                wordclass = k
                break
        classobject = self.machine.language.rules[wordclass]
        
        # Call the wordclass's method to get the token.
        start, end = match.span(wordclass)
        start += self.offset
        end += self.offset
        token = classobject.method(self, self.buffer[start:end])
        self.tokens.append(token)
        self.token_offset += 1
        return token
