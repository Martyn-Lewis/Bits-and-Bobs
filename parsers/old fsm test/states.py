# FSM for symbol-recognition in a syntax analyser using classes.
# Please replace this, it makes human writing so annoying.
from machine import State
import string

class ErrorState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.identity = 'STATE_ERROR'
        
    def next(self):
        self.machine.finish()
        print(self.machine.buffer)
        print(list(map(str, self.machine.tokens)))
        raise Exception("We done goofed!")

class BeginState(State):
    operator_lookup = {'+': 'PLUS', '-': 'MINUS', '*': 'MULTIPLY', 
                       '/': 'DIVIDE', '(': 'OPEN', ')': 'CLOSE', 
                       ',': 'SEPARATOR', '=': 'EQUAL', ';': 'STATEMENT_SEPARATOR', '\n': 'STATEMENT_SEPARATOR',
                       ':': 'COLON', '[': 'OPEN_LIST', ']': 'CLOSE_LIST'}
    
    def __init__(self, machine):
        super().__init__(machine)
        self.identity = 'STATE_BEGIN'
    
    def next(self):
        ch = self.machine.lookahead()
        if ch == 'EOF':
            return 'STATE_FINAL'
        elif ch in '0123456789':
            self.machine.consume(1)
            return 'STATE_INTEGER'
        elif ch == '-':
            self.machine.consume(1)
            return 'STATE_MINUS'
        elif ch == '"':
            self.machine.consume(1)
            return 'STATE_STRING'
        elif ch == "'":
            self.machine.consume(1)
            return 'STATE_CHAR'
        elif ch in '+/*(),;\n:[]':
            self.machine.consume(1)
            self.machine.emit(BeginState.operator_lookup[ch])
            return 'STATE_BEGIN'
        elif ch in "=<>!":
            self.machine.consume(1)
            return 'STATE_CONDITIONAL' # or assignment
        elif ch == 'n':
            self.machine.consume(1)
            return 'STATE_NOT'
        elif ch == 'd':
            self.machine.consume(1)
            return 'STATE_DEF'
        elif ch == 'i':
            self.machine.consume(1)
            return 'STATE_IF'
        elif ch == 't':
            self.machine.consume(1)
            return 'STATE_THEN'
        elif ch == 'e':
            self.machine.consume(1)
            return 'STATE_ELSE'
        elif ch == 'w':
            self.machine.consume(1)
            return 'STATE_WHERE'
        elif ch == 'o':
            self.machine.consume(1)
            return 'STATE_OTHERWISE'
        elif ch == 'u':
            self.machine.consume(1)
            return 'STATE_USING'
        elif ch == 'c':
            self.machine.consume(1)
            return 'STATE_CASE'
        elif ch in IdState.symbol_initials:
            self.machine.consume(1)
            return 'STATE_ID'
        elif ch in ' \t':
            self.machine.ignore(1)
            return 'STATE_BEGIN'
        else:
            return 'STATE_ERROR'

class FinalState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.identity = 'STATE_FINAL'
        
    def next(self):
        self.machine.finish()

class CaseState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.identity = 'STATE_CASE'
    
    def next(self):
        ch = self.machine.lookahead()
        if ch == 'EOF':
            if self.machine.lifespan == 3:
                self.machine.emit('KEYWORD_CASE')
            else:
                self.machine.emit('id')
            return 'STATE_FINAL'
        elif ch == 'a' and self.machine.lifespan == 0:
            self.machine.consume(1)
            return 'STATE_CASE'
        elif ch == 's' and self.machine.lifespan == 1:
            self.machine.consume(1)
            return 'STATE_CASE'
        elif ch == 'e' and self.machine.lifespan == 2:
            self.machine.consume(1)
            return 'STATE_CASE'
        elif self.machine.lifespan == 3:
            if ch in IdState.symbol_valid:
                self.machine.consume(1)
                return 'STATE_ID'
            self.machine.emit('KEYWORD_CASE')
            return 'STATE_BEGIN'
        else:
            if ch in IdState.symbol_valid:
                self.machine.consume(1)
                return 'STATE_ID'
            else:
                self.machine.emit('id')
                return 'STATE_BEGIN'
        
