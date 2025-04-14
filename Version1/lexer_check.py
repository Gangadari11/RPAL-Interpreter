from Parser.lexer import tokenize_rpal, RPALTokenType

def main():
    try:
        with open("input.txt", "r") as file:
            source_code = file.read()
    except FileNotFoundError:
        print("Error: input.txt not found.")
        return

    try:
        tokens = tokenize_rpal(source_code)

        print("Lexer Check Results:")
        print("====================")
        for token in tokens:
            if token.token_type != RPALTokenType.EOF:
                print(f"{token.token_type.name:<10} | {token.value:<20} | Line {token.line}, Pos {token.position}")
    
    except Exception as e:
        print(f"Error while lexing: {e}")

if __name__ == "__main__":
    main()
