"""
Lexical Analyzer for RPAL Language
Tokenizes RPAL source code according to lexical rules.
"""

import re # Importing Python's built-in regular expressions module for pattern matching
from enum import Enum                       # Importing Enum class to define token types in a structured way

class TokenType(Enum):
    """Enum representing different token types in RPAL."""
    KEYWORD = 1   # Reserved words like let, in, fn, etc.
    IDENTIFIER = 2 # Variable names or function names
    INTEGER = 3 # Numeric literals
    STRING = 4  # Strings wrapped in single quotes
    END_OF_TOKENS = 5 # Marks the end of the token stream (not actively used here)
    PUNCTUATION = 6 # Symbols like ; , ( )
    OPERATOR = 7 # Operators like + - * = etc.

class Token:
    """Class representing a token in RPAL."""
    def __init__(self, token_type, value):
        # Ensure token_type is a valid TokenType enum
        if not isinstance(token_type, TokenType):
            raise ValueError("token_type must be an instance of TokenType enum")
        self.type = token_type  # Store token type (like KEYWORD, INTEGER, etc.)
        self.value = value  # Store the actual matched text (e.g., "let", "42")

    def get_type(self):
        """Get the token type."""
        return self.type

    def get_value(self):
        """Get the token value."""
        return self.value
    
    def __str__(self):
        """String representation of the token."""
        return f"<{self.type.name}, '{self.value}'>"    # e.g., <KEYWORD, 'let'>

def tokenize(input_str):
    """
    Tokenize the input string according to RPAL lexical rules.
    
    Args:
        input_str (str): The input RPAL program as a string
        
    Returns:
        list: A list of Token objects
    """
    tokens = []  # This will hold the final list of tokens
    token_patterns = {
        'COMMENT': r'//.*',    # Single-line comments starting with //
        'KEYWORD': r'(let|in|fn|where|aug|or|not|gr|ge|ls|le|eq|ne|true|false|nil|dummy|within|and|rec)\b',
        'STRING': r'\'(?:\\\'|[^\'])*\'',   # String literals with escaped single quotes
        'IDENTIFIER': r'[a-zA-Z][a-zA-Z0-9_]*',  # Variable/function names (letters, digits, underscore)
        'INTEGER': r'\d+', # Integer values (only positive numbers supported here)
        'OPERATOR': r'[+\-*<>&.@/:=~|$\#!%^_\[\]{}"\'?]+',  
        'SPACES': r'[ \t\n]+',  # Whitespace (to be ignored)
        'PUNCTUATION': r'[();,]'   # Punctuation characters
    }
    
    # Process the input string until it's empty
    while input_str:
        matched = False   # Track if any pattern matched in this iteration
        for key, pattern in token_patterns.items():
            match = re.match(pattern, input_str)  # Try to match from the start of the input
            if match:
                # Ignore spaces and comments, don't add them as tokens
                if key != 'SPACES' and key != 'COMMENT':
                    token_type = getattr(TokenType, key)  # Convert pattern key to enum type
                    tokens.append(Token(token_type, match.group(0)))  # Create a token and add to the list
                input_str = input_str[match.end():] # Remove matched part from input string

                matched = True  # Break since we found a match and processed it
                break
        
        if not matched:
            raise ValueError(f"Unable to tokenize: '{input_str[:20]}...'")   # Show first 20 characters for debugging
    
    return tokens
