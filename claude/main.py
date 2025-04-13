from rpal_lexer import RPALLexer

def main():
    with open('input.rpal', 'r') as file:
        input_text = file.read()

    lexer = RPALLexer()
    tokens = lexer.tokenize(input_text)

    for token in tokens:
        print(token)

if __name__ == "__main__":
    main()
