from rpal_lexer import lexer

with open("input.rpal", "r") as file:
    data = file.read()

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(f"{tok.type:<12} {tok.value}")
