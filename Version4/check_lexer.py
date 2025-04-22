import sys
from lexer.lexer import tokenize
from utils.token_types import TokenType, Token

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_lexer.py input.txt")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        code = f.read()
    
    tokens = tokenize(code)
    
    for token in tokens:
        print(f"{token.type.name}: {token.value}")
