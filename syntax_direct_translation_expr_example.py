import re
from grammar import Grammar
from token_sequence_2 import token_sequence
from predict import predict_algorithm


def create_expr_grammar() -> Grammar:
    G = Grammar()
    G.add_terminal('num')
    G.add_terminal('+')
    G.add_terminal('*')
    G.add_terminal('$')
    G.add_nonterminal('Start')
    G.add_nonterminal('E')
    G.add_nonterminal('E\'')
    G.add_nonterminal('T')
    G.add_nonterminal('T\'')
    G.add_nonterminal('F')
    G.add_production('Start', ['E', '$'])  # 10
    G.add_production('E', ['T', 'E\''])  # 11
    G.add_production('E\'', [])  # 12
    G.add_production('E\'', ['+', 'T', 'E\''])  # 13
    G.add_production('T', ['F', 'T\''])  # 14
    G.add_production('T\'', ['*','F','T\'']) # 15
    G.add_production('T\'', [])  # 16
    G.add_production('F', ['num'])  # 17
    return G


regex_table = {
    r'^\+$': '+',
    r'^\*$': '*',
    r'^[0-9]+$': 'num',
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
    token_sequence.append(('$', None))
    print(token_sequence)
    return token_sequence


def Start(ts: token_sequence, p: predict_algorithm) -> int:
    if ts.peek() in p.predict(10):
        # print('8')
        val = E(ts, p)
        ts.match('$')
        return val
    else:
        print('Syntax error in Start')
        exit(0)


def E(ts: token_sequence, p: predict_algorithm) -> int:
    if ts.peek() in p.predict(11):
        # print('9')
        val = T(ts, p)
        val += E2(ts, p)
        return val
    else:
        print('Syntax error in E')


def E2(ts: token_sequence, p: predict_algorithm) -> int:
    if ts.peek() in p.predict(12):
        # print('10')
        return 0
    elif ts.peek() in p.predict(13):
        # print('11')
        ts.match('+')
        val = T(ts, p)
        val2 = E2(ts, p)
        return val + val2
    else:
        print('Syntax error in E\'')


def T(ts: token_sequence, p: predict_algorithm) -> int:
    if ts.peek() in p.predict(14):
        # print('12')
        val = F(ts,p)        
        val2  = T2(ts, p)
        return val*val2
    else:
        print('Syntax error in T')
        exit(0)


def T2(ts: token_sequence, p: predict_algorithm) -> int:
    if ts.peek() in p.predict(15):
        # print('13')
        ts.match('*')
        val = F(ts, p)
        val2 = T2(ts,p)
        return val*val2
    elif ts.peek() in p.predict(16):
        return 1
    else:
        print('Syntax error in T\'')
        exit(0)

def F(ts: token_sequence, p: predict_algorithm) -> int:
    if ts.peek() in p.predict(17):
        val = ts.value()
        ts.match('num')
        return val
    else:
        print('Syntax error in F')
        exit(0)


if __name__ == '__main__':
    filepath = 'expr.txt'
    tokens = lexical_analyser(filepath)
    ts = token_sequence(tokens)
    print(ts)
    G = create_expr_grammar()
    p_alg = predict_algorithm(G)
    for i in range(10,18):
        print(f'predict({i})',p_alg.predict(i))
    print('Resultado: ', Start(ts, p_alg))
