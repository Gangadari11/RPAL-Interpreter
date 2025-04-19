"""
Parser for RPAL Language
Parses tokens into an Abstract Syntax Tree (AST).
"""

from enum import Enum
from utils.token_types import TokenType, Token

class NodeType(Enum):
    """Enum representing different node types in the AST."""
    LET = 1
    FUNCTION_FORM = 2
    IDENTIFIER = 3
    INTEGER = 4
    STRING = 5
    WHERE = 6
    GAMMA = 7
    LAMBDA = 8
    TAU = 9
    REC = 10
    AUG = 11
    CONDITIONAL = 12
    OR = 13
    AND = 14
    NOT = 15
    COMPARE = 16
    PLUS = 17
    MINUS = 18
    NEG = 19
    MULTIPLY = 20
    DIVIDE = 21
    POWER = 22
    AT = 23
    TRUE = 24
    FALSE = 25
    NIL = 26
    DUMMY = 27
    WITHIN = 28
    AND_OP = 29
    EQUAL = 30
    COMMA = 31
    EMPTY_PARAMS = 32

class Node:
    """Class representing a node in the AST."""
    def __init__(self, node_type, value, children):
        self.type = node_type
        self.value = value
        self.no_of_children = children

class Parser:
    """Parser for RPAL language."""
    def __init__(self, tokens):
        self.tokens = tokens
        self.ast = []
        self.string_ast = []

    def parse(self):
        """
        Parse the tokens into an AST.
        
        Returns:
            list: The AST as a list of nodes
        """
        self.tokens.append(Token(TokenType.END_OF_TOKENS, ""))  # Add an End Of Tokens marker
        self.E()  # Start parsing from the entry point
        if self.tokens[0].type == TokenType.END_OF_TOKENS:
            return self.ast
        else:
            print("Parsing Unsuccessful!")
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
        dots = ""
        stack = []

        while self.ast:
            if not stack:
                if self.ast[-1].no_of_children == 0:
                    self.add_strings(dots, self.ast.pop())
                else:
                    node = self.ast.pop()
                    stack.append(node)
            else:
                if self.ast[-1].no_of_children > 0:
                    node = self.ast.pop()
                    stack.append(node)
                    dots += "."
                else:
                    stack.append(self.ast.pop())
                    dots += "."
                    while stack[-1].no_of_children == 0:
                        self.add_strings(dots, stack.pop())
                        if not stack:
                            break
                        dots = dots[:-1]
                        node = stack.pop()
                        node.no_of_children -= 1
                        stack.append(node)

        # Reverse the list
        self.string_ast.reverse()
        return self.string_ast

    def add_strings(self, dots, node):
        """
        Add a node to the string AST.
        
        Args:
            dots (str): The indentation for the node
            node (Node): The node to add
        """
        if node.type in [NodeType.IDENTIFIER, NodeType.INTEGER, NodeType.STRING, NodeType.TRUE,
                         NodeType.FALSE, NodeType.NIL, NodeType.DUMMY]:
            self.string_ast.append(dots + "<" + node.type.name.upper() + ":" + node.value + ">")
        elif node.type == NodeType.FUNCTION_FORM:
            self.string_ast.append(dots + "function_form")
        else:
            self.string_ast.append(dots + node.value)

    # Grammar rules implementation
    
    def E(self):
        """Parse an E expression."""
        if not self.tokens:
            return
            
        token = self.tokens[0]
        if token.type == TokenType.KEYWORD and token.value in ["let", "fn"]:
            if token.value == "let":
                self.tokens.pop(0)  # Remove "let"
                self.D()
                if self.tokens[0].value != "in":
                    raise ValueError("Parse error: 'in' expected")
                self.tokens.pop(0)  # Remove "in"
                self.E()
                self.ast.append(Node(NodeType.LET, "let", 2))
            else:  # fn
                self.tokens.pop(0)  # Remove "fn"
                n = 0
                while self.tokens and (self.tokens[0].type == TokenType.IDENTIFIER or self.tokens[0].value == "("):
                    self.Vb()
                    n += 1
                if not self.tokens or self.tokens[0].value != ".":
                    raise ValueError("Parse error: '.' expected")
                self.tokens.pop(0)  # Remove "."
                self.E()
                self.ast.append(Node(NodeType.LAMBDA, "lambda", n + 1))
        else:
            self.Ew()

    def Ew(self):
        """Parse an Ew expression."""
        self.T()
        if self.tokens[0].value == "where":
            self.tokens.pop(0)  # Remove "where"
            self.Dr()
            self.ast.append(Node(NodeType.WHERE, "where", 2))

    def T(self):
        """Parse a T expression."""
        self.Ta()
        n = 1
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
        if self.tokens[0].value == "not":
            self.tokens.pop(0)  # Remove "not"
            self.Bp()
            self.ast.append(Node(NodeType.NOT, "not", 1))
        else:
            self.Bp()

    def Bp(self):
        """Parse a Bp expression."""
        self.A()
        token = self.tokens[0]
        if token.value in [">", ">=", "<", "<=", "gr", "ge", "ls", "le", "eq", "ne"]:
            self.tokens.pop(0)
            self.A()
            op_value = token.value
            if token.value == ">":
                op_value = "gr"
            elif token.value == ">=":
                op_value = "ge"
            elif token.value == "<":
                op_value = "ls"
            elif token.value == "<=":
                op_value = "le"
            self.ast.append(Node(NodeType.COMPARE, op_value, 2))

    def A(self):
        """Parse an A expression."""
        if self.tokens[0].value == "+":
            self.tokens.pop(0)  # Remove unary plus
            self.At()
        elif self.tokens[0].value == "-":
            self.tokens.pop(0)  # Remove unary minus
            self.At()
            self.ast.append(Node(NodeType.NEG, "neg", 1))
        else:
            self.At()

        while self.tokens[0].value in ["+", "-"]:
            current_token = self.tokens[0]
            self.tokens.pop(0)
            self.At()
            if current_token.value == "+":
                self.ast.append(Node(NodeType.PLUS, "+", 2))
            else:
                self.ast.append(Node(NodeType.MINUS, "-", 2))

    def At(self):
        """Parse an At expression."""
        self.Af()
        while self.tokens[0].value in ["*", "/"]:
            current_token = self.tokens[0]
            self.tokens.pop(0)
            self.Af()
            if current_token.value == "*":
                self.ast.append(Node(NodeType.MULTIPLY, "*", 2))
            else:
                self.ast.append(Node(NodeType.DIVIDE, "/", 2))

    def Af(self):
        """Parse an Af expression."""
        self.Ap()
        if self.tokens[0].value == "**":
            self.tokens.pop(0)
            self.Af()
            self.ast.append(Node(NodeType.POWER, "**", 2))

    def Ap(self):
        """Parse an Ap expression."""
        self.R()
        while self.tokens[0].value == "@":
            self.tokens.pop(0)
            
            if self.tokens[0].type != TokenType.IDENTIFIER:
                raise ValueError("Parse error: identifier expected")
            
            self.ast.append(Node(NodeType.IDENTIFIER, self.tokens[0].value, 0))
            self.tokens.pop(0)
            
            self.R()
            self.ast.append(Node(NodeType.AT, "@", 3))

    def R(self):
        """Parse an R expression."""
        self.Rn()
        while (self.tokens[0].type in [TokenType.IDENTIFIER, TokenType.INTEGER, TokenType.STRING] or
               self.tokens[0].value in ["true", "false", "nil", "dummy"] or
               self.tokens[0].value == "("):
            
            self.Rn()
            self.ast.append(Node(NodeType.GAMMA, "gamma", 2))

    def Rn(self):
        """Parse an Rn expression."""
        token_type = self.tokens[0].type
        token_value = self.tokens[0].value
        
        if token_type == TokenType.IDENTIFIER:
            self.ast.append(Node(NodeType.IDENTIFIER, token_value, 0))
            self.tokens.pop(0)
        elif token_type == TokenType.INTEGER:
            self.ast.append(Node(NodeType.INTEGER, token_value, 0))
            self.tokens.pop(0)
        elif token_type == TokenType.STRING:
            self.ast.append(Node(NodeType.STRING, token_value, 0))
            self.tokens.pop(0)
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
        self.Da()
        if self.tokens[0].value == "within":
            self.tokens.pop(0)
            self.D()
            self.ast.append(Node(NodeType.WITHIN, "within", 2))

    def Da(self):
        """Parse a Da expression."""
        self.Dr()
        n = 1
        while self.tokens[0].value == "and":
            self.tokens.pop(0)
            self.Dr()
            n += 1
        if n > 1:
            self.ast.append(Node(NodeType.AND_OP, "and", n))

    def Dr(self):
        """Parse a Dr expression."""
        is_rec = False
        if self.tokens[0].value == "rec":
            self.tokens.pop(0)
            is_rec = True
        self.Db()
        if is_rec:
            self.ast.append(Node(NodeType.REC, "rec", 1))

    def Db(self):
        """Parse a Db expression."""
        if self.tokens[0].type == TokenType.PUNCTUATION and self.tokens[0].value == "(":
            self.tokens.pop(0)
            self.D()
            if self.tokens[0].value != ")":
                raise ValueError("Parse error: ')' expected")
            self.tokens.pop(0)
        elif self.tokens[0].type == TokenType.IDENTIFIER:
            if len(self.tokens) > 1 and (self.tokens[1].value == "(" or self.tokens[1].type == TokenType.IDENTIFIER):
                # Function form
                self.ast.append(Node(NodeType.IDENTIFIER, self.tokens[0].value, 0))
                self.tokens.pop(0)

                n = 1  # Identifier child
                while self.tokens[0].type == TokenType.IDENTIFIER or self.tokens[0].value == "(":
                    self.Vb()
                    n += 1
                if self.tokens[0].value != "=":
                    raise ValueError("Parse error: '=' expected")
                self.tokens.pop(0)
                self.E()

                self.ast.append(Node(NodeType.FUNCTION_FORM, "function_form", n+1))
            elif len(self.tokens) > 1 and self.tokens[1].value == "=":
                self.ast.append(Node(NodeType.IDENTIFIER, self.tokens[0].value, 0))
                self.tokens.pop(0)
                self.tokens.pop(0)  # Remove equal
                self.E()
                self.ast.append(Node(NodeType.EQUAL, "=", 2))
            elif len(self.tokens) > 1 and self.tokens[1].value == ",":
                self.Vl()
                if self.tokens[0].value != "=":
                    raise ValueError("Parse error: '=' expected")
                self.tokens.pop(0)
                self.E()
                self.ast.append(Node(NodeType.EQUAL, "=", 2))
            else:
                raise ValueError("Parse error: unexpected token sequence")
        else:
            raise ValueError("Parse error: unexpected token")

    def Vb(self):
        """Parse a Vb expression."""
        if self.tokens[0].type == TokenType.PUNCTUATION and self.tokens[0].value == "(":
            self.tokens.pop(0)
            isVl = False

            if self.tokens[0].type == TokenType.IDENTIFIER:
                self.Vl()
                isVl = True
            
            if self.tokens[0].value != ")":
                raise ValueError("Parse error: ')' expected")
            self.tokens.pop(0)
            if not isVl:
                self.ast.append(Node(NodeType.EMPTY_PARAMS, "()", 0))
        elif self.tokens[0].type == TokenType.IDENTIFIER:
            self.ast.append(Node(NodeType.IDENTIFIER, self.tokens[0].value, 0))
            self.tokens.pop(0)
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