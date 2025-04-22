"""
Token types for RPAL Language
Defines the token types used in the lexical analyzer.
"""

from enum import Enum

class TokenType(Enum):
    """Enum representing different token types in RPAL."""
    KEYWORD = 1
    IDENTIFIER = 2
    INTEGER = 3
    STRING = 4
    END_OF_TOKENS = 5
    PUNCTUATION = 6
    OPERATOR = 7

class Token:
    """Class representing a token in RPAL."""
    def __init__(self, token_type, value):
        if not isinstance(token_type, TokenType):
            raise ValueError("token_type must be an instance of TokenType enum")
        self.type = token_type
        self.value = value

    def get_type(self):
        """Get the token type."""
        return self.type

    def get_value(self):
        """Get the token value."""
        return self.value
    
    def __str__(self):
        """String representation of the token."""
        return f"<{self.type.name}, '{self.value}'>"