class StringState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.identity = 'STATE_STRING'
        
    def consume_break(self):
        part = self.machine.lookahead()
        if part == 'n':
            self.ignore(1)
            self.presume('\n')
        elif part == '\\':
            self.consume(1)
        elif part == 't':
            self.ignore(1)
            self.presume('\t')
        
    def next(self):
        ch = self.machine.lookahead()
        if ch == 'EOF':
            print("End of file while reading string.")
            return 'STATE_ERROR'
        elif ch == '\\':
            self.machine.ignore(1)
            self.consume_break()
            return 'STATE_STRING'
        elif ch == '"':
            self.machine.consume(1)
            self.machine.emit('STRING')
            return 'STATE_BEGIN'
        else:
            # Assume it's stringable and hope for the best.
            self.machine.consume(1)
            return 'STATE_STRING'

class CharState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.identity = 'STATE_CHAR'
    
    def next(self):
        ch = self.machine.lookahead()
        if ch == 'EOF':
            if self.machine.lifespan == 1:
                self.consume(1)
                self.emit('CHAR')
                return 'STATE_FINAL'
            else:
                print("End of file while reading char.")
                return 'STATE_ERROR'
        elif self.machine.lifespan == 0:
            if ch == '\\':
                self.ignore(1)
                part = self.machine.lookahead()
                StringState.consume_break(self)
                return 'STATE_CHAR'
            else:
                self.machine.consume(1)
            return 'STATE_CHAR'
        elif self.machine.lifespan == 1:
            if ch == "'":
                self.machine.consume(1)
                self.machine.emit('CHAR')
                return 'STATE_BEGIN'
            else:
                print("Characters can only contain one symbol.")
                return 'STATE_ERROR'
            
        
class WhereState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.identity = 'STATE_WHERE'
    
    def next(self):
        ch = self.machine.lookahead()
        if ch == 'EOF':
            if self.machine.lifespan == 4:
                self.machine.emit('KEYWORD_WHERE')
            else:
                self.machine.emit('id')
            return 'STATE_FINAL'
        elif ch == 'h' and self.machine.lifespan == 0:
            self.machine.consume(1)
            return 'STATE_WHERE'
        elif ch == 'e' and self.machine.lifespan == 1:
            self.machine.consume(1)
            return 'STATE_WHERE'
        elif ch == 'r' and self.machine.lifespan == 2:
            self.machine.consume(1)
            return 'STATE_WHERE'
        elif ch == 'e' and self.machine.lifespan == 3:
            self.machine.consume(1)
            return 'STATE_WHERE'
        elif self.machine.lifespan == 4:
            if ch in IdState.symbol_valid:
                self.machine.consume(1)
                return 'STATE_ID'
            self.machine.emit('KEYWORD_WHERE')
            return 'STATE_BEGIN'
        else:
            if ch in IdState.symbol_valid:
                self.machine.consume(1)
                return 'STATE_ID'
            else:
                self.machine.emit('id')
                return 'STATE_BEGIN'

class UsingState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.identity = 'STATE_USING'
    
    def next(self):
        ch = self.machine.lookahead()
        if ch == 'EOF':
            if self.machine.lifespan == 4:
                self.machine.emit('KEYWORD_USING')
            else:
                self.machine.emit('id')
            return 'STATE_FINAL'
        elif ch == 's' and self.machine.lifespan == 0:
            self.machine.consume(1)
            return 'STATE_USING'
        elif ch == 'i' and self.machine.lifespan == 1:
            self.machine.consume(1)
            return 'STATE_USING'
        elif ch == 'n' and self.machine.lifespan == 2:
            self.machine.consume(1)
            return 'STATE_USING'
        elif ch == 'g' and self.machine.lifespan == 3:
            self.machine.consume(1)
            return 'STATE_USING'
        elif self.machine.lifespan == 4:
            if ch in IdState.symbol_valid:
                self.machine.consume(1)
                return 'STATE_ID'
            self.machine.emit('KEYWORD_USING')
            return 'STATE_BEGIN'
        else:
            if ch in IdState.symbol_valid:
                self.machine.consume(1)
                return 'STATE_ID'
            else:
                self.machine.emit('id')
                return 'STATE_BEGIN'

