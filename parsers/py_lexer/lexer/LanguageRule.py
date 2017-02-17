from .LanguageClass import LanguageClass
from .LanguageChain import LanguageChain

def ChainRule(language_class, *rulechain):
    chain = LanguageChain()
    for x in rulechain:
        chain.addRule(x)
        
    def internal_decorator(f):
        chain.setMethod(f)
        language_class.addChain(chain)
        return f
    return internal_decorator

def LanguageRule(language_class, word_class):
    if not isinstance(language_class, LanguageClass):
        raise ValueError("argument 0 for LanguageRule decorator is not a LanguageClass")
    if not isinstance(word_class, str):
        raise ValueError("argument 1 for LanguageRule is not a string")
    
    def internal_decorator(f):
        language_class.addRuleMethod(word_class, f)
        return f
    return internal_decorator
