"""
Lexical Analyzer for RPAL Language
Tokenizes RPAL source code according to lexical rules.

This module takes in RPAL source code and returns a list of tokens,
which are the smallest meaningful units in the language, such as keywords,
identifiers, numbers, operators, punctuation, etc.
"""

import re   # Regular expressions for pattern matching
from utils.token_types import TokenType, Token # TokenType enum and Token dataclass are defined externally

def tokenize(input_str):
    """
    Tokenize the input string according to RPAL lexical rules.
    
    Args:
        input_str (str): The input RPAL program as a string
        
    Returns:
        list: A list of Token objects
    """
    tokens = []  # This will store all the tokens we extract from the input string

    # Dictionary mapping token types to their regex patterns
    token_patterns = {
        'COMMENT': r'//.*',   # Line comments start with // and go until the end of the line
        'KEYWORD': r'(let|in|fn|where|aug|or|not|gr|ge|ls|le|eq|ne|true|false|nil|dummy|within|and|rec)\b',   # Reserved keywords of the RPAL language
        'STRING': r'\'(?:\\\'|[^\'])*\'', # String literals enclosed in single quotes, can contain escaped quotes (e.g., \')
        'IDENTIFIER': r'[a-zA-Z][a-zA-Z0-9_]*',  # Identifiers: must start with a letter and can include letters, digits, and underscores
        'INTEGER': r'\d+', # Integers: sequences of digits
        'OPERATOR': r'[+\-*<>&.@/:=~|$\#!%^_\[\]{}"\'?]+', 
        'SPACES': r'[ \t\n]+',  # Whitespace characters: spaces, tabs, and newlines (ignored by the lexer)
        'PUNCTUATION': r'[();,]'  # Punctuation characters: parentheses, semicolons, commas
    }
    
    # Process the input string until it's empty
    while input_str:
        matched = False  # Flag to track whether a valid token was matched in this iteration

         # Try each token pattern in the order they appear
        for key, pattern in token_patterns.items():
            match = re.match(pattern, input_str)  # Match the pattern at the beginning of the string
            if match:
                if key != 'SPACES' and key != 'COMMENT':   # Skip adding whitespace and comments to the token list
                    token_type = getattr(TokenType, key)  # Get the corresponding token type from the TokenType enum
                    tokens.append(Token(token_type, match.group(0))) # Create a new Token and add it to the list
                input_str = input_str[match.end():]  # Remove the matched portion from the input string
                matched = True # Mark that a token was successfully matched
                break # Exit the loop and restart the outer loop with updated input
        
        if not matched:   # If no pattern matched the current beginning of the input string, raise an error
            raise ValueError(f"Unable to tokenize: '{input_str[:20]}...'")
    
    return tokens # Return the complete list of Token objects