import re

class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f'Token({self.tipo}, {self.valor})'

class Lexer:
    def __init__(self, texto):
        self.texto = texto
        self.pos = 0
        self.caractere_atual = self.texto[self.pos] if self.texto else None

        self.regras = [
            (r'[ \t\n]+', None),  # Ignorar espaços em branco
            (r'int', 'INT'),
            (r'if', 'IF'),
            (r'else', 'ELSE'),
            (r'while', 'WHILE'),
            (r'\{', 'LBRACE'),
            (r'\}', 'RBRACE'),
            (r'\(', 'LPAREN'),
            (r'\)', 'RPAREN'),
            (r';', 'SEMI'),
            (r'==', 'EQ'),
            (r'!=', 'NEQ'),
            (r'<', 'LT'),
            (r'>', 'GT'),
            (r'<=', 'LE'),
            (r'>=', 'GE'),
            (r'=', 'ASSIGN'),
            (r'\+', 'PLUS'),
            (r'-', 'MINUS'),
            (r'\*', 'MULT'),
            (r'/', 'DIV'),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', 'IDENTIFICADOR'),
            (r'\d+', 'NUMERO'),
        ]

    def error(self):
        raise Exception('Erro de análise: caractere inesperado')

    def avancar(self):
        self.pos += 1
        if self.pos > len(self.texto) - 1:
            self.caractere_atual = None
        else:
            self.caractere_atual = self.texto[self.pos]

    def obter_token(self):
        while self.caractere_atual is not None:
            for regex, tipo in self.regras:
                match = re.match(regex, self.texto[self.pos:])
                if match:
                    valor = match.group(0)
                    if tipo:
                        token = Token(tipo, valor)
                        self.pos += len(valor)
                        self.caractere_atual = self.texto[self.pos] if self.pos < len(self.texto) else None
                        return token
                    else:
                        self.pos += len(valor)
                        self.caractere_atual = self.texto[self.pos] if self.pos < len(self.texto) else None
                        break
            else:
                self.error()
        return Token('EOF', None)

class ASTNode:
    pass

class AssignNode(ASTNode):
    def __init__(self, identificador, valor):
        self.identificador = identificador
        self.valor = valor

    def __repr__(self):
        return f"AssignNode({self.identificador}, {self.valor})"

class NumNode(ASTNode):
    def __init__(self, valor):
        self.valor = valor

    def __repr__(self):
        return f"NumNode({self.valor})"

class IdentNode(ASTNode):
    def __init__(self, identificador):
        self.identificador = identificador

    def __repr__(self):
        return f"IdentNode({self.identificador})"

class BinOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOpNode({self.left}, {self.op}, {self.right})"

class WhileNode(ASTNode):
    def __init__(self, condicao, corpo):
        self.condicao = condicao
        self.corpo = corpo

    def __repr__(self):
        return f"WhileNode({self.condicao}, {self.corpo})"

