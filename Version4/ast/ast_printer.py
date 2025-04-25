""" 
Abstract Syntax Tree (AST) for RPAL Language
Represents the structure of an RPAL program.
"""

from ast.ast_node import Node, NodeFactory

class AST:
    """Class representing an Abstract Syntax Tree."""
    def __init__(self,root=None):
        self.root = root

    def set_root(self, root):
        """Set the rootnode of the AST."""
        self.root = root

    def get_root(self):
        """Get the root node of the AST."""
        return self.root
    
    def standarize(self):
        """Standarize the AST."""
        if not self.root.is_standarized:
            self.root.standarize()

    def pre_order_traverse(self, node, i):
        """
        Traverse the AST in pre-order.
        
        Args:
            node: The current node
            i: The current imdentation level
            """
        
        print("." * i + str(node.get_data()))

        for child in node.children:
            self.pre_order_traverse(child, i + 1)

    def print_ast(self):
        """Print the AST."""
        self.pre_order_traverse(self.get_root(), 0)

    