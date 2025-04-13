import ply.lex as lex

# Reserved keywords in RPAL
reserved = {
    'let': 'KEYWORD',
    'in': 'KEYWORD',
    'fn': 'KEYWORD',
    'where': 'KEYWORD',
    'rec': 'KEYWORD',
    'within': 'KEYWORD',
    'and': 'KEYWORD',
    'or': 'KEYWORD',
    'gr': 'KEYWORD',
    'ge': 'KEYWORD',
    'ls': 'KEYWORD',
    'le': 'KEYWORD',
    'nil': 'KEYWORD',
    'true': 'KEYWORD',
    'false': 'KEYWORD',
    'not': 'KEYWORD',
    'aug': 'KEYWORD',
    'isnil': 'KEYWORD',
    'neg': 'KEYWORD',
    'Stem': 'KEYWORD',
    'Stern': 'KEYWORD',
    'Order': 'KEYWORD',
    'Print': 'KEYWORD',
    'Conc': 'KEYWORD',
    'eq': 'KEYWORD',
    'ne': 'KEYWORD'
}

# List of token names
tokens = [
    'IDENTIFIER',
    'INTEGER',
    'STRING',
    'OPERATOR',
    'LPAREN', 'RPAREN',
    'COMMA', 'SEMICOLON'
] + list(set(reserved.values()))

# Operators (handled as a combined token)
operator_symbols = {
    '->', '**', '>=', '<=', '==', '/=', '><', '||', '::', ':=', 
    '+', '-', '*', '/', '<', '>', '&', '.', '@', '|', ':', '~', '=', 
    '!', '#', '%', '^', '[', ']', '{', '}', '"', '?'
}

# Regex-based token rules
t_STRING = r"\'([^\\\n]|(\\.))*?\'"
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_SEMICOLON = r';'

# Ignored characters (spaces and tabs)
t_ignore = ' \t\r'

# Ignore comments (from // to end of line)
def t_COMMENT(t):
    r'//.*'
    pass

# Handle newlines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Integer (digits only)
def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Identifiers or keywords
def t_IDENTIFIER(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

# Operators
def t_OPERATOR(t):
    r'(\->|\*\*|>=|<=|==|/=|><|\|\||::|:=|[+\-*/<>&.@|:~=!#%^{}\[\]"\?])'
    if t.value not in operator_symbols:
        print(f"Unknown operator: {t.value}")
    return t

# Error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}' on line {t.lineno}")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

