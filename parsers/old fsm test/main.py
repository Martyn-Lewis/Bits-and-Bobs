import states
import machine

class Calculator(object):
    def __init__(self, stream, terms={}):
        self.stream = stream
        self.matchee = None
        self.terms = terms
    
    def match(self, token_identifier):
        if self.matchee:
            return self.matchee.identifier == token_identifier
        else:
            self.matchee = self.stream.next()
            #print(self.matchee)
            if self.matchee:
                return self.matchee.identifier == token_identifier
            else:
                return None
    
    def nom(self):
        self.matchee = None
    
    def parse_expr(self):
        term = self.parse_term()
        while self.stream.valid():
            if self.match('PLUS'):
                self.nom()
                term = term + self.parse_term()
            elif self.match('MINUS'):
                self.nom()
                term = term - self.parse_term()
            else:
                return term
        return term
    
    def parse_term(self):
        factor = self.parse_factor()
        while self.stream.valid():
            if self.match('DIVIDE'):
                self.nom()
                factor = factor / self.parse_factor()
            elif self.match('MULTIPLY'):
                self.nom()
                factor = factor * self.parse_factor()
            else:
                return factor
        return factor
    
    def parse_factor(self):
        negate = 1
        if self.match('MINUS'):
            negate = -1
            self.nom()
        if self.match('OPEN'):
            self.nom()
            ans = self.parse_expr()
            if not self.match('CLOSE'):
                raise Exception("Please close your expressions :(")
            else:
                self.nom()
                return ans * negate
        elif self.match('INTEGER') or self.match('FLOAT') or self.match('DOUBLE'):
            x = self.matchee
            self.nom()
            return float(x.value) * negate
        elif self.match('id'):
            id = self.matchee.value
            if id in self.terms:
                self.nom()
                if self.match('OPEN'):
                    return self.parse_function(id)
                else:
                    return self.terms[id]
            else:
                raise Exception("Please complete your terms :(")
        raise Exception("This should literally never happen though")
    
    def parse_function(self, id):
        arguments = []
        self.nom()
        while not self.match('CLOSE'):
            next = self.parse_expr()
            arguments.append(next)
            if self.match('SEPARATOR'):
                self.nom()
            elif self.match('CLOSE'):
                break
            else:
                raise Exception("Incorrect function application?")
        self.nom()
        f = self.terms[id]
        return f(*arguments)

if __name__ == '__main__':
    myMachine = machine.Machine()
    list(map(myMachine.addStateConstructor, states.InitialiserList))
    myMachine.initial = 'STATE_BEGIN'
    
    print(myMachine.states)
    
    def test(expr, terms=None):
        if terms:
            print ("Test input: '%s', with terms: %s" % (expr, str(terms)))
        else:
            print("Test input: '%s'" % (expr))
        tokenstream = myMachine.stream(expr)
        ans = Calculator(tokenstream, terms).parse_expr()
        print("Answer: %f" % (ans))
    
    test('2 + 2 * 2')
    test('(2 + 2) * 2')
    test('(2 + 2) * (2 + 2)')
    test('a + b * c', {'a': 2, 'b': 2, 'c': 2})
    test('(a + b) * c', {'a': 2, 'b': 2, 'c': 2})
    test('(a + a) * (b + b) / (c + c)', {'a': 2, 'b': 2, 'c': 2})
    test('abs(-123) * pow(abs(a), 2)', {'a': 2, 'pow': pow, 'abs': abs})
    
    #while tokenstream.valid():
    #   try:
    #      print(tokenstream.next())
    #   except:
    #       print(tokenstream.tokens, tokenstream.buffer, tokenstream.state, tokenstream.states)
    #       raise