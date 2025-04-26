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

class ASTFactory:
    """Factory class for creating ASTs."""
    def __init__(self):
        pass

    def get_abstract_syntax_tree(self,data):
        """
        Creating an AST from a string representation.
        
        Args:
            data: The string representation of the AST
            
        Returns:
            AST: The creating AST
        """
        root = NodeFactory.get_node(data[0],0)
        previous_node = root
        current_depth = 0

        for s in data[1:]:
            i = 0
            d = 0

            while s[i] == '.':
                d += 1
                i += 1

            current_node = NodeFactory.get_node(s[i:], d)

            if current_depth < d:
                previous_node.children.append(current_node)
                current_node.set_parent(previous_node)
            else:
                while previous_node.get_depth() !=d :
                    previous_node = previous_node.get_parent()
                previous_node.get_parent().children.append(current_node)
                current_node.set_parent(previous_node.get_parent())

            previous_node = current_node
            current_depth = d
        return AST(root)