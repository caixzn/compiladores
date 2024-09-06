import re
from grammar import Grammar
from token_sequence import token_sequence
from predict import predict_algorithm
from ll1_check import is_ll1
import inspect
import traceback

def get_func_name():
    return inspect.stack()[1][3]

regular_expression = {
    r'^begin$': 'begin',
    r'^end$': 'end',
    r'^int$': 'int',
    r'^float$': 'float',
    r'^if$': 'if',
    r'^then$': 'then',
    r'^endif$': 'endif',
    r'^else$': 'else',
    r'^endelse$': 'endelse',
    r'^while$': 'while',
    r'^do$': 'do',
    r'^endwhile$': 'endwhile',
    r'^print$' : 'print',
    r'^scan$' : 'scan',
    r'^\($': '(',
    r'^\)$': ')',
    r'^\+$': '+',
    r'^\-$': '-',
    r'^\*$': '*',
    r'^/$': '/',
    r'^=$': '=',
    r'^==$': '==',
    r'^<$': '<',
    r'^<=$': '<=',
    r'^>$': '>',
    r'^>=$': '>=',
    r'^!=$': '!=',
    r'^(?!^if$|^then$|^endif$|^else$|^endelse$|^while$|^do$|^endwhile$|^int$|^float$|^begin$|^end$|^print$|^scan$)[A-Za-z][A-Za-z0-9]*$': 'identifier',
    r'^\d+$': 'integer',
    r'^\d+\.\d+$': 'floating-point'
}

def lexical_analyser(filepath) -> str:
    with open(filepath,'r') as f:
        token_sequence = []
        tokens = []
        line_number = 1
        for line in f:
            if line == "\n":
                continue
            tokens = tokens + line.split(' ')
        # print(tokens)
        for t in tokens:
            found = False
            if "\n" in t:
                line_number += 1
            for regex,category in regular_expression.items():
                if re.match(regex,t):
                    #token_sequence.append((category, t)) #mudança para tupla
                    token_sequence.append(category)
                    found = True
            if not found:
                print('Lexical error in line', line_number, ':',t)
                exit(1)
    print(token_sequence)
    token_sequence.append('$')
    return token_sequence

