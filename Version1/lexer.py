# Import necessary libraries
import re
from enum import Enum, auto
from typing import List, Optional

# Define token types as an Enum for better type safety and readability
class RPALTokenType(Enum):
    # Define all possible token types for RPAL language
    IDENTIFIER = auto()  # Variables and function names
    INTEGER = auto()     # Numeric literals
    STRING = auto()      # String literals enclosed in quotes
    OPERATOR = auto()    # Symbols like +, -, *, etc.
    KEYWORD = auto()     # Reserved words like let, in, where
    LPAREN = auto()      # Left parenthesis (
    RPAREN = auto()      # Right parenthesis )
    COMMA = auto()       # Comma ,
    SEMICOLON = auto()   # Semicolon ;
    PERIOD = auto()      # Period .
    EOF = auto()         # End of file marker

# Define a Token class to represent individual tokens
class RPALToken:
    def __init__(self, token_type: RPALTokenType, value: str, line: int = 0, position: int = 0):
        """
        Initialize a new token with type, value, and position information
        
        Args:
            token_type: The type of this token from RPALTokenType enum
            value: The string value of this token
            line: Line number where this token was found
            position: Character position where this token was found
        """
        self.token_type = token_type
        self.value = value
        self.line = line
        self.position = position
    
    def __str__(self):
        """Return a string representation of the token for debugging"""
        return f"Token({self.token_type}, '{self.value}', line={self.line}, pos={self.position})"
    
    def __repr__(self):
        """Return a formal representation of the token"""
        return self.__str__()

