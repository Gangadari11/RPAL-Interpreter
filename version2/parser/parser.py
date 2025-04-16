"""
Parser for RPAL Language
Parses tokens into an Abstract Syntax Tree (AST).
"""

from enum import Enum
from lexer.lexical_analyzer import TokenType, Token    # Import token classes from the lexer module

class NodeType(Enum):
    """Enum representing different node types in the AST."""
    # Define all possible types of nodes that can appear in the abstract syntax tree
    # Each enum value is assigned a unique number
    LET = 1             # Let expressions (let ... in ...)
    FUNCTION_FORM = 2   # Function definitions
    IDENTIFIER = 3       # Variable names
    INTEGER = 4         # Integer literals
    STRING = 5  # String literals
    WHERE = 6 # Where expressions
    GAMMA = 7  # Function application
    LAMBDA = 8 # Lambda expressions (fn ... )
    TAU = 9 # Tuple construction
    REC = 10 # Recursive definitions
    AUG = 11 # Augmentation/record extension
    CONDITIONAL = 12 # Conditional expressions (if-then-else)
    OR = 13 # Logical OR
    AND = 14 # Logical AND
    NOT = 15 # Logical NOT
    COMPARE = 16 # Comparison operations
    PLUS = 17 # Addition
    MINUS = 18 # Subtraction
    NEG = 19 # Unary negation
    MULTIPLY = 20 # Multiplication
    DIVIDE = 21  # Division
    POWER = 22  # Exponentiation
    AT = 23 # At operator (@)
    TRUE = 24 # Boolean true
    FALSE = 25  # Boolean false
    NIL = 26 # Nil/null value
    DUMMY = 27 # Placeholder value
    WITHIN = 28 # Within expression
    AND_OP = 29 # And operator for definitions
    EQUAL = 30 # Equality/assignment
    COMMA = 31 # Comma-separated list
    EMPTY_PARAMS = 32 # Empty parameter list

class Node:
    """Class representing a node in the AST."""
    def __init__(self, node_type, value, children):
        self.type = node_type  # The type of this node (from NodeType enum)
        self.value = value # The value/text associated with this node
        self.no_of_children = children # Number of children this node has

