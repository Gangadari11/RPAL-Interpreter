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

    def get_children(self):
        """Get the children of the node."""
        return self.children
    
    def set_depth(self,depth):
        """Set the depth of the node."""
        self.depth = depth

    def get_depth(self):
        """Get the depth of the node."""
        return self.depth

    def set_parent(self,parent):
        """Set the parent of the node."""
        self.parent = parent

    def get_parent(self):
        """Get the parent of the node."""
        return self.parent 

    def standardize(self):
        """
        Standarize the node and its children into a core form used for evaluation.
        This transforms constructs into a more uniform and functional structure.
        """
        if not self.is_standardized:
            for children in self.children:
                child.standardize()

            # Transformation rules for various language constructs
            if self.data == "let":
                #letx = E in P -> gamma(lamda X. P, E)
                # Standardize LET node
                #       LET              GAMMA
                #     /     \           /     \
                #    EQUAL   P   ->   LAMBDA   E
                #   /   \             /    \
                #  X     E           X      P 
                temp1 = self.children[0].children[1]
                temp1.set_parent(self)
                temp1.set_depth(self.depth + 1)
                temp2 = self.children[1]
                temp2.set_parent(self.children[0])
                temp2.set_depth(self.depth + 2)
                self.children[1] = temp1
                self.children[0].set_data("lambda")
                self.children[0].children[1] = temp2
                self.set_data("gamma")

            elif self.data == "where":
                # 
