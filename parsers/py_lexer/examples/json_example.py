from lexer import LanguageRule, LanguageClass, LanguageToken, ChainRule

json = LanguageClass('json')
json.shouldSkipWhitespace(True)

# Single-character rules.

json.addSingleCharacterRule(',', 'comma')
json.addSingleCharacterRule('[', 'list_open')
json.addSingleCharacterRule(']', 'list_close')
json.addSingleCharacterRule('{', 'brace_open')
json.addSingleCharacterRule('}', 'brace_close')
json.addSingleCharacterRule(':', 'colon')

# Number rules.

@ChainRule(json, 'integer', 'frac')
def FloatRule(stream, values):
    values = (x.value for x in values)
    return LanguageToken('float', ''.join(values))

@ChainRule(json, 'integer', 'exp')
def IntegerExponentRule(stream, values):
    values = (x.value for x in values)
    intnum = str(int(float(''.join(values))))
    return LanguageToken('integer', intnum)

@ChainRule(json, 'float', 'exp')
def FloatExponentRule(stream, values):
    values = (x.value for x in values)
    return LanguageToken('float', str(float(''.join(values))))

@LanguageRule(json, 'integer')
def NumberRule(stream, value):
    r'[0-9]+'
    stream.advance(len(value))
    return LanguageToken('integer', value)

@LanguageRule(json, 'frac')
def FracRule(stream, value):
    r'[.][0-9]+'
    stream.advance(len(value))
    return LanguageToken('frac', value)
    
@LanguageRule(json, 'exp')
def ExpRule(stream, value):
    r'([Ee]|[Ee][+-])[0-9]+'
    stream.advance(len(value))
    return LanguageToken('exp', value)
    
# String rule.
@LanguageRule(json, 'string')
def StringRule(stream, value):
    r'["]([\\][bfnrt\/\\]|[^\\"])+["]'
    stream.advance(len(value))
    return LanguageToken('string', value)
