import re
from grammar import Grammar
from token_sequence import token_sequence
from predict import predict_algorithm

def create_ac_grammar()->Grammar:
    G = Grammar()
    G.add_terminal('floatdcl')
    G.add_terminal('intdcl')
    G.add_terminal('print')
    G.add_terminal('id')
    G.add_terminal('assign')
    G.add_terminal('plus')
    G.add_terminal('minus')
    G.add_terminal('inum')
    G.add_terminal('fnum')
    G.add_nonterminal('Prog')
    G.add_nonterminal('Dcls')
    G.add_nonterminal('Dcl')
    G.add_nonterminal('Stmts')
    G.add_nonterminal('Stmt')
    G.add_nonterminal('Expr')
    G.add_nonterminal('Val')
    G.add_production('Prog',['Dcls','Stmts','$']) # 16
    G.add_production('Dcls',['Dcl','Dcls']) # 17
    G.add_production('Dcls',[]) # 18
    G.add_production('Dcl',['floatdcl','id']) # 19
    G.add_production('Dcl',['intdcl','id']) # 20
    G.add_production('Stmts',['Stmt','Stmts']) # 21
    G.add_production('Stmts',[]) # 22
    G.add_production('Stmt',['id','assign','Val','Expr']) # 23
    G.add_production('Stmt',['print','id']) # 24
    G.add_production('Expr',['plus','Val','Expr']) # 25
    G.add_production('Expr',['minus','Val','Expr']) # 26
    G.add_production('Expr',[]) # 27
    G.add_production('Val',['id']) # 28
    G.add_production('Val',['inum']) # 29
    G.add_production('Val',['fnum']) # 30


regex_table = {
    r'^f$': 'floatdcl',
    r'^i$': 'intdcl',
    r'^p$': 'print',
    r'^[abcdeghjlmnoqrstuvwxyz]$' : 'id',
    r'^=$':'assign',
    r'^\+$': 'plus',
    r'^\-$': 'minus',
    r'^[0-9]+$': 'inum',
    r'^[0-9]+\.[0-9]+$': 'fnum'
}

def lexical_analyser(filepath) -> str:
    with open(filepath,'r') as f:
        token_sequence = []
        tokens = []
        for line in f:
            tokens = tokens + line.split(' ')
        for t in tokens:
            found = False
            for regex,category in regex_table.items():
                if re.match(regex,t):
                    token_sequence.append(category)
                    found=True
            if not found:
                print('Lexical error: ',t)
                exit(0)
    token_sequence.append('$')
    return token_sequence

def Prog(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() == p.predict(16):
        Dcls()
        Stmts()
        ts.match('$')

if __name__ == '__main__':
    filepath = 'programa.ac'
    tokens = lexical_analyser(filepath)
    ts = token_sequence(tokens)
    G = create_ac_grammar()
    p_alg = predict_algorithm(G)
    Prog(ts,p_alg)  