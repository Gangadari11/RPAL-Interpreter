"""
Node classes for RPAL Language AST
Define the structure and behavior of nodes in the  AST.
"""

class Node:
    """Base class for nodes in the Abstract Syntax Tree (AST)."""
    def __init__(self):
        self.data = None # The actual data stored in this node (eg -: operator or value)
        self.depth = 0 # Depth level in the AST
        self.parent = None # Reference to parent node
        self.children = [] # List of child nodes
        self.is_standardized = False # Indicates whether the node has been standarized

    def set_data(self, data):
        """Set the data of the node."""
        self.data = data

    def get_data(self):
        """Get the data of the node."""
        return self.data

    def get_degree(self):
        """Get the degree (number of chldren) of the node."""
        return len(self.children)