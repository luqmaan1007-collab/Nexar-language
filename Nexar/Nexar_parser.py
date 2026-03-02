import re

# ------------------- Lexer -------------------
TOKEN_SPEC = [
    ('NUMBER', r'\d+(\.\d+)?'),
    ('STRING', r'"[^"]*"'),
    ('IDENT', r'[A-Za-z_][A-Za-z0-9_]*'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('COLON', r':'),
    ('COMMA', r','),
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),
    ('MISMATCH', r'.'),
]
KEYWORDS = {'Screen', 'Button', 'Layout', 'Header', 'Label', 'Icon', 'onClick'}
token_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in TOKEN_SPEC)
get_token = re.compile(token_regex).match

def lex(code):
    pos = 0
    tokens = []
    while pos < len(code):
        m = get_token(code, pos)
        if not m:
            raise SyntaxError(f"Unexpected char: {code[pos]}")
        typ = m.lastgroup
        val = m.group(typ)
        if typ == 'IDENT' and val in KEYWORDS:
            typ = 'KEYWORD'
        elif typ in ['SKIP', 'NEWLINE']:
            pos = m.end()
            continue
        elif typ == 'MISMATCH':
            raise SyntaxError(f"Unexpected token: {val}")
        tokens.append((typ, val))
        pos = m.end()
    return tokens

# ------------------- AST Nodes -------------------
class ASTNode:
    def __init__(self, node_type, value):
        self.node_type = node_type
        self.value = value
        self.children = []

# ------------------- Parser -------------------
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF','')

    def consume(self):
        t = self.peek()
        self.pos += 1
        return t

    def parseScreen(self):
        self.consume()  # Screen
        name = ASTNode('Screen', 'MainScreen')
        self.consume()  # {
        while self.peek()[0] != 'RBRACE':
            name.children.append(self.parseWidget())
        self.consume()  # }
        return name

    def parseWidget(self):
        t = self.consume()
        node = ASTNode('Widget', t[1])
        if self.peek()[0] == 'LPAREN':
            self.consume()  # (
            while self.peek()[0] != 'RPAREN':
                self.consume()
            self.consume()  # )
        if self.peek()[0] == 'LBRACE':
            self.consume()
            while self.peek()[0] != 'RBRACE':
                self.consume()
            self.consume()
        return node

    def parse(self):
        return self.parseScreen()

# ------------------- Test -------------------
if __name__ == "__main__":
    code = '''
Screen {
    Button("Play", onClick: startGame)
}
'''
    tokens = lex(code)
    parser = Parser(tokens)
    ast = parser.parse()
    print(ast.node_type, ast.value)
    for c in ast.children:
        print(' ', c.node_type, c.value)
