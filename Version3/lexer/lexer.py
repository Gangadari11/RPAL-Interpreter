"""
Lexical Analyzer for RPAL Language
Tokenizes RPAL source code according to lexical rules.
"""

import re
from utils.token_types import TokenType, Token

def tokenize(input_str):
    """
    Tokenize the input string according to RPAL lexical rules.
    
    Args:
        input_str (str): The input RPAL program as a string
        
    Returns:
        list: A list of Token objects
    """
    tokens = []
    token_patterns = {
        'COMMENT': r'//.*',
        'KEYWORD': r'(let|in|fn|where|aug|or|not|gr|ge|ls|le|eq|ne|true|false|nil|dummy|within|and|rec)\b',
        'STRING': r'\'(?:\\\'|[^\'])*\'',
        'IDENTIFIER': r'[a-zA-Z][a-zA-Z0-9_]*',
        'INTEGER': r'\d+',
        'OPERATOR': r'[+\-*<>&.@/:=~|$\#!%^_\[\]{}"\'?]+',
        'SPACES': r'[ \t\n]+',
        'PUNCTUATION': r'[();,]'
    }
    
    # Process the input string until it's empty
    while input_str:
        matched = False
        for key, pattern in token_patterns.items():
            match = re.match(pattern, input_str)
            if match:
                if key != 'SPACES' and key != 'COMMENT':
                    token_type = getattr(TokenType, key)
                    tokens.append(Token(token_type, match.group(0)))
                input_str = input_str[match.end():]
                matched = True
                break
        
        if not matched:
            raise ValueError(f"Unable to tokenize: '{input_str[:20]}...'")
    
    return tokens