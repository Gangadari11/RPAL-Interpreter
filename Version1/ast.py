from enum import Enum
from typing import List, Optional, Union

from standizer.lexer import RPALToken, RPALTokenType
from standizer.parser import ASTNode

class NodeType(Enum):
    """
    Enumeration of all possible AST node types for RPAL language
    """
    LET = 1            # let expressions
    FUNCTION_FORM = 2  # function definitions
    IDENTIFIER = 3     # variable names
    INTEGER = 4        # integer literals
    STRING = 5         # string literals
    WHERE = 6          # where expressions
    GAMMA = 7          # function application
    LAMBDA = 8         # lambda expressions
    TAU = 9            # tuple constructor
    REC = 10           # recursive definitions
    AUG = 11           # augmentation
    CONDITIONAL = 12   # conditional expressions
    OR = 13            # logical OR
    AND = 14           # logical AND
    NOT = 15           # logical NOT
    COMPARE = 16       # comparison operators (gr, ge, ls, le, eq, ne)
    PLUS = 17          # addition
    MINUS = 18         # subtraction
    NEG = 19           # unary negation
    MULTIPLY = 20      # multiplication
    DIVIDE = 21        # division
    POWER = 22         # exponentiation
    AT = 23            # at operator
    TRUE = 24          # boolean true
    FALSE = 25         # boolean false
    NIL = 26           # nil value
    DUMMY = 27         # dummy placeholder
    WITHIN = 28        # within definitions
    AND_DEF = 29       # and in definitions
    EQUAL = 30         # equality in definitions
    COMMA = 31         # comma-separated list
    EMPTY_TUPLE = 32   # empty tuple

class Node:
    """Base class for all AST nodes"""
    def __init__(self, node_type: NodeType, value: str):
        self.node_type = node_type
        self.value = value
        self.children = []
    
    def add_child(self, child: 'Node') -> None:
        """Add a child node to this node"""
        self.children.append(child)
    
    def print_ast(self, indent: int = 0) -> List[str]:
        """
        Print the AST with proper indentation
        
        Args:
            indent: Current indentation level
            
        Returns:
            List of strings representing the AST
        """
        dots = "." * indent
        result = []
        
        # Print this node
        if self.node_type in [NodeType.IDENTIFIER, NodeType.INTEGER, NodeType.STRING, 
                             NodeType.TRUE, NodeType.FALSE, NodeType.NIL, NodeType.DUMMY]:
            result.append(f"{dots}<{self.node_type.name}:{self.value}>")
        elif self.node_type == NodeType.FUNCTION_FORM:
            result.append(f"{dots}function_form")
        else:
            result.append(f"{dots}{self.value}")
        
        # Print children with increased indentation
        for child in self.children:
            result.extend(child.print_ast(indent + 1))
        
        return result

class ASTBuilder:
    """
    Class to build an AST from a flat representation
    """
    @staticmethod
    def build_ast_from_stack(ast_stack: List[ASTNode]) -> Node:
        """
        Build an AST from a stack of ASTNode objects
        
        Args:
            ast_stack: List of ASTNode objects from the parser
            
        Returns:
            The root Node of the built AST
        """
        # Create a copy to avoid modifying the original
        stack = ast_stack.copy()
        stack.reverse()  # Reverse to process from first to last
        
        return ASTBuilder._build_node(stack)
    
    @staticmethod
    def _build_node(stack: List[ASTNode]) -> Node:
        """
        Recursively build a node and its children from the stack
        
        Args:
            stack: Remaining ASTNode objects
            
        Returns:
            A Node with its children populated
        """
        if not stack:
            return None
        
        ast_node = stack.pop(0)
        node = Node(ast_node.type, ast_node.value)
        
        # Add children based on children_count
        for _ in range(ast_node.children_count):
            child = ASTBuilder._build_node(stack)
            if child:
                node.add_child(child)
        
        return node

class ASTPrinter:
    """
    Class to print an AST in the required format
    """
    @staticmethod
    def print_ast(root: Node) -> List[str]:
        """
        Print the AST in the required format
        
        Args:
            root: Root node of the AST
            
        Returns:
            List of strings representing the AST
        """
        if not root:
            return []
        
        return root.print_ast()

# Modify the RPALParser class to use the new AST classes
class RPALParser:
    """
    Parser for RPAL language that builds an Abstract Syntax Tree (AST)
    """
    def __init__(self, tokens: List[RPALToken]):
        """
        Initialize the parser with a list of tokens
        
        Args:
            tokens: List of tokens from the lexical analyzer
        """
        self.tokens = tokens.copy()  # Make a copy to avoid modifying the original
        self.ast_nodes = []  # Stack used to build the AST
        self.string_ast = []  # String representation of the AST
    
    def parse(self) -> Optional[Node]:
        """
        Parse the tokens and build an AST
        
        Returns:
            The root node of the built Abstract Syntax Tree
        """
        # Add an end-of-tokens marker
        self.tokens.append(RPALToken(RPALTokenType.EOF, "EOF"))
        
        # Start parsing from the entry point
        self.E()
        
        # Check if we consumed all tokens
        if self.tokens[0].token_type == RPALTokenType.EOF:
            # Convert the flat AST to a hierarchical structure
            if self.ast_nodes:
                ast_root = ASTBuilder.build_ast_from_stack(self.ast_nodes)
                return ast_root
            return None
        else:
            print("Error: Parsing incomplete. Remaining tokens:")
            for token in self.tokens:
                print(f"<{token.token_type.name}, '{token.value}'>")
            return None
    
    def print_ast(self) -> List[str]:
        """
        Print the AST with proper indentation
        
        Returns:
            List of strings representing the AST
        """
        root = self.parse()
        if root:
            return ASTPrinter.print_ast(root)
        return []
    
    # The grammar rule methods would remain the same,
    # but they would add ASTNode objects to self.ast_nodes
    # as before
    # ...