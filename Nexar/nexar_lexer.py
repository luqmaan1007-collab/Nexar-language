import re

TOKEN_SPEC = [
    ('NUMBER',   r'\d+(\.\d+)?'),
    ('STRING',   r'"[^"]*"'),
    ('IDENT',    r'[A-Za-z_][A-Za-z0-9_]*'),
    ('LBRACE',   r'\{'),
    ('RBRACE',   r'\}'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('COLON',    r':'),
    ('COMMA',    r','),
    ('EQ',       r'='),
    ('NEWLINE',  r'\n'),
    ('SKIP',     r'[ \t]+'),
    ('MISMATCH', r'.'),
]

KEYWORDS = {'Screen', 'Button', 'Layout', 'Header', 'Label', 'Icon',
            'if', 'else', 'for', 'var', 'const', 'onClick'}

token_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in TOKEN_SPEC)
get_token = re.compile(token_regex).match

def lex(code):
    pos = 0
    tokens = []
    while pos < len(code):
        m = get_token(code, pos)
        if not m:
            raise SyntaxError(f'Unexpected character: {code[pos]}')
        typ = m.lastgroup
        val = m.group(typ)
        if typ == 'IDENT' and val in KEYWORDS:
            typ = 'KEYWORD'
        elif typ in ['SKIP', 'NEWLINE']:
            pos = m.end()
            continue
        elif typ == 'MISMATCH':
            raise SyntaxError(f'Unexpected token: {val}')
        tokens.append((typ, val))
        pos = m.end()
    return tokens

# Example usage
if __name__ == "__main__":
    code = '''
Screen {
    Button("Play", onClick: startGame)
}
'''
    for t in lex(code):
        print(t)