class OtherwiseState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.identity = 'STATE_OTHERWISE'
    
    def next(self):
        ch = self.machine.lookahead()
        if ch == 'EOF':
            if self.machine.lifespan == 8:
                self.machine.emit('KEYWORD_OTHERWISE')
            else:
                self.machine.emit('id')
            return 'STATE_FINAL'
        elif ch == 'f' and self.machine.lifespan == 0:
            self.machine.consume(1)
            la = self.machine.lookahead()
            if not la in IdState.symbol_valid:
                self.machine.emit('KEYWORD_OF')
                return 'STATE_BEGIN'
            else:
                self.consume(1)
                return 'STATE_ID'
        elif ch == 't' and self.machine.lifespan == 0:
            self.machine.consume(1)
            return 'STATE_OTHERWISE'
        elif ch == 'h' and self.machine.lifespan == 1:
            self.machine.consume(1)
            return 'STATE_OTHERWISE'
        elif ch == 'e' and self.machine.lifespan == 2:
            self.machine.consume(1)
            return 'STATE_OTHERWISE'
        elif ch == 'r' and self.machine.lifespan == 3:
            self.machine.consume(1)
            return 'STATE_OTHERWISE'
        elif ch == 'w' and self.machine.lifespan == 4:
            self.machine.consume(1)
            return 'STATE_OTHERWISE'
        elif ch == 'i' and self.machine.lifespan == 5:
            self.machine.consume(1)
            return 'STATE_OTHERWISE'
        elif ch == 's' and self.machine.lifespan == 6:
            self.machine.consume(1)
            return 'STATE_OTHERWISE'
        elif ch == 'e' and self.machine.lifespan == 7:
            self.machine.consume(1)
            return 'STATE_OTHERWISE'
        elif self.machine.lifespan == 8:
            if ch in IdState.symbol_valid:
                self.machine.consume(1)
                return 'STATE_ID'
            self.machine.emit('KEYWORD_OTHERWISE')
            return 'STATE_BEGIN'
        else:
            if ch in IdState.symbol_valid:
                self.machine.consume(1)
                return 'STATE_ID'
            else:
                self.machine.emit('id')
                return 'STATE_BEGIN'
                
class MinusState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.identity = 'STATE_MINUS'
    
    def next(self):
        ch = self.machine.lookahead()
        if ch == 'EOF':
            self.machine.emit('MINUS')
            return 'STATE_FINAL'
        elif ch == '>':
            self.machine.consume(1)
            self.machine.emit('FUNCTION_OPERATOR')
            return 'STATE_BEGIN'
        else:
            self.machine.emit('MINUS')
            return 'STATE_BEGIN'
        
class ElseState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.identity = 'STATE_ELSE'
    
    def next(self):
        ch = self.machine.lookahead()
        if ch == 'EOF':
            if self.machine.lifespan == 3:
                self.machine.emit('KEYWORD_ELSE')
            else:
                self.machine.emit('id')
            return 'STATE_FINAL'
        elif ch == 'l' and self.machine.lifespan == 0:
            self.machine.consume(1)
            return 'STATE_ELSE'
        elif ch == 'n' and self.machine.lifespan == 0:
            self.machine.consume(1)
            return 'STATE_END'
        elif ch == 's' and self.machine.lifespan == 1:
            self.machine.consume(1)
            return 'STATE_ELSE'
        elif ch == 'e' and self.machine.lifespan == 2:
            self.machine.consume(1)
            return 'STATE_ELSE'
        elif self.machine.lifespan == 3:
            if ch in IdState.symbol_valid:
                self.machine.consume(1)
                return 'STATE_ID'
            self.machine.emit('KEYWORD_ELSE')
            return 'STATE_BEGIN'
        else:
            if ch in IdState.symbol_valid:
                self.machine.consume(1)
                return 'STATE_ID'
            else:
                self.machine.emit('id')
                return 'STATE_BEGIN'

class EndState(State):
    # Transitions from ElseState
    def __init__(self, machine):
        super().__init__(machine)
        self.identity = 'STATE_END'
    
    def next(self):
        ch = self.machine.lookahead()
        if ch == 'EOF':
            if self.machine.lifespan == 1:
                self.machine.emit('KEYWORD_END')
            else:
                self.machine.emit('id')
            return 'STATE_FINAL'
        elif ch == 'd' and self.machine.lifespan == 0:
            self.machine.consume(1)
            return 'STATE_END'
        elif self.machine.lifespan == 1:
            if ch in IdState.symbol_valid:
                self.machine.consume(1)
                return 'STATE_ID'
            self.machine.emit('KEYWORD_END')
            return 'STATE_BEGIN'
        else:
            if ch in IdState.symbol_valid:
                self.machine.consume(1)
                return 'STATE_ID'
            else:
                self.machine.emit('id')
                return 'STATE_BEGIN'
                
