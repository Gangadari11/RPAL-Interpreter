
## This is a simple script to check the lexer functionality by '
# reading an input file and printing the tokens generated by the lexer.
# It expects the input file to be passed as a command line argument.
# If the file is not provided, it will print usage instructions and exit.
# If the file is provided, it will read the content, tokenize it, and print each token's type and value.


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