class Parser:
    """Parser for RPAL language."""
    def __init__(self, tokens):
        self.tokens = tokens # List of tokens from the lexer
        self.ast = [] # Will hold the AST nodes
        self.string_ast = [] # Will hold string representation of AST

    def parse(self):
        """
        Parse the tokens into an AST.
        
        Returns:
            list: The AST as a list of nodes
        """
        self.tokens.append(Token(TokenType.END_OF_TOKENS, ""))  # Add an End Of Tokens marker
        self.E()  # Start parsing from the entry point
        if self.tokens[0].type == TokenType.END_OF_TOKENS:  
            return self.ast # Parsing succeeded if we consumed all tokens
        else:
            print("Parsing Unsuccessful!") # Error if we have leftover tokens
            print("Remaining unparsed tokens:")
            for token in self.tokens:
                print(token)
            return None

    def convert_ast_to_string_ast(self):
        """
        Convert the AST to a string representation.
        
        Returns:
            list: The AST as a list of strings
        """
        dots = "" # Used for indentation in string representation
        stack = []  # Stack for processing nodes

        # Process nodes until the AST is empty
        while self.ast:
            if not stack: # If stack is empty
                if self.ast[-1].no_of_children == 0: # If the node has no children
                    self.add_strings(dots, self.ast.pop()) # Convert it to string
                else:
                    node = self.ast.pop() # Otherwise push it to stack
                    stack.append(node)
            else: # If stack has nodes
                if self.ast[-1].no_of_children > 0: # If next AST node has children
                    node = self.ast.pop()
                    stack.append(node)
                    dots += "." # Increase indentation for next level
                else:
                    stack.append(self.ast.pop())
                    dots += "."
                    # Process nodes with no children that are ready
                    while stack[-1].no_of_children == 0:
                        self.add_strings(dots, stack.pop())
                        if not stack:
                            break
                        dots = dots[:-1] # Decrease indentation level
                        node = stack.pop()
                        node.no_of_children -= 1 # Decrement children count
                        stack.append(node)

        # Reverse the list to get correct order
        self.string_ast.reverse()
        return self.string_ast

    def add_strings(self, dots, node):
        """
        Add a node to the string AST.
        
        Args:
            dots (str): The indentation for the node
            node (Node): The node to add
        """

        # Special handling for nodes with values
        if node.type in [NodeType.IDENTIFIER, NodeType.INTEGER, NodeType.STRING, NodeType.TRUE,
                         NodeType.FALSE, NodeType.NIL, NodeType.DUMMY]:
            self.string_ast.append(dots + "<" + node.type.name.upper() + ":" + node.value + ">")
        elif node.type == NodeType.FUNCTION_FORM:
            self.string_ast.append(dots + "function_form")
        else:
            self.string_ast.append(dots + node.value) # Just use the node value

    # Grammar rules implementation - each method corresponds to a rule in RPAL grammar
    
    def E(self):
        """Parse an E expression."""
        if not self.tokens: # Check if there are tokens left
            return
            
        token = self.tokens[0]
        # Handle let and fn keywords

        if token.type == TokenType.KEYWORD and token.value in ["let", "fn"]:
            if token.value == "let":
                self.tokens.pop(0)  # Remove "let"
                self.D() # Parse definition
                if self.tokens[0].value != "in":
                    raise ValueError("Parse error: 'in' expected")
                self.tokens.pop(0)  # Remove "in"
                self.E() # Parse expression
                self.ast.append(Node(NodeType.LET, "let", 2)) # Create let node with 2 children
            else:  # fn
                self.tokens.pop(0)  # Remove "fn"
                n = 0
                # Parse parameter list
                while self.tokens and (self.tokens[0].type == TokenType.IDENTIFIER or self.tokens[0].value == "("):
                    self.Vb() # Parse variable binding
                    n += 1
                if not self.tokens or self.tokens[0].value != ".":
                    raise ValueError("Parse error: '.' expected")
                self.tokens.pop(0)  # Remove "."
                self.E()  # Parse function body
                self.ast.append(Node(NodeType.LAMBDA, "lambda", n + 1)) # Create lambda node
        else:
            self.Ew() # Parse expression with 'where' clause

    def Ew(self):
        """Parse an Ew expression."""
        self.T() # Parse the base expression
        if self.tokens[0].value == "where":
            self.tokens.pop(0)  # Remove "where"
            self.Dr() # Parse definition in where clause
            self.ast.append(Node(NodeType.WHERE, "where", 2)) # Create where node

    def T(self):
        """Parse a T expression."""
        self.Ta() # Parse first element
        n = 1
         # Parse additional comma-separated elements
        while self.tokens[0].value == ",":
            self.tokens.pop(0)  # Remove comma
            self.Ta() # Parse next element
            n += 1
        if n > 1:
            self.ast.append(Node(NodeType.TAU, "tau", n))  # Create tuple node if multiple elements

    def Ta(self):
        """Parse a Ta expression."""
        self.Tc() # Parse first part
        # Parse chained augmentations
        while self.tokens[0].value == "aug":
            self.tokens.pop(0)  # Remove "aug"
            self.Tc() # Parse next part
            self.ast.append(Node(NodeType.AUG, "aug", 2))  # Create augmentation node

    def Tc(self):
        """Parse a Tc expression."""
        self.B() # Parse condition
        if self.tokens[0].value == "->":
            self.tokens.pop(0)  # Remove "->"
            self.Tc() # Parse "then" part
            if self.tokens[0].value != "|":
                raise ValueError("Parse error: '|' expected")
            self.tokens.pop(0)  # Remove "|"
            self.Tc() # Parse "else" part
            self.ast.append(Node(NodeType.CONDITIONAL, "->", 3)) # Create conditional node

    def B(self):
        """Parse a B expression."""
        self.Bt() # Parse first operand
        # Parse chained OR operations
        while self.tokens[0].value == "or":
            self.tokens.pop(0)  # Remove "or"
            self.Bt() # Parse next operand
            self.ast.append(Node(NodeType.OR, "or", 2)) # Create OR node

    def Bt(self):
        """Parse a Bt expression."""
        self.Bs() # Parse first operand
        # Parse chained AND operations
        while self.tokens[0].value == "&":
            self.tokens.pop(0)  # Remove "&"
            self.Bs() # Parse next operand
            self.ast.append(Node(NodeType.AND, "&", 2)) # Create AND node

    def Bs(self):
        """Parse a Bs expression."""
        if self.tokens[0].value == "not":
            self.tokens.pop(0)  # Remove "not"
            self.Bp() # Parse operand
            self.ast.append(Node(NodeType.NOT, "not", 1)) # Create NOT node
        else:
            self.Bp() # Parse regular expression

    def Bp(self):
        """Parse a Bp expression."""
        self.A()  # Parse left operand
        # Check for comparison operators
        token = self.tokens[0]
        if token.value in [">", ">=", "<", "<=", "gr", "ge", "ls", "le", "eq", "ne"]:
            self.tokens.pop(0) # Remove operator
            self.A() # Parse right operand
            op_value = token.value
            # Convert symbolic operators to their named equivalents
            if token.value == ">":
                op_value = "gr"
            elif token.value == ">=":
                op_value = "ge"
            elif token.value == "<":
                op_value = "ls"
            elif token.value == "<=":
                op_value = "le"
            self.ast.append(Node(NodeType.COMPARE, op_value, 2)) # Create comparison node

    def A(self):
        """Parse an A expression."""
         # Handle unary plus/minus
        if self.tokens[0].value == "+":
            self.tokens.pop(0)  # Remove unary plus
            self.At() # Parse operand (unary plus has no effect)
        elif self.tokens[0].value == "-":
            self.tokens.pop(0)  # Remove unary minus
            self.At()  # Parse operand
            self.ast.append(Node(NodeType.NEG, "neg", 1)) # Create negation node
        else:
            self.At() # Parse regular term

    # Parse chained addition/subtraction
        while self.tokens[0].value in ["+", "-"]:
            current_token = self.tokens[0]
            self.tokens.pop(0) # Remove operator
            self.At()# Parse next term
            if current_token.value == "+":
                self.ast.append(Node(NodeType.PLUS, "+", 2)) # Create addition node
            else:
                self.ast.append(Node(NodeType.MINUS, "-", 2)) # Create subtraction node

    def At(self):
        """Parse an At expression."""
        self.Af() # Parse first factor
        # Parse chained multiplication/division
        while self.tokens[0].value in ["*", "/"]:
            current_token = self.tokens[0]
            self.tokens.pop(0) # Remove operator
            self.Af() # Parse next factor
            if current_token.value == "*":
                self.ast.append(Node(NodeType.MULTIPLY, "*", 2)) # Create multiplication node
            else:
                self.ast.append(Node(NodeType.DIVIDE, "/", 2)) # Create division node

    def Af(self):
        """Parse an Af expression."""
        self.Ap() # Parse base
        if self.tokens[0].value == "**": 
            self.tokens.pop(0) # Remove exponentiation operator
            self.Af() # Parse exponent
            self.ast.append(Node(NodeType.POWER, "**", 2)) # Create power node

    def Ap(self):
        """Parse an Ap expression."""
        self.R() # Parse first part
        # Parse chained @ operations
        while self.tokens[0].value == "@":
            self.tokens.pop(0) # Remove @ operator
            
            if self.tokens[0].type != TokenType.IDENTIFIER:
                raise ValueError("Parse error: identifier expected")
            # Create node for the identifier
            self.ast.append(Node(NodeType.IDENTIFIER, self.tokens[0].value, 0))
            self.tokens.pop(0) # Remove identifier
            
            self.R() # Parse third part
            self.ast.append(Node(NodeType.AT, "@", 3))  # Create @ node with 3 children

    def R(self):
        """Parse an R expression."""
        self.Rn() # Parse function
        # Parse arguments (implicit function application)
        while (self.tokens[0].type in [TokenType.IDENTIFIER, TokenType.INTEGER, TokenType.STRING] or
               self.tokens[0].value in ["true", "false", "nil", "dummy"] or
               self.tokens[0].value == "("):
            
            self.Rn() # Parse argument
            self.ast.append(Node(NodeType.GAMMA, "gamma", 2)) # Create function application node

    def Rn(self):
        """Parse an Rn expression."""
        token_type = self.tokens[0].type
        token_value = self.tokens[0].value
        
        # Handle different types of primary expressions
        if token_type == TokenType.IDENTIFIER:
             # Variable
            self.ast.append(Node(NodeType.IDENTIFIER, token_value, 0))
            self.tokens.pop(0)
        elif token_type == TokenType.INTEGER:
            # Integer literal
            self.ast.append(Node(NodeType.INTEGER, token_value, 0))
            self.tokens.pop(0)
        elif token_type == TokenType.STRING:
            # String literal
            self.ast.append(Node(NodeType.STRING, token_value, 0))
            self.tokens.pop(0)
        elif token_type == TokenType.KEYWORD:
            # Handle keywords: true, false, nil, dummy
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
        elif token_type == TokenType.PUNCTUATION:
            # Handle parenthesized expressions
            if token_value == "(":
                self.tokens.pop(0) # Remove open parenthesis
                self.E() # Parse expression inside parentheses
                if self.tokens[0].value != ")":
                    raise ValueError("Parse error: ')' expected")
                self.tokens.pop(0) # Remove close parenthesis
            else:
                raise ValueError(f"Parse error: unexpected punctuation '{token_value}'")
        else:
            raise ValueError(f"Parse error: unexpected token '{token_value}'")

    def D(self):
        """Parse a D expression."""
        self.Da() # Parse basic definition
        if self.tokens[0].value == "within":
            self.tokens.pop(0) # Remove "within"
            self.D() # Parse inner definition
            self.ast.append(Node(NodeType.WITHIN, "within", 2)) # Create within node

    def Da(self):
        """Parse a Da expression."""
        self.Dr() # Parse first definition
        n = 1
        # Parse additional and-separated definitions
        while self.tokens[0].value == "and":
            self.tokens.pop(0)  # Remove "and"
            self.Dr() # Parse next definition
            n += 1
        if n > 1:
            self.ast.append(Node(NodeType.AND_OP, "and", n)) # Create and node if multiple definitions

    def Dr(self):
        """Parse a Dr expression."""
        is_rec = False
        if self.tokens[0].value == "rec":
            self.tokens.pop(0) # Remove "rec"
            is_rec = True
        self.Db() # Parse basic definition
        if is_rec:
            self.ast.append(Node(NodeType.REC, "rec", 1))  # Create recursive node

    def Db(self):
        """Parse a Db expression."""
        # Handle parenthesized definition
        if self.tokens[0].type == TokenType.PUNCTUATION and self.tokens[0].value == "(":
            self.tokens.pop(0) # Remove open parenthesis
            self.D() # Parse definition inside parentheses
            if self.tokens[0].value != ")":
                raise ValueError("Parse error: ')' expected")
            self.tokens.pop(0)  # Remove close parenthesis
        elif self.tokens[0].type == TokenType.IDENTIFIER:
            # Check for different forms of definitions
            if len(self.tokens) > 1 and (self.tokens[1].value == "(" or self.tokens[1].type == TokenType.IDENTIFIER):
                # Function form
                # Function form: f x y = ...
                self.ast.append(Node(NodeType.IDENTIFIER, self.tokens[0].value, 0)) # Function name
                self.tokens.pop(0)

                n = 1  # Start with one child (function name)
                # Parse formal parameters
                while self.tokens[0].type == TokenType.IDENTIFIER or self.tokens[0].value == "(":
                    self.Vb() # Parse parameter
                    n += 1
                if self.tokens[0].value != "=":
                    raise ValueError("Parse error: '=' expected")
                self.tokens.pop(0) # Remove equal sign
                self.E() # Parse function body

                self.ast.append(Node(NodeType.FUNCTION_FORM, "function_form", n+1)) # Create function form node
            elif len(self.tokens) > 1 and self.tokens[1].value == "=":
                # Simple variable definition: x = ...
                self.ast.append(Node(NodeType.IDENTIFIER, self.tokens[0].value, 0)) # Variable name
                self.tokens.pop(0)
                self.tokens.pop(0)  # Remove equal sign
                self.E()  # Parse expression
                self.ast.append(Node(NodeType.EQUAL, "=", 2)) # Create equals node
            elif len(self.tokens) > 1 and self.tokens[1].value == ",":
                # Multiple variable definition: x, y, z = ...
                self.Vl() # Parse variable list
                if self.tokens[0].value != "=":
                    raise ValueError("Parse error: '=' expected")
                self.tokens.pop(0)  # Remove equal sign
                self.E() # Parse expression
                self.ast.append(Node(NodeType.EQUAL, "=", 2))  # Create equals node
            else:
                raise ValueError("Parse error: unexpected token sequence")
        else:
            raise ValueError("Parse error: unexpected token")

    def Vb(self):
        """Parse a Vb expression."""
        if self.tokens[0].type == TokenType.PUNCTUATION and self.tokens[0].value == "(":
            # Handle parenthesized parameter list or empty params
            self.tokens.pop(0) # Remove open parenthesis
            isVl = False

            if self.tokens[0].type == TokenType.IDENTIFIER:
                self.Vl() # Parse variable list
                isVl = True
            
            if self.tokens[0].value != ")":
                raise ValueError("Parse error: ')' expected")
            self.tokens.pop(0) # Remove close parenthesis
            if not isVl:
                self.ast.append(Node(NodeType.EMPTY_PARAMS, "()", 0)) # Create empty params node
        elif self.tokens[0].type == TokenType.IDENTIFIER:
            # Single identifier parameter
            self.ast.append(Node(NodeType.IDENTIFIER, self.tokens[0].value, 0)) # Create identifier node
            self.tokens.pop(0) # Remove identifier
        else:
            raise ValueError("Parse error: identifier or '(' expected")

    def Vl(self):
        """Parse a Vl expression."""
        n = 0
        while True:
            if n > 0:
                self.tokens.pop(0)  # Remove comma if not first item
            if self.tokens[0].type != TokenType.IDENTIFIER:
                raise ValueError("Parse error: identifier expected")
            # Create node for each identifier in the list
            self.ast.append(Node(NodeType.IDENTIFIER, self.tokens[0].value, 0))
            
            self.tokens.pop(0) # Remove identifier
            n += 1
            if self.tokens[0].value != ",":  # Stop if no more commas
                break
        
        if n > 1:
            self.ast.append(Node(NodeType.COMMA, ",", n)) # Create comma node for multiple variables
