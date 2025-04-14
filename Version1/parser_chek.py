import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lexer import tokenize_rpal
from parser import RPALParser  # adjust to your parser class/module


def main():
    try:
        with open("input.txt", "r") as file:
            source_code = file.read()
    except FileNotFoundError:
        print("Error: input.txt not found.")
        sys.exit(1)

    try:
        tokens = tokenize_rpal(source_code)
        parser = RPALParser(tokens)  # assuming parser class takes token list
        ast_root = parser.parse()    # assuming this returns the root of the AST

        print("AST Representation:")
        print("===================")
        print_ast(ast_root)

    except Exception as e:
        print(f"Error while parsing: {e}")

# A recursive AST printer (customize this to match your AST class structure)
def print_ast(node, indent=0):
    if node is None:
        return

    print(" " * indent + str(node))

    if hasattr(node, "children"):  # assuming nodes have a children list
        for child in node.children:
            print_ast(child, indent + 2)

if __name__ == "__main__":
    main()
