"""
Combined implementation for RPAL Language AST
Defines  the structure, behavior, creation and traversal of an Abstract Syntax Tree 
"""

class Node:
    """Base class for nodes in the AST."""
    def __init__(self):
        self.data = None
        self.depth = 0
        self.parent = None
        self.children = []
        self.is_standarized = False

    def set_data(self, data):
        """Set the data of the node."""
        self.data = data

    def get_data(self):
        """Get the data of the node."""
        return self.data
    
    def get_degree(self):
        """Get the degree (number of children) of the node."""
        return len(self.children)
    
    def set_depth(self, depth):
        """Set the depth of the node."""
        self.depth = depth

    def get_depth(self):
        """Get the depth of the node."""
        return self.depth
    
    def set_parent(self, parent):
        """Set the parent of the node."""
        self.parent = parent

    def get_parent(self):
        """Get the parent of the node."""
        return self.parent
    
    def standardized(self):
        """Standardize the node and its children."""
        if not self.is_standarized:
            for child in self.children:
                child.standarize()

            if self.data == "let":
                #Transform LET node to standardized form
                temp1 = self.childern[0].children[1]
                temp1.set_parent(self)
                temp1.set_depth(self.depth + 1)
                temp2 = self.children[1]
                temp2.set_parent(self.children[0])
                temp2.set_depth(self.depth +2)
                self.children[1] = temp1