# check_lexer.py

import sys  # Needed to access command-line arguments
from lexical_analyzer import tokenize   # Importing the tokenize function from your lexical analyzer

def main():
    # Check that exactly one command-line argument (input file path) is provided
    if len(sys.argv) != 2:
        print("Usage: python check_lexer.py <path_to_input_file>") # Print usage help
        return

    input_path = sys.argv[1] # sys.argv[0] is the script name, sys.argv[1] is the path you pass

    try:
        with open(input_path, "r") as file:  # Open file in read mode
            input_str = file.read() # Read entire file content into a string

        tokens = tokenize(input_str)  # Call the lexical analyzer

        print("Tokens:")
        for token in tokens: # Iterate through the list of tokens
            print(token) 

    except FileNotFoundError: 
        print(f"Error: File not found at {input_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__": # This ensures that main() is called only when the script is run directly, not when imported
    main() # Call the main function
