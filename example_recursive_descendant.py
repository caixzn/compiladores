import sys
from token_sequence import token_sequence
from predict import predict_algorithm
from grammar import Grammar
import re
from ll1_check import is_ll1
regular_expression = {
    r'^a$': 'a',
    r'^b$': 'b',
    r'^c$': 'c',
    r'^d$': 'd',
    r'^q$': 'q'
}

def lexical_analyser(filepath) -> str:
    with open(filepath,'r') as f:
        token_sequence = []
        tokens = []
        line_number = 1
        for line in f:
            for c in line:
                tokens.append(c)
        print(f'tokens = {tokens}')
        for t in tokens:
            found = False
            if "\n" in t:
                line_number += 1
            for regex,category in regular_expression.items():
                if re.match(regex,t):
                    token_sequence.append(category)
                    found = True
            if not found:
                print('Lexical error in line', line_number, ':',t)
                exit(1)
    token_sequence.append('$')
    print(f'token_sequence = {token_sequence}')
    return token_sequence

def create_language_grammar():
    G = Grammar()
    G.add_terminal('a') # 0
    G.add_terminal('b') # 1
    G.add_terminal('c') # 2
    G.add_terminal('d') # 3
    G.add_terminal('q') # 4
    G.add_terminal('$') # 5
    G.add_nonterminal('S') # 6
    G.add_nonterminal('A') # 7
    G.add_nonterminal('B') # 8
    G.add_nonterminal('C') # 9
    G.add_nonterminal('Q') # 10
    G.add_production('S',['A','C','$']) # 11
    G.add_production('C',['c']) # 12
    G.add_production('C',[]) # 13
    G.add_production('A',['a','B','C','d']) # 14
    G.add_production('A',['B','Q']) # 15
    G.add_production('B',['b','B']) # 16
    G.add_production('B',[]) # 17
    G.add_production('Q',['q']) # 18
    G.add_production('Q',[]) # 19
    return G

def PrintGrammar(G:Grammar)->None:
    for x in G.productions():
        print(x,G.lhs(x),'->',G.rhs(x))

def print_syntax_error(ts:token_sequence,predset:set):
    predstr = ','.join(list(predset))
    print(f'Syntax error: Found {ts.peek()}, expected: {predstr}')

def S(ts:token_sequence,pred:predict_algorithm):
    if ts.peek() in pred.predict(11):
        A(ts,pred)
        C(ts,pred)
        ts.match('$')
    else:
        predset = set()
        predset.update(pred.predict(11))
        print_syntax_error(ts,predset)

def C(ts:token_sequence,pred:predict_algorithm):
    if ts.peek() in pred.predict(12):
        ts.match('c')
    elif ts.peek() in pred.predict(13):
        return
    else:
        predset = set()
        predset.update(pred.predict(12))
        predset.update(pred.predict(13))
        print_syntax_error(ts,predset)        

def A(ts:token_sequence,pred:predict_algorithm):
    if ts.peek() in pred.predict(14):
        ts.match('a')
        B(ts,pred)
        C(ts,pred)
        ts.match('d')
    elif ts.peek() in pred.predict(15):
        B(ts,pred)
        Q(ts,pred)
    else:
        predset = set()
        predset.update(pred.predict(14))
        predset.update(pred.predict(15))
        print_syntax_error(ts,predset)        

def B(ts:token_sequence,pred:predict_algorithm):
    if ts.peek() in pred.predict(16):
        ts.match('b')
        B(ts,pred)
    elif ts.peek() in pred.predict(17):
        return
    else:
        predset = set()
        predset.update(pred.predict(16))
        predset.update(pred.predict(17))
        print_syntax_error(ts,predset)        

def Q(ts:token_sequence,pred:predict_algorithm):
    if ts.peek() in pred.predict(18):
        ts.match('q')
    elif ts.peek() in pred.predict(19):
        return
    else:
        predset = set()
        predset.update(pred.predict(18))
        predset.update(pred.predict(19))
        print_syntax_error(ts,predset)

if __name__ == '__main__':
    # filepath = sys.argv
    filepath = 'example_recursive_descendant_input.txt'
    tokens = lexical_analyser(filepath)
    ts = token_sequence(tokens)
    G = create_language_grammar()
    p_alg = predict_algorithm(G)
    PrintGrammar(G)
    print('LL(1) ? ',is_ll1(G, p_alg))
    S(ts,p_alg)
    print('Compilation success!')
