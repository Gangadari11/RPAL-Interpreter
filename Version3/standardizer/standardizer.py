"""
Combined implementation for RPAL Language AST
Defines the structure, behavior, creation and traversal of an Abstract Syntax Tree
"""

class Node:
    """Base class for nodes in the AST."""
    def __init__(self):
        self.data = None
        self.depth = 0
        self.parent = None
        self.children = []
        self.is_standardized = False

    def set_data(self, data):
        """Set the data of the node."""
        self.data = data

    def get_data(self):
        """Get the data of the node."""
        return self.data

    def get_degree(self):
        """Get the degree (number of children) of the node."""
        return len(self.children)
    
    def get_children(self):
        """Get the children of the node."""
        return self.children

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

    def standardize(self):
        """Standardize the node and its children."""
        if not self.is_standardized:
            for child in self.children:
                child.standardize()

            if self.data == "let":
                # Transform LET node to standardized form
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
                # Transform WHERE node to standardized form
                temp = self.children[0]
                self.children[0] = self.children[1]
                self.children[1] = temp
                self.set_data("let")
                self.standardize()
            elif self.data == "function_form":
                # Transform function_form node to standardized form
                Ex = self.children[-1]
                current_lambda = NodeUtility.create_extended_node("lambda", self.depth + 1, self, [], True)
                self.children.insert(1, current_lambda)

                i = 2
                while self.children[i] != Ex:
                    V = self.children[i]
                    self.children.pop(i)
                    V.set_depth(current_lambda.depth + 1)
                    V.set_parent(current_lambda)
                    current_lambda.children.append(V)

                    if len(self.children) > 3:
                        current_lambda = NodeUtility.create_extended_node("lambda", current_lambda.depth + 1, current_lambda, [], True)
                        current_lambda.get_parent().children.append(current_lambda)

                current_lambda.children.append(Ex)
                self.children.pop(2)
                self.set_data("=")
            elif self.data == "lambda":
                # Transform LAMBDA node with multiple variables to standardized form
                if len(self.children) > 2:
                    Ey = self.children[-1]
                    current_lambda = NodeUtility.create_extended_node("lambda", self.depth + 1, self, [], True)
                    self.children.insert(1, current_lambda)

                    i = 2
                    while self.children[i] != Ey:
                        V = self.children[i]
                        self.children.pop(i)
                        V.set_depth(current_lambda.depth + 1)
                        V.set_parent(current_lambda)
                        current_lambda.children.append(V)

                        if len(self.children) > 3:
                            current_lambda = NodeUtility.create_extended_node("lambda", current_lambda.depth + 1, current_lambda, [], True)
                            current_lambda.get_parent().children.append(current_lambda)

                    current_lambda.children.append(Ey)
                    self.children.pop(2)
            elif self.data == "within":
                # Transform WITHIN node to standardized form
                X1 = self.children[0].children[0]
                X2 = self.children[1].children[0]
                E1 = self.children[0].children[1]
                E2 = self.children[1].children[1]
                gamma = NodeUtility.create_extended_node("gamma", self.depth + 1, self, [], True)
                lambda_ = NodeUtility.create_extended_node("lambda", self.depth + 2, gamma, [], True)
                X1.set_depth(X1.get_depth() + 1)
                X1.set_parent(lambda_)
                X2.set_depth(X1.get_depth() - 1)
                X2.set_parent(self)
                E1.set_depth(E1.get_depth())
                E1.set_parent(gamma)
                E2.set_depth(E2.get_depth() + 1)
                E2.set_parent(lambda_)
                lambda_.children.append(X1)
                lambda_.children.append(E2)
                gamma.children.append(lambda_)
                gamma.children.append(E1)
                self.children.clear()
                self.children.append(X2)
                self.children.append(gamma)
                self.set_data("=")
            elif self.data == "@":
                # Transform AT node to standardized form
                gamma1 = NodeUtility.create_extended_node("gamma", self.depth + 1, self, [], True)
                e1 = self.children[0]
                e1.set_depth(e1.get_depth() + 1)
                e1.set_parent(gamma1)
                n = self.children[1]
                n.set_depth(n.get_depth() + 1)
                n.set_parent(gamma1)
                gamma1.children.append(n)
                gamma1.children.append(e1)
                self.children.pop(0)
                self.children.pop(0)
                self.children.insert(0, gamma1)
                self.set_data("gamma")
            elif self.data == "and":
                # Transform AND node to standardized form
                comma = NodeUtility.create_extended_node(",", self.depth + 1, self, [], True)
                tau = NodeUtility.create_extended_node("tau", self.depth + 1, self, [], True)

                for equal in self.children:
                    equal.children[0].set_parent(comma)
                    equal.children[1].set_parent(tau)
                    comma.children.append(equal.children[0])
                    tau.children.append(equal.children[1])

                self.children.clear()
                self.children.append(comma)
                self.children.append(tau)
                self.set_data("=")
            elif self.data == "rec":
                # Transform REC node to standardized form
                X = self.children[0].children[0]
                E = self.children[0].children[1]
                F = NodeUtility.create_extended_node(X.get_data(), self.depth + 1, self, X.children, True)
                G = NodeUtility.create_extended_node("gamma", self.depth + 1, self, [], True)
                Y = NodeUtility.create_extended_node("<Y*>", self.depth + 2, G, [], True)
                L = NodeUtility.create_extended_node("lambda", self.depth + 2, G, [], True)

                X.set_depth(L.depth + 1)
                X.set_parent(L)
                E.set_depth(L.depth + 1)
                E.set_parent(L)
                L.children.append(X)
                L.children.append(E)
                G.children.append(Y)
                G.children.append(L)
                self.children.clear()
                self.children.append(F)
                self.children.append(G)
                self.set_data("=")

            self.is_standardized = True


