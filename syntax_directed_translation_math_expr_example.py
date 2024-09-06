from grammar import Grammar
from token_sequence_2 import token_sequence
from ll1_check import is_ll1
from predict import predict_algorithm
import re

'''
S -> E $
E -> T E'
E' -> epsilon
E' -> + T E'
E' -> - T E'
T -> F T'
T' -> * F T'
T' -> / F T'
T' -> vazio
F -> num
F -> ( E )
'''


regex_table = {
    r'^\+$': '+',
    r'^\-$': '-',
    r'^\*$': '*',
    r'^/$': '/',
    r'^\($': '(',
    r'^\)$': ')',
    r'[0-9]+': 'num'
}


def lexical_analyser(filepath) -> str:
    with open(filepath, 'r') as f:
        token_sequence = []
        tokens = []
        for line in f:
            tokens = tokens + line.split(' ')
        for t in tokens:
            found = False
            for regex, category in regex_table.items():
                if re.match(regex, t):
                    token_sequence.append((category, t))
                    found = True
            if not found:
                print('Lexical error: ', t)
                exit(0)
    token_sequence.append('$')
    return token_sequence


def create_ac_grammar() -> Grammar:
    G = Grammar()
    G.add_production('S', ['E', '$'])
    G.add_production('E', ['T', 'E2'])
    G.add_production('E2', [])
    G.add_production('E2', ['+', 'T', 'E2'])
    G.add_production('E2', ['-', 'T', 'E2'])
    G.add_production('T', ['F', 'T2'])
    G.add_production('T2', ['*', 'F', 'T2'])
    G.add_production('T2', ['/', 'F', 'T2'])
    G.add_production('T2', [])
    G.add_production('F', ['num'])
    G.add_production('F', ['(', 'E', ')'])
    G.add_terminal('+')
    G.add_terminal('-')
    G.add_terminal('*')
    G.add_terminal('/')
    G.add_terminal('(')
    G.add_terminal(')')
    G.add_terminal('num')
    G.add_terminal('$')
    G.add_nonterminal('S')
    G.add_nonterminal('E')
    G.add_nonterminal('E2')
    G.add_nonterminal('T')
    G.add_nonterminal('F')
    G.add_nonterminal('T2')
    return G

# S -> E $
def S(ts:token_sequence,p:predict_algorithm)->float:
    if ts.peek() in p.predict(0):
        val = E(ts,p)
        ts.match('$')
        return val
    else:
        print('Syntax error in S')
        exit(0)

# E -> T E'
def E(ts:token_sequence,p:predict_algorithm)->float:
    if ts.peek() in p.predict(1):
        val = T(ts,p)
        val2 = E2(ts,p)
        return val + val2
    else:
        print('Syntax error in E')
        exit(0)

# E' -> epsilon
# E' -> + T E'
#  E' -> - T E'

def E2(ts:token_sequence,p:predict_algorithm)->float:
    if ts.peek() in p.predict(2):
        return 0
    elif ts.peek() in p.predict(3):
        ts.match('+')
        val = T(ts,p)
        val2 = E2(ts,p)
        return val+val2
    elif ts.peek() in p.predict(4):
        ts.match('-')
        val =  T(ts,p)
        val2 = E2(ts,p)
        return -(val+val2)
    else:
        print('Syntax error in E\'')
        exit(0)
    
# T -> F T'
def T(ts:token_sequence,p:predict_algorithm)->float:
   if ts.peek() in p.predict(5):
       val = F(ts,p)
       val2 = T2(ts,p)
       return val*val2 
   else:
       print('Syntax error')
       exit(0)

# T' -> * F T'
# T' -> / F T'
# T' -> vazio

def T2(ts:token_sequence,p:predict_algorithm)->float:
    if ts.peek() in p.predict(6):
        ts.match('*')
        val = F(ts,p)
        val2 = T2(ts,p)
        return val*val2
    elif ts.peek() in p.predict(7):
        ts.match('/')
        val = F(ts,p)
        val2 = T2(ts,p)
        return 1/(val*val2)
    elif ts.peek() in p.predict(8):
        return 1
    else:
        print('Syntax error in T\'')
        exit(0)

def F(ts:token_sequence,p:predict_algorithm)->float:
    if ts.peek() in p.predict(9):
        val =  ts.value()
        ts.match('num')
        return val
    elif ts.peek() in p.predict(10):
        ts.match('(')
        val = E(ts,p)
        ts.match(')')
        return val
    else:
        print('Syntax error in F')
        exit(0)

if __name__ == '__main__':
    filepath = 'expr.txt'
    tokens = lexical_analyser(filepath)
    ts = token_sequence(tokens)
    G = create_ac_grammar()
    p_alg = predict_algorithm(G)
    print(is_ll1(G, p_alg))
    print(S(ts,p_alg))
