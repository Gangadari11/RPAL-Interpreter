"""
AST Factory for RPAL Language
Creates an AST from a string representation.
"""

from ast.node import NodeFactory
from ast.ast import AST

class ASTFactory:
    """Factory class for creating ASTs."""
    def __init__(self):
        pass

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

            while s[i] == '.':
                d += 1
                i += 1

            current_node = NodeFactory.get_node(s[i:], d)  # Create the current node

            if current_depth < d:
                previous_node.children.append(current_node)  # Add current node as a child of previous node
                current_node.set_parent(previous_node)  
            else:
                while previous_node.get_depth() != d:
                    previous_node = previous_node.get_parent()  # Traverse up the tree until reaching the node at depth d
                previous_node.get_parent().children.append(current_node)  
                current_node.set_parent(previous_node.get_parent())  

            previous_node = current_node  
            current_depth = d  
        return AST(root)