# Define the Lexer class to break source code into tokens
class RPALLexer:
    def __init__(self, source_code: str):
        """
        Initialize the lexer with source code to tokenize
        
        Args:
            source_code: The RPAL source code as a string
        """
        self.source = source_code
        self.current_position = 0
        self.current_line = 1
        self.current_line_position = 0
        self.tokens = []
        
        # Define RPAL keywords
        self.keywords = {
            "let": RPALTokenType.KEYWORD,
            "in": RPALTokenType.KEYWORD,
            "where": RPALTokenType.KEYWORD,
            "rec": RPALTokenType.KEYWORD,
            "fn": RPALTokenType.KEYWORD,
            "aug": RPALTokenType.KEYWORD,
            "or": RPALTokenType.KEYWORD,
            "and": RPALTokenType.KEYWORD,
            "not": RPALTokenType.KEYWORD,
            "gr": RPALTokenType.KEYWORD,
            "ge": RPALTokenType.KEYWORD,
            "ls": RPALTokenType.KEYWORD,
            "le": RPALTokenType.KEYWORD,
            "eq": RPALTokenType.KEYWORD,
            "ne": RPALTokenType.KEYWORD,
            "true": RPALTokenType.KEYWORD,
            "false": RPALTokenType.KEYWORD,
            "nil": RPALTokenType.KEYWORD,
            "dummy": RPALTokenType.KEYWORD,
            "within": RPALTokenType.KEYWORD,
            "print": RPALTokenType.KEYWORD,
            "tau": RPALTokenType.KEYWORD,
        }
        
        # Define punctuation tokens
        self.punctuation = {
            "(": RPALTokenType.LPAREN,
            ")": RPALTokenType.RPAREN,
            ",": RPALTokenType.COMMA,
            ";": RPALTokenType.SEMICOLON,
            ".": RPALTokenType.PERIOD,
        }
        
        # Define regex patterns for token recognition
        self.patterns = {
            # Based on RPAL lexicon definitions
            'identifier': r'[A-Za-z](?:[A-Za-z0-9_])*',
            'integer': r'[0-9]+',
            'operator': r'[+\-*/<>=&@$#%^!|~?:]+',
            'string': r'\'(?:[^\'\\]|\\.)*\'',
            'whitespace': r'[ \t\r\n]+',
            'comment': r'//[^\n]*'
        }
        
        # Compile regex patterns for better performance
        self.regex = {
            name: re.compile(pattern) for name, pattern in self.patterns.items()
        }
    
    def is_at_end(self) -> bool:
        """Check if we've reached the end of the source code"""
        return self.current_position >= len(self.source)
    
    def advance(self, count: int = 1) -> None:
        """
        Move the current position pointer forward
        
        Args:
            count: Number of characters to advance
        """
        for _ in range(count):
            if self.current_position < len(self.source):
                if self.source[self.current_position] == '\n':
                    self.current_line += 1
                    self.current_line_position = 0
                else:
                    self.current_line_position += 1
                self.current_position += 1
    
    def peek(self) -> Optional[str]:
        """Return the current character without advancing"""
        if self.is_at_end():
            return None
        return self.source[self.current_position]
    
    def add_token(self, token_type: RPALTokenType, value: str) -> None:
        """
        Add a new token to the tokens list
        
        Args:
            token_type: Type of the token
            value: String value of the token
        """
        self.tokens.append(RPALToken(
            token_type, 
            value, 
            self.current_line, 
            self.current_line_position - len(value)
        ))
    
    def scan_tokens(self) -> List[RPALToken]:
        """
        Scan the source code and break it into tokens
        
        Returns:
            List of RPALToken objects
        """
        while not self.is_at_end():
            # Try to match each pattern at the current position
            start_pos = self.current_position
            remaining = self.source[start_pos:]
            
            # Check for whitespace first
            match = self.regex['whitespace'].match(remaining)
            if match:
                # Skip whitespace
                self.advance(len(match.group(0)))
                continue
            
            # Check for comments
            match = self.regex['comment'].match(remaining)
            if match:
                # Skip comments
                self.advance(len(match.group(0)))
                continue
            
            # Check for strings
            match = self.regex['string'].match(remaining)
            if match:
                value = match.group(0)
                self.add_token(RPALTokenType.STRING, value)
                self.advance(len(value))
                continue
            
            # Check for punctuation
            current_char = self.peek()
            if current_char in self.punctuation:
                self.add_token(self.punctuation[current_char], current_char)
                self.advance()
                continue
            
            # Check for integers
            match = self.regex['integer'].match(remaining)
            if match:
                value = match.group(0)
                self.add_token(RPALTokenType.INTEGER, value)
                self.advance(len(value))
                continue
            
            # Check for identifiers and keywords
            match = self.regex['identifier'].match(remaining)
            if match:
                value = match.group(0)
                # Check if this identifier is a keyword
                if value in self.keywords:
                    self.add_token(self.keywords[value], value)
                else:
                    self.add_token(RPALTokenType.IDENTIFIER, value)
                self.advance(len(value))
                continue
            
            # Check for operators
            match = self.regex['operator'].match(remaining)
            if match:
                value = match.group(0)
                self.add_token(RPALTokenType.OPERATOR, value)
                self.advance(len(value))
                continue
            
            # If we get here, we encountered an unexpected character
            raise SyntaxError(f"Unexpected character '{current_char}' at line {self.current_line}, position {self.current_line_position}")
        
        # Add EOF token at the end
        self.add_token(RPALTokenType.EOF, "EOF")
        return self.tokens

# Function to tokenize input string
def tokenize_rpal(source_code: str) -> List[RPALToken]:
    """
    Tokenize RPAL source code into a list of tokens
    
    Args:
        source_code: RPAL source code as a string
    
    Returns:
        List of RPALToken objects
    """
    lexer = RPALLexer(source_code)
    return lexer.scan_tokens()

# # Main function to demonstrate usage
# def main():
#     """Main function to demonstrate lexer usage"""
#     # Try to read from a file
#     try:
#         with open("input.rpal", "r") as input_file:
#             source_code = input_file.read()
#     except FileNotFoundError:
#         # Example source code if file not found
#         source_code = """
#         let Sum(A) = Psum (A, Order A)
#         where rec Psum(T, N) = N eq 0 -> 0 | Psum(T, N-1) + T N
#         in Print(Sum(1, 2, 3, 4, 5))
#         """
#         print("Using example code (input.rpal not found)")
    
#     # Tokenize the source code
#     try:
#         tokens = tokenize_rpal(source_code)
        
#         # Print the tokens for demonstration
#         print("Tokenization Results:")
#         print("=====================")
#         for token in tokens:
#             if token.token_type != RPALTokenType.EOF:
#                 print(f"{token.token_type.name:<10} | {token.value:<20} | Line {token.line}, Pos {token.position}")
    
#     except SyntaxError as e:
#         print(f"Lexer Error: {e}")

# # Run the program if executed directly
# if __name__ == "__main__":
#     main()