class IfState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.identity = 'STATE_IF'
    
    def next(self):
        ch = self.machine.lookahead()
        if ch == 'EOF':
            if self.machine.lifespan == 1:
                self.machine.emit('KEYWORD_IF')
            else:
                self.machine.emit('id')
            return 'STATE_FINAL'
        elif ch == 'f' and self.machine.lifespan == 0:
            self.machine.consume(1)
            return 'STATE_IF'
        elif self.machine.lifespan == 1:
            if ch in IdState.symbol_valid:
                self.machine.consume(1)
                return 'STATE_ID'
            self.machine.emit('KEYWORD_IF')
            return 'STATE_BEGIN'
        else:
            if ch in IdState.symbol_valid:
                self.machine.consume(1)
                return 'STATE_ID'
            else:
                self.machine.emit('id')
                return 'STATE_BEGIN'

class ThenState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.identity = 'STATE_THEN'
    
    def next(self):
        ch = self.machine.lookahead()
        if ch == 'EOF':
            if self.machine.lifespan == 3:
                self.machine.emit('KEYWORD_THEN')
            else:
                self.machine.emit('id')
            return 'STATE_FINAL'
        elif ch == 'h' and self.machine.lifespan == 0:
            self.machine.consume(1)
            return 'STATE_THEN'
        elif ch == 'e' and self.machine.lifespan == 1:
            self.machine.consume(1)
            return 'STATE_THEN'
        elif ch == 'n' and self.machine.lifespan == 2:
            self.machine.consume(1)
            return 'STATE_THEN'
        elif self.machine.lifespan == 3:
            if ch in IdState.symbol_valid:
                self.machine.consume(1)
                return 'STATE_ID'
            self.machine.emit('KEYWORD_THEN')
            return 'STATE_BEGIN'
        else:
            if ch in IdState.symbol_valid:
                self.machine.consume(1)
                return 'STATE_ID'
            else:
                self.machine.emit('id')
                return 'STATE_BEGIN'
                
class ConditionalState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.identity = 'STATE_CONDITIONAL'
        
    def next(self):
        fch = self.machine.buffer
        ch = self.machine.lookahead()
        if fch == '=' and ch == '=':
            self.machine.consume(1)
            self.machine.emit('COND_EQUALS')
            return 'STATE_BEGIN'
        elif ch == 'EOF':
            self.machine.consume(1)
            self.machine.emit(BeginState.operator_lookup[fch])
            return 'STATE_FINAL'
        elif fch == '>' and ch == '=':
            self.machine.consume(1)
            self.machine.emit('GTEQUAL')
            return 'STATE_BEGIN'
        elif fch == '>' and ch == '>':
            self.machine.consume(1)
            self.machine.emit('TUP_FORWARD')
            return 'STATE_BEGIN'
        elif fch == '<' and ch == '=':
            self.machine.consume(1)
            self.machine.emit('LTEQUAL')
            return 'STATE_BEGIN'
        elif fch == '!' and ch == '=':
            self.machine.consume(1)
            self.machine.emit('NOTEQUAL')
            return 'STATE_BEGIN'
        elif fch == '=':
            self.machine.emit('EQUAL')
            return 'STATE_BEGIN'
        elif fch == '>':
            self.machine.emit('GREATER_THAN')
            return 'STATE_BEGIN'
        elif fch == '<':
            self.machine.emit('LESS_THAN')
            return 'STATE_BEGIN'
        return 'STATE_ERROR'
        
class DefState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.identity = 'STATE_DEF'
    
    def next(self):
        ch = self.machine.lookahead()
        if ch == 'EOF':
            if self.machine.lifespan == 2:
                self.machine.emit('KEYWORD_DEF')
            else:
                self.machine.emit('id')
            return 'STATE_FINAL'
        elif ch == 'e' and self.machine.lifespan == 0:
            self.machine.consume(1)
            return 'STATE_DEF'
        elif ch == 'f' and self.machine.lifespan == 1:
            self.machine.consume(1)
            return 'STATE_DEF'
        elif self.machine.lifespan == 2:
            if ch in IdState.symbol_valid:
                self.machine.consume(1)
                return 'STATE_ID'
            self.machine.emit('KEYWORD_DEF')
            return 'STATE_BEGIN'
        else:
            if ch in IdState.symbol_valid:
                self.machine.consume(1)
                return 'STATE_ID'
            else:
                self.machine.emit('id')
                return 'STATE_BEGIN'
        