def create_language_grammar() -> Grammar:
    G = Grammar()
    G.add_terminal('begin') #1
    G.add_terminal('end') #2
    G.add_terminal('int')#3
    G.add_terminal('float')#4
    G.add_terminal('if')#5
    G.add_terminal('then')#6
    G.add_terminal('endif')#7
    G.add_terminal('else')#8
    G.add_terminal('endelse')#9
    G.add_terminal('while')#10
    G.add_terminal('do')#11
    G.add_terminal('endwhile')#12
    G.add_terminal('print')#13
    G.add_terminal('scan')#14
    G.add_terminal('(')#15
    G.add_terminal(')')#16
    G.add_terminal('+')#17
    G.add_terminal('-')#18
    G.add_terminal('*')#19
    G.add_terminal('/')#20
    G.add_terminal('=')#21
    G.add_terminal('==')#22
    G.add_terminal('<')#23
    G.add_terminal('<=')#24
    G.add_terminal('>')#25
    G.add_terminal('>=')#26
    G.add_terminal('!=')#27
    G.add_terminal('identifier')#28
    G.add_terminal('integer')#29
    G.add_terminal('floating-point')#30
    G.add_nonterminal('Program')#31
    G.add_nonterminal('ProgramBlock')#32
    G.add_nonterminal('Statement')#33
    G.add_nonterminal('Declaration')#34
    G.add_nonterminal('Assignment')#35
    G.add_nonterminal('Loop')#36
    G.add_nonterminal('Conditional')#37
    G.add_nonterminal('PrintScanCommand')#38
    G.add_nonterminal('ElseConditional')#39
    G.add_nonterminal('Condition')#40
    G.add_nonterminal('Expression')#41
    G.add_nonterminal('ExpressionTail')#42
    G.add_nonterminal('Term')#43
    G.add_nonterminal('TermTail')#44
    G.add_nonterminal('Factor')#45
    G.add_nonterminal('RelationalOperator')#46
    G.add_nonterminal('AdditiveOperator')#47
    G.add_nonterminal('MultiplicativeOperator')#48
    G.add_production('Program',['begin', 'ProgramBlock', 'end']) #49
    G.add_production('ProgramBlock',['Statement', 'ProgramBlock']) #50
    G.add_production('ProgramBlock',[]) #51
    G.add_production('Statement',['Declaration']) #52
    G.add_production('Statement',['Assignment']) #53
    G.add_production('Statement',['Loop']) #54
    G.add_production('Statement',['Conditional']) #55
    G.add_production('Statement',['PrintScanCommand']) #56
    G.add_production('Declaration',['int', 'identifier']) #57
    G.add_production('Declaration',['float', 'identifier']) #58
    G.add_production('Assignment',['identifier', '=', 'Expression']) #59
    G.add_production('Loop',['while', 'Condition', 'do', 'ProgramBlock', 'endwhile']) #60
    G.add_production('Conditional',['if', 'Condition', 'then', 'ProgramBlock', 'ElseConditional', 'endif']) #61
    G.add_production('ElseConditional',['else', 'ProgramBlock', 'endelse']) #62
    G.add_production('ElseConditional',[]) #63
    G.add_production('PrintScanCommand',['print', 'identifier']) #64
    G.add_production('PrintScanCommand',['scan', 'identifier']) #65
    G.add_production('Condition',['Expression', 'RelationalOperator', 'Expression']) #66
    G.add_production('Expression',['Term', 'ExpressionTail']) #67
    G.add_production('ExpressionTail',['AdditiveOperator', 'Term', 'ExpressionTail']) #68
    G.add_production('ExpressionTail',[]) #69
    G.add_production('Term',['Factor', 'TermTail']) #70
    G.add_production('TermTail',['MultiplicativeOperator', 'Factor', 'TermTail']) #71
    G.add_production('TermTail',[]) #72
    G.add_production('Factor',['integer']) #73
    G.add_production('Factor',['floating-point']) #74
    G.add_production('Factor',['identifier']) #75
    G.add_production('Factor',['(', 'Expression', ')']) #76
    G.add_production('RelationalOperator',['==']) #77
    G.add_production('RelationalOperator',['!=']) #78
    G.add_production('RelationalOperator',['<']) #79
    G.add_production('RelationalOperator',['>']) #80
    G.add_production('RelationalOperator',['<=']) #81
    G.add_production('RelationalOperator',['>=']) #82
    G.add_production('AdditiveOperator',['+']) #83
    G.add_production('AdditiveOperator',['-']) #84
    G.add_production('MultiplicativeOperator',['*']) #85
    G.add_production('MultiplicativeOperator',['/']) #86
    G.add_terminal('$')
    return G


def Program(ts:token_sequence,p:predict_algorithm)->None: #Talvez mudar esses Nones para manter os valores de numeros depois...
    if ts.peek() in p.predict(48):
        ts.match('begin')
        ProgramBlock(ts,p)
        ts.match('end')
    else:
        print('Syntax error at',get_func_name())
        exit(0)


