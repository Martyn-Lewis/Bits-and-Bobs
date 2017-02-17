import json_example
from lexer import LanguageMachine

machine = LanguageMachine(json_example.json)
json_string = '{"abc":123, "ab":123.123, "a":123e+4, "d":123.321e+4, "e": ["asd", "sdf", 123]}'
stream = machine.createStream(json_string)

for x in stream.generator():
    print(x.value, x.identifier)

# TODO: Actual tests perhaps?
