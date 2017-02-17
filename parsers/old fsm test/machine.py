class Token(object):
    def __init__(self, name, value):
        self.identifier = name
        self.value = value
        
    def __str__(self):
        return "<%s '%s'>" % (self.identifier, str(self.value))

class StateException(Exception): pass
        
class State(object):
    def __init__(self, machine):
        self.machine = machine
    
    def next(self):
        if identity in self.__dict__:
            raise StateException("Unimplemented next method in '%s'" % (self.identity))
        else:
            raise StateException("Unimplemented next method in a state, furthermore no identity has been defined.")

class MachineException(Exception): pass
            
class MachineContext(object):
    def __init__(self, parent, input_buffer):
        self.input = input_buffer
        self.parent = parent
        self.offset = 0
        self.buffer = ""
        self.tokens = []
        self.states = {}
        self.alive = True
        self.emitted = False
        self.state = parent.initial
        self.lifespan = 0
        
    def consume(self, length):
        if self.offset < len(self.input):
            self.buffer += self.input[self.offset : self.offset + length]
            self.offset += length
    
    def presume(self, s):
        self.buffer += s
    
    def ignore(self, length):
        self.offset += length
    
    def emit(self, identity):
        # Please forgive me, future self.
        if identity == 'id' and (self.buffer == self.buffer.upper()):
            identity = 'atom'
        self.tokens.append(Token(identity, self.buffer))
        self.buffer = ""
        self.emitted = True
        self.lifespan = 0
        
    def lookahead(self, length=1):
        if self.offset >= len(self.input):
            return 'EOF'
        else:
            return self.input[self.offset : self.offset + length]
        
    def finish(self):
        self.alive = False
        
    def valid(self):
        return self.alive
        
    def next(self):
        if not self.alive:
            return None
        
        if self.emitted:
            self.emitted = False
            return self.tokens[-1]
            
        while not self.emitted and self.valid():
            if not self.state in self.states:
                print(list(map(str, self.tokens)))
                raise MachineException("Unacceptable state produced by state machine.")
            #print(self.state)
            old_state = self.state
            self.state = self.states[self.state].next()
            if old_state == self.state:
                self.lifespan += 1
            else:
                self.lifespan = 0
        
        if self.emitted:
            self.emitted = False
            return self.tokens[-1]
        else:
            # Possibly a final state, should better handle this maybe.
            return None
            
class Machine(object):
    def __init__(self):
        self.initial = None
        self.states = {}
        self.constructors = []
        
    def addStateConstructor(self, constructor):
        self.constructors.append(constructor)
        
    def stream(self, buffer):
        context = MachineContext(self, buffer)
        for x in self.constructors:
            state = x(context)
            context.states[state.identity] = state
        return context