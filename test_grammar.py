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

    # Definindo não-terminais
    G.add_nonterminal("programa")
    G.add_nonterminal("declaracoes")
    G.add_nonterminal("declaracao")
    G.add_nonterminal("instrucoes")
    G.add_nonterminal("instrução")
    G.add_nonterminal("atribuição")
    G.add_nonterminal("condicional")
    G.add_nonterminal("repetição")
    G.add_nonterminal("bloco")
    G.add_nonterminal("expressao")
    G.add_nonterminal("termo")
    G.add_nonterminal("fator")
    G.add_nonterminal("expressao_booleana")
    G.add_nonterminal("operador_aritmetico")
    G.add_nonterminal("operador_relacional")
    G.add_nonterminal("expressao_prime")
    
    # Definindo terminais
    G.add_terminal("int")
    G.add_terminal("identificador")
    G.add_terminal("=")
    G.add_terminal("+")
    G.add_terminal("-")
    G.add_terminal("*")
    G.add_terminal("/")
    G.add_terminal("if")
    G.add_terminal("else")
    G.add_terminal("while")
    G.add_terminal("{")
    G.add_terminal("}")
    G.add_terminal("(")
    G.add_terminal(")")
    G.add_terminal("==")
    G.add_terminal("!=")
    G.add_terminal("<")
    G.add_terminal(">")
    G.add_terminal("<=")
    G.add_terminal(">=")
    G.add_terminal("numero")
    G.add_terminal(";")

    # Definindo produções
    G.add_production("programa", ["declaracoes", "instrucoes"])

    G.add_production("declaracoes", ["declaracao", "declaracoes"])
    G.add_production("declaracoes", [])
    G.add_production("declaracao", ["int", "identificador", ";"])

    G.add_production("instrucoes", ["instrução", "instrucoes"])
    G.add_production("instrucoes", [])

    G.add_production("instrução", ["atribuição", ";"])
    G.add_production("instrução", ["condicional"])
    G.add_production("instrução", ["repetição"])
    G.add_production("instrução", ["bloco"])

    G.add_production("atribuição", ["identificador", "=", "expressao", ";"])

    G.add_production("condicional", ["if", "(", "expressao_booleana", ")", "instrução", "else", "instrução"])

    G.add_production("repetição", ["while", "(", "expressao_booleana", ")", "instrução"])

    G.add_production("bloco", ["{", "instrucoes", "}"])

    # Corrigindo a produção da expressão
    G.add_production("expressao", ["termo", "expressao_prime"])

    G.add_production("expressao_prime", ["operador_aritmetico", "termo", "expressao_prime"])
    G.add_production("expressao_prime", [])

    G.add_production("termo", ["identificador"])
    G.add_production("termo", ["numero"])
    G.add_production("termo", ["(", "expressao", ")"])

    G.add_production("expressao_booleana", ["expressao", "operador_relacional", "expressao"])

    # Definindo operadores aritméticos
    G.add_production("operador_aritmetico", ["+"])
    G.add_production("operador_aritmetico", ["-"])
    G.add_production("operador_aritmetico", ["*"])
    G.add_production("operador_aritmetico", ["/"])

    # Definindo operadores relacionais
    G.add_production("operador_relacional", ["=="])
    G.add_production("operador_relacional", ["!="])
    G.add_production("operador_relacional", ["<"])
    G.add_production("operador_relacional", [">"])
    G.add_production("operador_relacional", ["<="])
    G.add_production("operador_relacional", [">="])

    

   

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