class IfNode(ASTNode):
    def __init__(self, condicao, corpo, else_corpo=None):
        self.condicao = condicao
        self.corpo = corpo
        self.else_corpo = else_corpo

    def __repr__(self):
        return f"IfNode({self.condicao}, {self.corpo}, {self.else_corpo})"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.token_atual = self.tokens[self.pos] if self.tokens else None

    def error(self):
        raise Exception('Erro de análise: token inesperado')

    def avancar(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.token_atual = self.tokens[self.pos]
        else:
            self.token_atual = None

    def parse(self):
        nodes = []
        while self.token_atual is not None:
            if self.token_atual.tipo == 'IDENTIFICADOR':
                ident = self.token_atual
                self.avancar()  # Move para o próximo token
                if self.token_atual.tipo == 'ASSIGN':
                    self.avancar()  # Move para o valor
                    valor_node = self.expr()
                    nodes.append(AssignNode(ident.valor, valor_node))
                    if self.token_atual.tipo == 'SEMI':
                        self.avancar()  # Move para o próximo token
                    else:
                        self.error()
            elif self.token_atual.tipo == 'WHILE':
                self.avancar()  # Move para '('
                condicao = self.expr()
                if self.token_atual.tipo == 'RPAREN':
                    self.avancar()  # Move para '{'
                    if self.token_atual.tipo == 'LBRACE':
                        self.avancar()  # Move para '{'
                        corpo = []
                        while self.token_atual.tipo != 'RBRACE':
                            corpo.append(self.parse())
                        self.avancar()  # Move para '}'
                        nodes.append(WhileNode(condicao, corpo))
                    else:
                        self.error()
                else:
                    self.error()
            elif self.token_atual.tipo == 'IF':
                self.avancar()  # Move para '('
                condicao = self.expr()
                if self.token_atual.tipo == 'RPAREN':
                    self.avancar()  # Move para '{'
                    if self.token_atual.tipo == 'LBRACE':
                        self.avancar()  # Move para '{'
                        corpo = []
                        while self.token_atual.tipo != 'RBRACE':
                            corpo.append(self.parse())
                        self.avancar()  # Move para '}'
                        else_corpo = None
                        if self.token_atual.tipo == 'ELSE':
                            self.avancar()  # Move para '{'
                            if self.token_atual.tipo == 'LBRACE':
                                self.avancar()  # Move para '{'
                                else_corpo = []
                                while self.token_atual.tipo != 'RBRACE':
                                    else_corpo.append(self.parse())
                                self.avancar()  # Move para '}'
                        nodes.append(IfNode(condicao, corpo, else_corpo))
                    else:
                        self.error()
                else:
                    self.error()
            else:
                self.avancar()
        return nodes

    def expr(self):
        node = self.term()
        while self.token_atual and self.token_atual.tipo in ('PLUS', 'MINUS'):
            op = self.token_atual
            self.avancar()  # Move para o próximo token
            right = self.term()
            node = BinOpNode(node, op, right)
        return node

    def term(self):
        node = self.factor()
        while self.token_atual and self.token_atual.tipo in ('MULT', 'DIV'):
            op = self.token_atual
            self.avancar()  # Move para o próximo token
            right = self.factor()
            node = BinOpNode(node, op, right)
        return node

    def factor(self):
        if self.token_atual.tipo == 'NUMERO':
            valor = self.token_atual
            self.avancar()
            return NumNode(valor.valor)
        elif self.token_atual.tipo == 'IDENTIFICADOR':
            ident = self.token_atual
            self.avancar()
            return IdentNode(ident.valor)
        elif self.token_atual.tipo == 'LPAREN':
            self.avancar()
            node = self.expr()
            if self.token_atual.tipo == 'RPAREN':
                self.avancar()
                return node
            else:
                self.error()
        else:
            self.error()

class Interpreter:
    def __init__(self):
        self.variables = {}

    def visit(self, node):
        if isinstance(node, AssignNode):
            self.variables[node.identificador] = self.visit(node.valor)
        elif isinstance(node, NumNode):
            return int(node.valor)
        elif isinstance(node, IdentNode):
            return self.variables.get(node.identificador, 0)
        elif isinstance(node, BinOpNode):
            left = self.visit(node.left)
            right = self.visit(node.right)
            if node.op.tipo == 'PLUS':
                return left + right
            elif node.op.tipo == 'MINUS':
                return left - right
            elif node.op.tipo == 'MULT':
                return left * right
            elif node.op.tipo == 'DIV':
                return left // right
        elif isinstance(node, WhileNode):
            while self.visit(node.condicao):
                for n in node.corpo:
                    self.visit(n)
        elif isinstance(node, IfNode):
            if self.visit(node.condicao):
                for n in node.corpo:
                    self.visit(n)
            elif node.else_corpo:
                for n in node.else_corpo:
                    self.visit(n)
        else:
            raise Exception("Tipo de nó desconhecido")

    def interpret(self, ast):
        for node in ast:
            self.visit(node)

class CodeGenerator:
    def __init__(self):
        self.codigo = []

    def gerar(self, ast):
        for node in ast:
            self.visit(node)
        return "\n".join(self.codigo)

    def visit(self, node):
        if isinstance(node, AssignNode):
            self.visit_assign(node)
        elif isinstance(node, NumNode):
            return self.visit_num(node)
        elif isinstance(node, IdentNode):
            return self.visit_ident(node)
        elif isinstance(node, BinOpNode):
            return self.visit_binop(node)
        elif isinstance(node, WhileNode):
            self.visit_while(node)
        elif isinstance(node, IfNode):
            self.visit_if(node)

    def visit_assign(self, node):
        valor = self.visit(node.valor)
        self.codigo.append(f"STORE {node.identificador}")  # Armazenar o valor na variável

    def visit_num(self, node):
        return node.valor  # Retornar o valor numérico

    def visit_ident(self, node):
        return node.identificador  # Retornar o identificador

    def visit_binop(self, node):
        left = self.visit(node.left)  # Visitar o lado esquerdo
        right = self.visit(node.right)  # Visitar o lado direito
        self.codigo.append(f"LOAD {left}")  # Carregar o valor da esquerda

        if node.op.tipo == 'PLUS':
            self.codigo.append(f"ADD {right}")
        elif node.op.tipo == 'MINUS':
            self.codigo.append(f"SUB {right}")
        elif node.op.tipo == 'MULT':
            self.codigo.append(f"MUL {right}")
        elif node.op.tipo == 'DIV':
            self.codigo.append(f"DIV {right}")

        return "RESULT"  # Retornar um marcador que representa o resultado da operação

    def visit_while(self, node):
        start_label = f"WHILE_START_{id(node)}"
        end_label = f"WHILE_END_{id(node)}"
        self.codigo.append(f"{start_label}:")
        cond = self.visit(node.condicao)
        self.codigo.append(f"LOAD {cond}")
        self.codigo.append(f"JZ {end_label}")  # Pular se a condição for zero

        for stmt in node.corpo:
            self.visit(stmt)

        self.codigo.append(f"JMP {start_label}")  # Voltar ao início do loop
        self.codigo.append(f"{end_label}:")

    def visit_if(self, node):
        start_label = f"IF_START_{id(node)}"
        end_label = f"IF_END_{id(node)}"
        self.codigo.append(f"{start_label}:")
        cond = self.visit(node.condicao)
        self.codigo.append(f"LOAD {cond}")
        self.codigo.append(f"JZ {end_label}")  # Pular para o final se a condição for falsa

        for stmt in node.corpo:
            self.visit(stmt)

        if node.else_corpo:
            self.codigo.append(f"JMP {end_label}")

        self.codigo.append(f"{end_label}:")
        if node.else_corpo:
            for stmt in node.else_corpo:
                self.visit(stmt)

# Exemplo de uso
if __name__ == "__main__":
    texto = """
    int a = 11 * 4;
    if (a > 20) {
        int b = a - 5;
    } else {
        int c = a + 5;
    }
    """

    lexer = Lexer(texto)
    tokens = []
    token = lexer.obter_token()
    while token.tipo != 'EOF':
        tokens.append(token)
        token = lexer.obter_token()

    parser = Parser(tokens)
    ast = parser.parse()

    codegen = CodeGenerator()
    codigo_asm = codegen.gerar(ast)

    print(codigo_asm)  # Imprime o código Assembly gerado