class NodeUtility:
    """Utility class for creating nodes."""
    
    @staticmethod
    def create_basic_node(data, depth):
        """
        Create a node with the given data and depth.
        
        Args:
            data: The data for the node
            depth: The depth of the node
            
        Returns:
            Node: The created node
        """
        node = Node()
        node.set_data(data)
        node.set_depth(depth)
        node.children = []
        return node

    @staticmethod
    def create_extended_node(data, depth, parent, children, is_standardized):
        """
        Create a node with the given data, depth, parent, children, and standardization status.
        
        Args:
            data: The data for the node
            depth: The depth of the node
            parent: The parent of the node
            children: The children of the node
            is_standardized: Whether the node is standardized
            
        Returns:
            Node: The created node
        """
        node = Node()
        node.set_data(data)
        node.set_depth(depth)
        node.set_parent(parent)
        node.children = children
        node.is_standardized = is_standardized
        return node


class SyntaxTree:
    """Class representing an Abstract Syntax Tree."""
    
    def __init__(self, root=None):
        self.root = root
    
    def set_root(self, root):
        """Set the root node of the tree."""
        self.root = root
    
    def get_root(self):
        """Get the root node of the tree."""
        return self.root
    
    def standardize(self):
        """Standardize the tree."""
        if not self.root.is_standardized:
            self.root.standardize()
    
    def traverse_preorder(self, node, indent_level):
        """
        Traverse the tree in pre-order.
        
        Args:
            node: The current node
            indent_level: The current indentation level
        """
        print("." * indent_level + str(node.get_data()))
        for child in node.children:
            self.traverse_preorder(child, indent_level + 1)
    
    def display(self):
        """Display the tree."""
        self.traverse_preorder(self.get_root(), 0)


class TreeBuilder:
    """Builder class for creating syntax trees."""
    
    def __init__(self):
        pass
    
    def build_syntax_tree(self, input_data):
        """
        Create a syntax tree from a string representation.
        
        Args:
            input_data: The string representation of the tree
            
        Returns:
            SyntaxTree: The created tree
        """
        root = NodeUtility.create_basic_node(input_data[0], 0)  # Create the root node
        prev = root  # Initialize the previous node as the root
        curr_depth = 0  # Initialize the current depth as 0
        
        for element in input_data[1:]:
            pos = 0  # Position in the current string
            node_depth = 0  # Depth of the current node
            
            # Count dots to determine depth
            while pos < len(element) and element[pos] == '.':
                node_depth += 1
                pos += 1
            
            # Create the current node with the actual text (after dots)
            curr_node = NodeUtility.create_basic_node(element[pos:], node_depth)
            
            # If we're going deeper in the tree
            if curr_depth < node_depth:
                # Add current node as a child of previous node
                prev.children.append(curr_node)
                curr_node.set_parent(prev)
            else:
                # We need to go back up the tree to find the right parent
                while prev.get_depth() != node_depth:
                    prev = prev.get_parent()
                # Add the current node as a sibling to the previous node
                prev.get_parent().children.append(curr_node)  
                curr_node.set_parent(prev.get_parent())
            
            # Update the previous node and current depth
            prev = curr_node
            curr_depth = node_depth
        
        # Return a new syntax tree with the constructed root
        return SyntaxTree(root)