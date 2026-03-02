import re

# ------------------- Token -------------------
TOKEN_SPEC = [
    ('NUMBER', r'\d+(\.\d+)?'),
    ('STRING', r'"[^"]*"'),
    ('IDENT', r'[A-Za-z_][A-Za-z0-9_]*'),
    ('LBRACE', r'\{'), ('RBRACE', r'\}'),
    ('LPAREN', r'\('), ('RPAREN', r'\)'),
    ('COLON', r':'), ('COMMA', r','), ('SEMICOLON', r';'),
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),
    ('MISMATCH', r'.'),
]
KEYWORDS = {'Screen','Button','Layout','Header','Label','Icon','onClick'}
token_regex = '|'.join(f'(?P<{n}>{r})' for n,r in TOKEN_SPEC)
get_token = re.compile(token_regex).match

def lex(code):
    pos = 0; tokens=[]
    while pos<len(code):
        m = get_token(code,pos)
        if not m: raise SyntaxError(f"Unexpected char: {code[pos]}")
        typ,val = m.lastgroup,m.group(m.lastgroup)
        if typ=='IDENT' and val in KEYWORDS: typ='KEYWORD'
        elif typ in ['SKIP','NEWLINE']: pos=m.end(); continue
        elif typ=='MISMATCH': raise SyntaxError(f"Unexpected token: {val}")
        tokens.append((typ,val))
        pos=m.end()
    return tokens

# ------------------- AST -------------------
class ASTNode:
    def __init__(self,node_type,value): self.node_type=node_type; self.value=value; self.children=[]
    def add_child(self,child): self.children.append(child)
    def print(self,indent=0):
        print("  "*indent+f"{self.node_type}: {self.value}")
        for c in self.children: c.print(indent+1)

# ------------------- Parser -------------------
class Parser:
    def __init__(self,tokens): self.tokens=tokens; self.pos=0
    def peek(self): return self.tokens[self.pos] if self.pos<len(self.tokens) else ('EOF','')
    def consume(self): t=self.peek(); self.pos+=1; return t

    def parseWidget(self):
        t = self.consume()
        node = ASTNode('Widget', t[1])
        if self.peek()[0]=='LPAREN':
            self.consume()
            while self.peek()[0]!='RPAREN': self.consume()
            self.consume()
        if self.peek()[0]=='LBRACE':
            self.consume()
            while self.peek()[0]!='RBRACE': self.consume()
            self.consume()
        return node

    def parseScreen(self):
        self.consume() # Screen
        node=ASTNode('Screen','MainScreen')
        self.consume() # {
        while self.peek()[0]!='RBRACE': node.add_child(self.parseWidget())
        self.consume() # }
        return node

    def parse(self): return self.parseScreen()

# ------------------- Example -------------------
if __name__=="__main__":
    code = '''
Screen {
    Button("Play", onClick: startGame)
    Layout {
        Icon("coin")
        Label("100")
    }
}
'''
    tokens=lex(code)
    parser=Parser(tokens)
    ast=parser.parse()
    ast.print()
