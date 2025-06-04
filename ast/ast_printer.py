"""
Abstract Syntax Tree (AST) for RPAL Language
Represents the structure of an RPAL program.
"""

from ast.ast_node import Node, NodeFactory

class AST:
    """Class representing an Abstract Syntax Tree."""
    def __init__(self, root=None):
        # Initialize the AST with an optional root node
        self.root = root

    def set_root(self, root):
        """Set the root node of the AST."""
        self.root = root

    def get_root(self):
        """Get the root node of the AST."""
        return self.root

    def standardize(self):
        """Standardize the AST."""
        if not self.root.is_standardized:
            self.root.standardize()

    def pre_order_traverse(self, node, i):
        """
        Traverse the AST in pre-order.
        
        Args:
            node: The current node
            i: The current indentation level
        """
        

        print("." * i + str(node.get_data())) # Print the current node's data with indentation
        for child in node.children:
            self.pre_order_traverse(child, i + 1) # Recursively traverse child nodes

    def print_ast(self):
        """Print the AST."""
        self.pre_order_traverse(self.get_root(), 0)

class ASTFactory:
    """Factory class for creating ASTs."""
    def __init__(self):
        pass # No special initialization needed

    def get_abstract_syntax_tree(self, data):
        """
        Create an AST from a string representation.
        
        Args:
            data: The string representation of the AST
            
        Returns:
            AST: The created AST
        """
        root = NodeFactory.get_node(data[0], 0)  # Create the root node
        previous_node = root  # Initialize the previous node as the root
        current_depth = 0  # Initialize the current depth as 0

        for s in data[1:]:
            i = 0  # index of word
            d = 0  # depth of node

            # Count the number of leading dots to determine the depth
            while s[i] == '.':
                d += 1
                i += 1

            # Create the current node using the remaining string (after dots)
            current_node = NodeFactory.get_node(s[i:], d)  # Create the current node

            if current_depth < d:
                 # If we go deeper, current node is a child of previous node
                previous_node.children.append(current_node)  # Add current node as a child of previous node
                current_node.set_parent(previous_node)  
            else:
                 # If we stay at the same level or go up, move up to the correct parent
                while previous_node.get_depth() != d:
                    previous_node = previous_node.get_parent()  # Traverse up the tree until reaching the node at depth d
                 # Add the current node as a sibling under the correct parent
                previous_node.get_parent().children.append(current_node)  
                current_node.set_parent(previous_node.get_parent())  

            previous_node = current_node   # Update previous node
            current_depth = d  # Update current depth
        return AST(root) # Return the constructed AST