def ProgramBlock(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(49):
        Statement(ts,p)
        ProgramBlock(ts,p)
    elif ts.peek() in p.predict(50):
        return
    else:
        print('Syntax error at',get_func_name())
        exit(0)

def Statement(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(51):
        Declaration(ts,p)
    elif ts.peek() in p.predict(52):
        Assignment(ts,p)
    elif ts.peek() in p.predict(53):
        Loop(ts,p)
    elif ts.peek() in p.predict(54):
        Conditional(ts,p)
    elif ts.peek() in p.predict(55):
        PrintScanCommand(ts,p)
    else:
        print('Syntax error at',get_func_name())
        exit(0)
def Declaration(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(56):
        ts.match('int')
        ts.match('identifier')
    elif ts.peek() in p.predict(57):
        ts.match('float')
        ts.match('identifier')
    else:
        print('Syntax error at',get_func_name())
        exit(0)

def Assignment(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(58):
        ts.match('identifier')
        ts.match('=')
        Expression(ts,p)
    else:
        print('Syntax error at',get_func_name())
        exit(0)

def Loop(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(59):
        ts.match('while')
        Condition(ts,p)
        ts.match('do')
        ProgramBlock(ts,p)
        ts.match('endwhile')
    else:
        print('Syntax error at',get_func_name())
        exit(0)

def Conditional(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(60):
        ts.match('if')
        Condition(ts,p)
        ts.match('then')
        ProgramBlock(ts,p)
        ElseConditional(ts,p)
        ts.match('endif')
    else:
        print('Syntax error at',get_func_name())
        exit(0)

def ElseConditional(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(61):
        ts.match('else')
        ProgramBlock(ts,p)
        ts.match('endelse')
    elif ts.peek() in p.predict(62):
        return
    else:
        print('Syntax error at',get_func_name())
        exit(0)

def PrintScanCommand(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(63):
        ts.match('print')
        ts.match('identifier')
    elif ts.peek() in p.predict(64):
        ts.match('scan')
        ts.match('identifier')
    else:
        print('Syntax error at',get_func_name())
        exit(0)

def Condition(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(65):
        Expression(ts,p)
        RelationalOperator(ts,p)
        Expression(ts,p)
    else:
        print('Syntax error at',get_func_name())
        exit(0)

def Expression(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(66):
        Term(ts,p)
        ExpressionTail(ts,p)
    else:
        print('Syntax error at',get_func_name())
        exit(0)

def ExpressionTail(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(67):
        AdditiveOperator(ts,p)
        Term(ts,p)
        ExpressionTail(ts,p)
    elif ts.peek() in p.predict(68):
        return
    else:
        print('Syntax error at',get_func_name())
        exit(0)

def Term(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(69):
        Factor(ts,p)
        TermTail(ts,p)
    else:
        print('Syntax error at',get_func_name())
        exit(0)

def TermTail(ts:token_sequence,p:predict_algorithm)->None:
    print('Term Peek: ',ts.peek())
    for i in range(70,72):
        print('Predict ',i,p.predict(i))
    if ts.peek() in p.predict(70):
        MultiplicativeOperator(ts,p)
        Factor(ts,p)
        TermTail(ts,p)
    elif ts.peek() in p.predict(71):
        return
    else:
        traceback.print_stack()
        l = list(p.predict(70).union(p.predict(71)))
        print('Syntax error at',get_func_name(),'expected:', ' or '.join(l),'found:',ts.peek())
        print('Token idx:',ts.get_idx())
        exit(0)

def Factor(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(72):
        ts.match('integer')
    elif ts.peek() in p.predict(73):
        ts.match('floating-point')
    elif ts.peek() in p.predict(74):
        ts.match('identifier')
    elif ts.peek() in p.predict(75):
        ts.match('(')
        Expression(ts,p)
        ts.match(')')
    else:
        print('Syntax error at',get_func_name())
        exit(0)

def RelationalOperator(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(76):
        ts.match('==')
    elif ts.peek() in p.predict(77):
        ts.match('!=')
    elif ts.peek() in p.predict(78):
        ts.match('<')
    elif ts.peek() in p.predict(79):
        ts.match('>')
    elif ts.peek() in p.predict(80):
        ts.match('<=')
    elif ts.peek() in p.predict(81):
        ts.match('>=')
    else:
        print('Syntax error at',get_func_name())
        exit(0)

def AdditiveOperator(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(82):
        ts.match('+')
    elif ts.peek() in p.predict(83):
        ts.match('-')
    else:
        print('Syntax error at',get_func_name())
        exit(0)

def MultiplicativeOperator(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(84):
        ts.match('*')
    elif ts.peek() in p.predict(85):
        ts.match('/')
    else:
        print('Syntax error at',get_func_name())
        exit(0)

def PrintGrammar(G:Grammar)->None:
    for x in G.productions():
        print(x,G.lhs(x),'->',G.rhs(x))

if __name__ == '__main__':
    filepath = 'programa.aalanguage'
    # filepath = 'Parser - Compiladores/dummy.aa'
    tokens = lexical_analyser(filepath)
    ts = token_sequence(tokens)
    G = create_language_grammar()
    p_alg = predict_algorithm(G)
    PrintGrammar(G)
    print('LL(1) ? ',is_ll1(G, p_alg))
    Program(ts,p_alg)