class IdState(State):
    symbol_initials = string.ascii_letters + '_'
    symbol_valid = string.ascii_letters + '_' + string.digits
    
    def __init__(self, machine):
        super().__init__(machine)
        self.identity = 'STATE_ID'
        
    def next(self):
        ch = self.machine.lookahead()
        if ch == 'EOF':
            self.machine.emit('id')
            return 'STATE_FINAL'
        elif ch in IdState.symbol_valid:
            self.machine.consume(1)
            return 'STATE_ID'
        else:
            self.machine.emit('id')
            return 'STATE_BEGIN'

class KeywordNotState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.identity = 'STATE_NOT'
    
    def next(self):
        ch = self.machine.lookahead()
        if ch == 'EOF':
            if self.machine.lifespan == 2:
                self.machine.emit('KEYWORD_NOT')
            else:
                self.machine.emit('id')
            return 'STATE_FINAL'
        elif ch == 'e' and self.machine.lifespan == 0:
            self.machine.consume(1)
            return 'STATE_NEW'
        elif ch == 'o' and self.machine.lifespan == 0:
            self.machine.consume(1)
            return 'STATE_NOT'
        elif ch == 't' and self.machine.lifespan == 1:
            self.machine.consume(1)
            return 'STATE_NOT'
        elif self.machine.lifespan == 2:
            if ch in IdState.symbol_valid:
                self.machine.consume(1)
                return 'STATE_ID'
            self.machine.emit('KEYWORD_NOT')
            return 'STATE_BEGIN'
        else:
            if ch in IdState.symbol_valid:
                self.machine.consume(1)
                return 'STATE_ID'
            else:
                self.machine.emit('id')
                return 'STATE_BEGIN'

class KeywordNewState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.identity = 'STATE_NEW'
    
    def next(self):
        ch = self.machine.lookahead()
        if ch == 'EOF':
            if self.machine.lifespan == 1:
                self.machine.emit('KEYWORD_NEW')
            else:
                self.machine.emit('id')
            return 'STATE_FINAL'
        elif ch == 'w' and self.machine.lifespan == 0:
            self.machine.consume(1)
            return 'STATE_NEW'
        elif self.machine.lifespan == 1:
            if ch in IdState.symbol_valid:
                self.machine.consume(1)
                return 'STATE_ID'
            self.machine.emit('KEYWORD_NEW')
            return 'STATE_BEGIN'
        else:
            if ch in IdState.symbol_valid:
                self.machine.consume(1)
                return 'STATE_ID'
            else:
                self.machine.emit('id')
                return 'STATE_BEGIN'
            
class IntegerState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.identity = 'STATE_INTEGER'
        
    def next(self):
        ch = self.machine.lookahead()
        if ch == 'EOF':
            self.machine.emit('INTEGER')
            return 'STATE_FINAL'
        elif ch == '.':
            self.machine.consume(2)
            return 'STATE_FLOAT'
        elif ch in '0123456789':
            self.machine.consume(1)
            return 'STATE_INTEGER'
        else:
            self.machine.emit('INTEGER')
            return 'STATE_BEGIN'

class FloatState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.identity = 'STATE_FLOAT'
    
    def next(self):
        ch = self.machine.lookahead()
        if ch == 'EOF':
            self.machine.emit('FLOAT')
            return 'STATE_FINAL'
        elif ch in '012345679':
            self.machine.consume(1)
            return 'STATE_FLOAT'
        elif ch == 'f':
            self.machine.ignore(1)
            self.machine.emit('FLOAT')
            return 'STATE_BEGIN'
        elif ch == 'd':
            self.machine.ignore(1)
            self.machine.emit('DOUBLE')
            return 'STATE_BEGIN'
        else:
            self.machine.emit('FLOAT')
            return 'STATE_BEGIN'

# I don't get why I didn't just build the list from each class. I don't get a lot of things I do.
InitialiserList = [CaseState, StringState, CharState, OtherwiseState, UsingState, WhereState, MinusState, EndState, ElseState, ThenState, IfState, ConditionalState, DefState, KeywordNewState, KeywordNotState, ErrorState, BeginState, FinalState, IdState, IntegerState, FloatState]