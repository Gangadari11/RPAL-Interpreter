"""
Parser for RPAL Language
Parses tokens into an Abstract Syntax Tree (AST).
"""

from enum import Enum
from utils.token_types import TokenType, Token # Importing necessary classes for tokenization


class NodeType(Enum):
    """Enum representing different node types in the AST."""
    # Define all possible node types in the AST as enum values

    LET = 1  # For let expressions
    FUNCTION_FORM = 2 # For function definitions
    IDENTIFIER = 3 # For variable names
    INTEGER = 4 # For integer literals
    STRING = 5 # For string literals
    WHERE = 6 # For where clauses
    GAMMA = 7 # For function application
    LAMBDA = 8  # For lambda expressions
    TAU = 9 # For tuples
    REC = 10  # For recursive definitions
    AUG = 11  # For augmentation operator
    CONDITIONAL = 12 # For conditional expressions (if-then-else)
    OR = 13 # For logical OR
    AND = 14 # For logical AND
    NOT = 15 # For logical NOT
    COMPARE = 16 # For comparison operators (>, >=, <, <=, ==, !=)
    PLUS = 17 # For addition operator
    MINUS = 18 # For subtraction operator
    NEG = 19 # For negation operator
    MULTIPLY = 20 # For multiplication operator
    DIVIDE = 21 # For division operator
    POWER = 22 # For exponentiation operator
    AT = 23 # For at operator
    TRUE = 24  # For boolean true
    FALSE = 25 # For boolean false
    NIL = 26 # For nil value
    DUMMY = 27 # For dummy placeholder
    WITHIN = 28  # For within expressions
    AND_OP = 29 # For and operator
    EQUAL = 30 # For equality operator
    COMMA = 31  # For comma-separated lists
    EMPTY_PARAMS = 32 # For empty parameter lists

class Node:
    """Class representing a node in the AST."""
    def __init__(self, node_type, value, children):
        self.type = node_type # Type of the node (from NodeType enum)
        self.value = value  # Value of the node (e.g., variable name, operator symbol)
        self.no_of_children = children # Number of children this node has

