# # check_ast.py

# from lexer import RPALLexer, tokenize_rpal
# from parser import RPALParser
# import sys

# def read_file(file_path):
#     with open(file_path, 'r') as f:
#         return f.read()

# def check_ast(file_path):
#     # Step 1: Read input RPAL code
#     source_code = read_file(file_path)

#     # Step 2: Tokenize using your lexer
#     tokens = tokenize_rpal(source_code)

#     # Step 3: Parse tokens into AST
#     parser = RPALParser(tokens)
#     ast = parser.parse()
    
#     # Step 4: Convert AST to string representation
#     ast_lines = parser.print_ast()


#     # Step 5: Print the AST
#     print("\n".join(ast_lines))

#     # (Optional) Step 6: Compare to expected output
#     expected_path = file_path.replace(".rpal", ".ast")
#     try:
#         with open(expected_path, 'r') as f:
#             expected = [line.strip() for line in f.readlines()]
#         actual = [line.strip() for line in ast_lines]

#         if expected == actual:
#             print("\n✅ AST matches expected output.")
#         else:
#             print("\n❌ AST does not match expected output.")
#             print("\nExpected:")
#             print("\n".join(expected))
#             print("\nActual:")
#             print("\n".join(actual))
#     except FileNotFoundError:
#         print("\n⚠️ Expected AST file not found. Skipping comparison.")

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Usage: python check_ast.py <filename.rpal>")
#         sys.exit(1)
    
#     check_ast(sys.argv[1])



#!/usr/bin/env python3
# check_ast.py - Utility to check RPAL parser by printing AST tree

from lexer import tokenize_rpal, RPALToken, RPALTokenType
from parser import RPALParser, NodeType, ASTNode

def check_ast(filename="input.txt"):
    """
    Read an RPAL program from a file, parse it, and print the AST tree
    
    Args:
        filename: Path to the file containing RPAL code
    """
    try:
        # Read the source code from file
        with open(filename, "r") as file:
            source_code = file.read()
        
        print(f"Input RPAL program:\n{'-'*20}")
        print(source_code)
        print(f"{'-'*20}\n")
        
        # Tokenize the source code
        print("Tokenizing...")
        tokens = tokenize_rpal(source_code)
        
        # Print token information
        print(f"Found {len(tokens)} tokens:")
        for i, token in enumerate(tokens[:20]):  # Print first 20 tokens only
            if token.token_type != RPALTokenType.EOF:
                print(f"{i}: {token.token_type.name:<10} | '{token.value}'")
        
        if len(tokens) > 20:
            print(f"... and {len(tokens) - 20} more tokens")
        print()
        
        # Parse the tokens and build the AST
        print("Parsing and building AST...")
        parser = RPALParser(tokens)
        ast = parser.parse()
        
        if ast is None:
            print("Failed to parse the program.")
            return
        
        # Convert AST to string representation
        print("AST Tree:")
        print(f"{'-'*20}")
        ast_strings = parser.convert_ast_to_string()
        for line in ast_strings:
            print(line)
        print(f"{'-'*20}")
        
        print("\nAST construction successful!")
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_ast()