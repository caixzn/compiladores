from grammar import Grammar
from derives_empty_string import derives_empty_string_algorithm
from first_operation import first_algorithm
from follow_operation import follow_algorithm
from ll1_check import is_ll1
from predict import predict_algorithm


def print_grammar(G: Grammar) -> None:
    print(f"Terminais:\n{'\n'.join([x for x in G.terminals()])}")
    print(f"Não-terminais:\n{'\n'.join([X for X in G.nonterminals()])}")
    print(f"Produções:\n{'\n'.join(
        ['id: ' + str(p) + ' ' + str(G.lhs(p)) + '->' + str(G.rhs(p)) for p in G.productions()])}")


if __name__ == "__main__":
    G = Grammar()
    G.grammar("programa")
    G.add_nonterminal("declaracoes")
    G.add_nonterminal("comandos")
    G.add_production("programa", ["declaracoes", "comandos"])
    G.add_terminal("operadorRelacional")
    G.add_terminal("identificador")
    G.add_nonterminal("numero")
    G.add_terminal("numeroInt")
    G.add_terminal("numeroFloat")
    G.add_production("numero", ["numeroInt"])
    G.add_production("numero", ["numeroFloat"])
    G.add_terminal("tipoDeclaracao")
    G.add_terminal("tipo")
    G.add_nonterminal("declaracao")
    G.add_production("declaracao", ["tipoDeclaracao", "identificador", "tipo"])
    G.add_production("declaracoes", ["declaracao", "declaracoes"])
    G.add_production("declaracoes", [])
    G.add_nonterminal("comandos")
    G.add_nonterminal("comando")
    G.add_production("comandos", ["comando", "comandos"])
    G.add_production("comandos", [])
    G.add_nonterminal("atribuicao")
    G.add_production("comando", ["atribuicao"])
    G.add_production("comando", ["while"])
    G.add_production("comando", ["if"])
    G.add_terminal("=")
    G.add_production("atribuicao", ["identificador", "=", "fator"])

    G.add_nonterminal("fator")
    G.add_nonterminal("termo")
    G.add_nonterminal("fatorPrime")
    G.add_nonterminal("termoPrime")
    G.add_nonterminal("expressao")
    G.add_nonterminal("expressaoPrime")
    G.add_terminal("*")
    G.add_terminal("/")
    G.add_terminal("+")
    G.add_terminal("-")
    G.add_terminal("(")
    G.add_terminal(")")

    G.add_production("fator", ["(", "expressao", ")"])
    G.add_production("fator", ["numero"])
    # G.add_production("fator", ["identificador"])

    G.add_production("termo", ["fator", "termoPrime"])
    G.add_production("termoPrime", ["*", "fator", "termoPrime"])
    G.add_production("termoPrime", ["/", "fator", "termoPrime"])
    G.add_production("termoPrime", [])

    G.add_production("expressao", ["termo", "expressaoPrime"])
    G.add_production("expressaoPrime", ["+", "termo", "expressaoPrime"])
    G.add_production("expressaoPrime", ["-", "termo", "expressaoPrime"])
    G.add_production("expressaoPrime", [])
    


    G.add_nonterminal("while")
    G.add_nonterminal("if")
    G.add_nonterminal("condicaoSimples")
    G.add_production("condicaoSimples", ["fator"])
    # G.add_production("condicaoSimples", ["condicaoSimples", "operadorRelacional", "condicaoSimples"])
    # G.add_terminal("and")
    # G.add_terminal("or")
    # G.add_terminal("not")
    # G.add_nonterminal("condicao")
    # G.add_production("condicao", ["condicaoSimples"])
    # G.add_production("condicao", ["not", "condicao"])
    # G.add_production("condicao", ["condicaoSimples", "and", "condicao"])
    # G.add_production("condicao", ["condicaoSimples", "or", "condicao"])
    
    # G.add_nonterminal("else")
    # G.add_production("else", ["else", "comandos"])
    # G.add_production("else", [])
    # G.add_nonterminal("if")
    # G.add_terminal("endif")
    # G.add_production("if", ["if", "condicao", "comandos", "else", "endif"])
    

   

    # print_grammar(G)
    # print("Imprimindo terminais")
    # for x in G.terminals():
    #     print(x)
    # print("Imprimindo não-terminais")
    # for x in G.nonterminals():
    #     print(x)
    # print("Imprimindo produções")
    # for x in G.productions():
    #     print(x)
    # print("Produçoes para A:")
    # for productions in G.productions_for("A"):
    #     print(productions)

    empty_alg = derives_empty_string_algorithm(G)
    empty_alg.run()

    empty_alg = derives_empty_string_algorithm(G)
    empty_alg.run()

    pred_alg = predict_algorithm(G)
    ll1 = is_ll1(G, pred_alg)
    if ll1:
        print("É LL(1)")
    else:
        print("Não é LL(1)")