class Parser:
    """Parser for RPAL language."""
    def __init__(self, tokens):
        self.tokens = tokens # Input tokens to parse
        self.ast = [] # The abstract syntax tree being built
        self.string_ast = []  # String representation of the AST

    def parse(self):
        """
        Parse the tokens into an AST.
        
        Returns:
            list: The AST as a list of nodes
        """
        self.tokens.append(Token(TokenType.END_OF_TOKENS, ""))  # Add an End Of Tokens marker
        self.E()  # Start parsing from the entry point (E production rule)
        if self.tokens[0].type == TokenType.END_OF_TOKENS:
            return self.ast  # Return the completed AST if parsing was successful
        else:
            print("Parsing Unsuccessful!") # Print error message if parsing failed
            print("Remaining unparsed tokens:")
            for token in self.tokens:
                print(token) # Print remaining tokens
            return None # Return None if parsing failed

    def convert_ast_to_string_ast(self):
        """
        Convert the AST to a string representation.
        
        Returns:
            list: The AST as a list of strings
        """
        dots = ""   # String to track indentation leve
        stack = []   # Stack to manage traversal of the AST

        while self.ast: # Process until AST is empty
            if not stack: # If stack is empty, process next node from AST
                if self.ast[-1].no_of_children == 0: # If leaf node
                    self.add_strings(dots, self.ast.pop()) # Add to string representation
                else: # If non-leaf node
                    node = self.ast.pop()
                    stack.append(node) # Push to stack for processing children
            else: # If stack is not empty
                if self.ast[-1].no_of_children > 0: # If next node has children
                    node = self.ast.pop()
                    stack.append(node) # Push to stack
                    dots += "."  # Increase indentation level
                else:
                    stack.append(self.ast.pop())
                    dots += "." # Increase indentation level
                    while stack[-1].no_of_children == 0:
                        self.add_strings(dots, stack.pop()) # Add to string representation
                        if not stack: # If stack is empty, we're done
                            break
                        dots = dots[:-1] # Decrease indentation level
                        node = stack.pop()
                        node.no_of_children -= 1 # Decrease child count of parent
                        stack.append(node) # Push parent back to stack

        # Reverse the list to get correct ordering
        self.string_ast.reverse()
        return self.string_ast

    def add_strings(self, dots, node):
        """
        Add a node to the string AST.
        
        Args:
            dots (str): The indentation for the node
            node (Node): The node to add
        """
        # Check the type of the node and add it to the string AST accordingly
        if node.type in [NodeType.IDENTIFIER, NodeType.INTEGER, NodeType.STRING, NodeType.TRUE,
                         NodeType.FALSE, NodeType.NIL, NodeType.DUMMY]:
            # If the node is an identifier, integer, string, true, false, nil or dummy, add it to the string AST with its type and value
            self.string_ast.append(dots + "<" + node.type.name.upper() + ":" + node.value + ">")
        elif node.type == NodeType.FUNCTION_FORM:
            # If the node is a function form, add it to the string AST with the function_form label
            self.string_ast.append(dots + "function_form")
        else:
            # If the node is anything else, add it to the string AST with its value
            self.string_ast.append(dots + node.value)

    # Grammar rules implementation
    
    def E(self):
        """Parse an E expression."""
        if not self.tokens:
            return
            
        token = self.tokens[0]
        # Check if the token is a keyword and if it is either "let" or "fn"
        if token.type == TokenType.KEYWORD and token.value in ["let", "fn"]:
            # If the token is "let"
            if token.value == "let":
                self.tokens.pop(0)  # Remove "let"
                self.D()  # Parse the next expression
                # Check if the next token is "in"
                if self.tokens[0].value != "in":
                    raise ValueError("Parse error: 'in' expected")
                self.tokens.pop(0)  # Remove "in"
                self.E()  # Parse the next expression
                self.ast.append(Node(NodeType.LET, "let", 2))  # Add a LET node to the AST
            else:  # fn
                self.tokens.pop(0)  # Remove "fn"
                n = 0
                # Parse the next expression until a "." is encountered
                while self.tokens and (self.tokens[0].type == TokenType.IDENTIFIER or self.tokens[0].value == "("):
                    self.Vb()
                    n += 1
                # Check if a "." is encountered
                if not self.tokens or self.tokens[0].value != ".":
                    raise ValueError("Parse error: '.' expected")
                self.tokens.pop(0)  # Remove "."
                self.E()  # Parse the next expression
                self.ast.append(Node(NodeType.LAMBDA, "lambda", n + 1))  # Add a LAMBDA node to the AST
        else:
            self.Ew()  # Parse the next expression

    def Ew(self):
        """Parse an Ew expression."""
        self.T()
        # Check if the next token is "where"
        if self.tokens[0].value == "where":
            self.tokens.pop(0)  # Remove "where"
            self.Dr()
            self.ast.append(Node(NodeType.WHERE, "where", 2))

    def T(self):
        """Parse a T expression."""
        self.Ta()
        n = 1
        # Loop through the tokens until a comma is not found
        while self.tokens[0].value == ",":
            self.tokens.pop(0)  # Remove comma
            self.Ta()
            n += 1
        if n > 1:
            self.ast.append(Node(NodeType.TAU, "tau", n))

    def Ta(self):
        """Parse a Ta expression."""
        self.Tc()
        while self.tokens[0].value == "aug":
            self.tokens.pop(0)  # Remove "aug"
            self.Tc()
            self.ast.append(Node(NodeType.AUG, "aug", 2))

    def Tc(self):
        """Parse a Tc expression."""
        self.B()
        if self.tokens[0].value == "->":
            self.tokens.pop(0)  # Remove "->"
            self.Tc()
            if self.tokens[0].value != "|":
                raise ValueError("Parse error: '|' expected")
            self.tokens.pop(0)  # Remove "|"
            self.Tc()
            self.ast.append(Node(NodeType.CONDITIONAL, "->", 3))

    def B(self):
        """Parse a B expression."""
        self.Bt()
        while self.tokens[0].value == "or":
            self.tokens.pop(0)  # Remove "or"
            self.Bt()
            self.ast.append(Node(NodeType.OR, "or", 2))

    def Bt(self):
        """Parse a Bt expression."""
        self.Bs()
        while self.tokens[0].value == "&":
            self.tokens.pop(0)  # Remove "&"
            self.Bs()
            self.ast.append(Node(NodeType.AND, "&", 2))

    def Bs(self):
        """Parse a Bs expression."""
        # Check if the first token is "not"
        if self.tokens[0].value == "not":
            self.tokens.pop(0)  # Remove "not"
            self.Bp()
            self.ast.append(Node(NodeType.NOT, "not", 1))
        else:
            self.Bp()

    def Bp(self):
        """Parse a Bp expression."""
        # Call the A() method to parse the first part of the expression
        self.A()
        # Get the current token
        token = self.tokens[0]
        # Check if the token value is one of the comparison operators
        if token.value in [">", ">=", "<", "<=", "gr", "ge", "ls", "le", "eq", "ne"]:
            # Remove the token from the list
            self.tokens.pop(0)
            # Call the A() method to parse the second part of the expression
            self.A()
            # Store the token value in a variable
            op_value = token.value
            # Convert the token value to the appropriate operator
            if token.value == ">":
                op_value = "gr"
            elif token.value == ">=":
                op_value = "ge"
            elif token.value == "<":
                op_value = "ls"
            elif token.value == "<=":
                op_value = "le"
            # Create a new Node object with the comparison operator and append it to the ast list
            self.ast.append(Node(NodeType.COMPARE, op_value, 2))

    def A(self):
        """Parse an A expression."""
        # Check if the first token is a unary plus or minus
        if self.tokens[0].value == "+":
            self.tokens.pop(0)  # Remove unary plus
            self.At()
        elif self.tokens[0].value == "-":
            self.tokens.pop(0)  # Remove unary minus
            self.At()
            self.ast.append(Node(NodeType.NEG, "neg", 1))  # Append a negation node to the AST
        else:
            self.At()

        # Loop through the tokens and check if they are addition or subtraction operators
        while self.tokens[0].value in ["+", "-"]:
            current_token = self.tokens[0]
            self.tokens.pop(0)
            self.At()
            # Append the appropriate node to the AST based on the operator
            if current_token.value == "+":
                self.ast.append(Node(NodeType.PLUS, "+", 2))
            else:
                self.ast.append(Node(NodeType.MINUS, "-", 2))

    def At(self):
        """Parse an At expression."""
        # Parse the first factor
        self.Af()
        # While the current token is a multiplication or division operator
        while self.tokens[0].value in ["*", "/"]:
            # Store the current token
            current_token = self.tokens[0]
            # Remove the current token from the token list
            self.tokens.pop(0)
            # Parse the next factor
            self.Af()
            # If the current token is a multiplication operator
            if current_token.value == "*":
                # Append a multiply node to the abstract syntax tree
                self.ast.append(Node(NodeType.MULTIPLY, "*", 2))
            # Else if the current token is a division operator
            else:
                # Append a divide node to the abstract syntax tree
                self.ast.append(Node(NodeType.DIVIDE, "/", 2))

    def Af(self):
        """Parse an Af expression."""
        # Parse an Ap expression
        self.Ap()
        # Check if the current token is "**"
        if self.tokens[0].value == "**":
            # Remove the "**" token from the list
            self.tokens.pop(0)
            # Parse an Af expression
            self.Af()
            # Append a Node to the ast list with the type POWER, value "**", and 2 children
            self.ast.append(Node(NodeType.POWER, "**", 2))

    def Ap(self):
        """Parse an Ap expression."""
        # Parse the R expression
        self.R()
        # While the current token is an '@' symbol
        while self.tokens[0].value == "@":
            # Remove the '@' symbol from the token list
            self.tokens.pop(0)
            
            # If the next token is not an identifier, raise a ValueError
            if self.tokens[0].type != TokenType.IDENTIFIER:
                raise ValueError("Parse error: identifier expected")
            
            # Append a Node to the AST with the identifier value
            self.ast.append(Node(NodeType.IDENTIFIER, self.tokens[0].value, 0))
            # Remove the identifier from the token list
            self.tokens.pop(0)
            
            # Parse the R expression
            self.R()
            # Append a Node to the AST with the '@' symbol
            self.ast.append(Node(NodeType.AT, "@", 3))

    def R(self):
        """Parse an R expression."""
        # Parse an R expression by calling the Rn() method
        self.Rn()
        # While the first token is an identifier, integer, string, true, false, nil, dummy, or an opening parenthesis
        while (self.tokens[0].type in [TokenType.IDENTIFIER, TokenType.INTEGER, TokenType.STRING] or
               self.tokens[0].value in ["true", "false", "nil", "dummy"] or
               self.tokens[0].value == "("):
            
            # Parse another R expression by calling the Rn() method
            self.Rn()
            # Append a new node to the AST with the type GAMMA and the value "gamma" and 2 children
            self.ast.append(Node(NodeType.GAMMA, "gamma", 2))

    def Rn(self):
        """Parse an Rn expression."""
        # Get the type and value of the first token in the tokens list
        token_type = self.tokens[0].type
        token_value = self.tokens[0].value
        
        # If the token is an identifier, create a Node with the identifier type and value, and append it to the ast list
        if token_type == TokenType.IDENTIFIER:
            self.ast.append(Node(NodeType.IDENTIFIER, token_value, 0))
            self.tokens.pop(0)
        # If the token is an integer, create a Node with the integer type and value, and append it to the ast list
        elif token_type == TokenType.INTEGER:
            self.ast.append(Node(NodeType.INTEGER, token_value, 0))
            self.tokens.pop(0)
        # If the token is a string, create a Node with the string type and value, and append it to the ast list
        elif token_type == TokenType.STRING:
            self.ast.append(Node(NodeType.STRING, token_value, 0))
            self.tokens.pop(0)
        # If the token is a keyword, check the value and create a Node with the corresponding type and value, and append it to the ast list
        elif token_type == TokenType.KEYWORD:
            if token_value == "true":
                self.ast.append(Node(NodeType.TRUE, token_value, 0))
                self.tokens.pop(0)
            elif token_value == "false":
                self.ast.append(Node(NodeType.FALSE, token_value, 0))
                self.tokens.pop(0)
            elif token_value == "nil":
                self.ast.append(Node(NodeType.NIL, token_value, 0))
                self.tokens.pop(0)
            elif token_value == "dummy":
                self.ast.append(Node(NodeType.DUMMY, token_value, 0))
                self.tokens.pop(0)
            else:
                raise ValueError(f"Parse error: unexpected keyword '{token_value}'")
        # If the token is punctuation, check the value and create a Node with the corresponding type and value, and append it to the ast list
        elif token_type == TokenType.PUNCTUATION:
            if token_value == "(":
                self.tokens.pop(0)
                self.E()
                if self.tokens[0].value != ")":
                    raise ValueError("Parse error: ')' expected")
                self.tokens.pop(0)
            else:
                raise ValueError(f"Parse error: unexpected punctuation '{token_value}'")
        else:
            raise ValueError(f"Parse error: unexpected token '{token_value}'")

    def D(self):
        """Parse a D expression."""
        # Parse a Da expression
        self.Da()
        # Check if the next token is "within"
        if self.tokens[0].value == "within":
            # Remove the "within" token from the list
            self.tokens.pop(0)
            # Parse a D expression
            self.D()
            # Append a Node to the AST with the type "within" and the value "within" and the number of children as 2
            self.ast.append(Node(NodeType.WITHIN, "within", 2))

    def Da(self):
        """Parse a Da expression."""
        # Parse a Dr expression
        self.Dr()
        # Initialize a counter for the number of "and" tokens
        n = 1
        # While the first token is "and"
        while self.tokens[0].value == "and":
            # Remove the "and" token from the list
            self.tokens.pop(0)
            # Parse a Dr expression
            self.Dr()
            # Increment the counter
            n += 1
        # If the counter is greater than 1, add an AND_OP node to the AST
        if n > 1:
            self.ast.append(Node(NodeType.AND_OP, "and", n))

    def Dr(self):
        """Parse a Dr expression."""
        # Initialize a variable to check if the expression is recursive
        is_rec = False
        # Check if the first token is "rec"
        if self.tokens[0].value == "rec":
            # Remove the "rec" token from the list
            self.tokens.pop(0)
            # Set the is_rec variable to True
            is_rec = True
        # Call the Db method to parse the Db expression
        self.Db()
        # If the expression is recursive, append a Node to the ast list with the type REC and the value "rec"
        if is_rec:
            self.ast.append(Node(NodeType.REC, "rec", 1))

    def Db(self):
        """Parse a Db expression."""
        # Check if the first token is a punctuation and if it is an opening parenthesis
        if self.tokens[0].type == TokenType.PUNCTUATION and self.tokens[0].value == "(":
            # Remove the opening parenthesis from the token list
            self.tokens.pop(0)
            # Parse the D expression
            self.D()
            # Check if the next token is a closing parenthesis
            if self.tokens[0].value != ")":
                raise ValueError("Parse error: ')' expected")
            # Remove the closing parenthesis from the token list
            self.tokens.pop(0)
        # Check if the first token is an identifier
        elif self.tokens[0].type == TokenType.IDENTIFIER:
            # Check if the next token is an opening parenthesis or an identifier
            if len(self.tokens) > 1 and (self.tokens[1].value == "(" or self.tokens[1].type == TokenType.IDENTIFIER):
                # Function form
                # Add a new node to the abstract syntax tree with the identifier as the value
                self.ast.append(Node(NodeType.IDENTIFIER, self.tokens[0].value, 0))
                # Remove the identifier from the token list
                self.tokens.pop(0)

                n = 1  # Identifier child
                # While the next token is an identifier or an opening parenthesis
                while self.tokens[0].type == TokenType.IDENTIFIER or self.tokens[0].value == "(":
                    # Parse the Vb expression
                    self.Vb()
                    n += 1
                # Check if the next token is an equal sign
                if self.tokens[0].value != "=":
                    raise ValueError("Parse error: '=' expected")
                # Remove the equal sign from the token list
                self.tokens.pop(0)
                # Parse the E expression
                self.E()

                # Add a new node to the abstract syntax tree with the function form as the value
                self.ast.append(Node(NodeType.FUNCTION_FORM, "function_form", n+1))
            # Check if the next token is an equal sign
            elif len(self.tokens) > 1 and self.tokens[1].value == "=":
                # Add a new node to the abstract syntax tree with the identifier as the value
                self.ast.append(Node(NodeType.IDENTIFIER, self.tokens[0].value, 0))
                # Remove the identifier from the token list
                self.tokens.pop(0)
                # Remove the equal sign from the token list
                self.tokens.pop(0)  # Remove equal
                # Parse the E expression
                self.E()
                # Add a new node to the abstract syntax tree with the equal sign as the value
                self.ast.append(Node(NodeType.EQUAL, "=", 2))
            # Check if the next token is a comma
            elif len(self.tokens) > 1 and self.tokens[1].value == ",":
                # Parse the Vl expression
                self.Vl()
                # Check if the next token is an equal sign
                if self.tokens[0].value != "=":
                    raise ValueError("Parse error: '=' expected")
                # Remove the equal sign from the token list
                self.tokens.pop(0)
                # Parse the E expression
                self.E()
                # Add a new node to the abstract syntax tree with the equal sign as the value
                self.ast.append(Node(NodeType.EQUAL, "=", 2))
            else:
                raise ValueError("Parse error: unexpected token sequence")
        else:
            raise ValueError("Parse error: unexpected token")

    def Vb(self):
        """Parse a Vb expression."""
        # Check if the first token is a punctuation and if it is an opening parenthesis
        if self.tokens[0].type == TokenType.PUNCTUATION and self.tokens[0].value == "(":
            # Remove the opening parenthesis from the token list
            self.tokens.pop(0)
            isVl = False

            # Check if the next token is an identifier
            if self.tokens[0].type == TokenType.IDENTIFIER:
                # Parse the Vl expression
                self.Vl()
                isVl = True
            
            # Check if the next token is a closing parenthesis
            if self.tokens[0].value != ")":
                # Raise an error if it is not
                raise ValueError("Parse error: ')' expected")
            # Remove the closing parenthesis from the token list
            self.tokens.pop(0)
            # If the Vl expression was not parsed, append an empty parameters node to the AST
            if not isVl:
                self.ast.append(Node(NodeType.EMPTY_PARAMS, "()", 0))
        # Check if the first token is an identifier
        elif self.tokens[0].type == TokenType.IDENTIFIER:
            # Append an identifier node to the AST
            self.ast.append(Node(NodeType.IDENTIFIER, self.tokens[0].value, 0))
            # Remove the identifier from the token list
            self.tokens.pop(0)
        # Raise an error if the first token is neither an identifier nor an opening parenthesis
        else:
            raise ValueError("Parse error: identifier or '(' expected")

    def Vl(self):
        """Parse a Vl expression."""
        n = 0
        while True:
            if n > 0:
                self.tokens.pop(0)  # Remove comma
            if self.tokens[0].type != TokenType.IDENTIFIER:
                raise ValueError("Parse error: identifier expected")
            self.ast.append(Node(NodeType.IDENTIFIER, self.tokens[0].value, 0))
            
            self.tokens.pop(0)
            n += 1
            if self.tokens[0].value != ",":
                break
        
        if n > 1:
            self.ast.append(Node(NodeType.COMMA, ",", n))