#!/usr/bin/env python3
"""
RPAL Language Interpreter
CS 3513 - Programming Languages Project 01
Authors - Gangadari M.D.S (220178X ) , Jayawardana W.S.S (220282K)
This program implements a lexical analyzer, parser, and CSE machine for the RPAL language.
"""

import argparse
import sys
from lexer.lexer import tokenize
from parser.parser import Parser
from ast.ast_printer import ASTFactory
from cse_machine.cse_machine import CSEMachineFactory

def main():
    """Main entry point for the RPAL interpreter."""
    parser = argparse.ArgumentParser(description='RPAL Language Interpreter')
    parser.add_argument('file_name', type=str, help='The RPAL program input file')
    parser.add_argument('-ast', action='store_true', help='Print the abstract syntax tree')
    parser.add_argument('-st', action='store_true', help='Print the standardized tree')
    
    args = parser.parse_args()

    try:
        # Read input file
        with open(args.file_name, "r") as input_file:
            input_text = input_file.read()
        
        # Tokenize the input text
        tokens = tokenize(input_text)
        
        # Parse tokens into AST
        parser = Parser(tokens)
        ast_nodes = parser.parse()
        if ast_nodes is None:
            sys.exit(1)
        
        # Convert to string representation
        string_ast = parser.convert_ast_to_string_ast()
        
        # If -ast flag is provided, print the AST and exit
        if args.ast:
            for string in string_ast:
                print(string)
            return
        
        # Create and standardize the AST
        ast_factory = ASTFactory()
        ast = ast_factory.get_abstract_syntax_tree(string_ast)
        ast.standardize()
        
        # If -st flag is provided, print the standardized tree and exit
        if args.st:
            ast.print_ast()
            return
        
        # Create and execute the CSE machine
        cse_machine_factory = CSEMachineFactory()
        cse_machine = cse_machine_factory.get_cse_machine(ast)
        
        # Print the final output
        result = cse_machine.get_answer()
        print(result)
        
    except FileNotFoundError:
        print(f"Error: File '{args.file_name}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()