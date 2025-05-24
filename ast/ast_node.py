"""
Node classes for RPAL Language AST
Defines the structure and behavior of nodes in the AST.
"""

class Node:
    """Base class for nodes in the AST."""
    def __init__(self):
        # Core node properties
        self.data = None                # The actual data stored in this node (e.g., operator or value)
        self.depth = 0                  # Depth level in the AST (distance from root)
        self.parent = None              # Reference to parent node for tree navigation
        self.children = []              # List of child nodes forming the tree structure
        self.is_standardized = False    # Flag indicating whether standardization has been applied

    def set_data(self, data):
        """Set the data content of the node."""
        self.data = data

    def get_data(self):
        """Get the data content of the node."""
        return self.data

    def get_degree(self):
        """Get the degree (number of children) of the node."""
        return len(self.children)
    
    def get_children(self):
        """Get the list of child nodes."""
        return self.children

    def set_depth(self, depth):
        """Set the depth level of the node in the tree."""
        self.depth = depth

    def get_depth(self):
        """Get the depth level of the node."""
        return self.depth

    def set_parent(self, parent):
        """Set the parent node reference."""
        self.parent = parent

    def get_parent(self):
        """Get the parent node reference."""
        return self.parent

    def standardize(self):
        """
        Standardize the node and its children into a canonical form.
        This process transforms high-level language constructs into a uniform
        functional representation suitable for evaluation.
        """
        # Only standardize if not already done (prevents infinite recursion)
        if not self.is_standardized:
            # First, recursively standardize all children from bottom-up
            for child in self.children:
                child.standardize()

            # Apply transformation rules based on node type
            if self.data == "let":
                # Transform: let x = E in P  →  gamma(lambda x.P, E)
                # This converts let-expressions into function application
                #       LET              GAMMA
                #     /     \           /     \
                #    EQUAL   P   ->   LAMBDA   E
                #   /   \             /    \
                #  X     E           X      P 
                
                # Extract E from the equal node and move it up
                temp1 = self.children[0].children[1]  # E
                temp1.set_parent(self)
                temp1.set_depth(self.depth + 1)
                
                # Move P to become body of lambda
                temp2 = self.children[1]  # P
                temp2.set_parent(self.children[0])
                temp2.set_depth(self.depth + 2)
                
                # Restructure the tree
                self.children[1] = temp1
                self.children[0].set_data("lambda")  # Convert EQUAL to LAMBDA
                self.children[0].children[1] = temp2
                self.set_data("gamma")  # Convert LET to GAMMA (function application)
                
            elif self.data == "where":
                # Transform: P where x = E  →  let x = E in P
                # This converts where-expressions to let-expressions for uniform handling
                #       WHERE               LET
                #       /   \             /     \
                #      P    EQUAL   ->  EQUAL   P
                #           /   \       /   \
                #          X     E     X     E
                
                # Swap P and EQUAL positions
                temp = self.children[0]
                self.children[0] = self.children[1]
                self.children[1] = temp
                self.set_data("let")
                self.standardize()  # Recursively apply let transformation
                
            elif self.data == "function_form":
                # Transform: function definition with multiple parameters
                # f v1 v2 ... vn = E  →  f = lambda v1.(lambda v2.(...(lambda vn.E)...))
                # This creates nested lambda expressions for curried functions
                #       FCN_FORM                EQUAL
                #       /   |   \              /    \
                #      P    V+   E    ->      P     +LAMBDA
                #                                    /     \
                #                                    V     .E
                
                Ex = self.children[-1]  # The expression E
                # Create the first lambda node
                current_lambda = NodeFactory.get_node_with_parent("lambda", self.depth + 1, self, [], True)
                self.children.insert(1, current_lambda)

                # Process each parameter, creating nested lambdas
                i = 2
                while self.children[i] != Ex:
                    V = self.children[i]  # Current parameter
                    self.children.pop(i)
                    V.set_depth(current_lambda.depth + 1)
                    V.set_parent(current_lambda)
                    current_lambda.children.append(V)

                    # Create another lambda if more parameters exist
                    if len(self.children) > 3:
                        current_lambda = NodeFactory.get_node_with_parent("lambda", current_lambda.depth + 1, current_lambda, [], True)
                        current_lambda.get_parent().children.append(current_lambda)

                # Attach the expression to the innermost lambda
                current_lambda.children.append(Ex)
                self.children.pop(2)
                self.set_data("=")  # Convert to simple assignment
                
            elif self.data == "lambda":
                # Transform: lambda with multiple parameters into nested lambdas
                # lambda v1 v2 ... vn.E  →  lambda v1.(lambda v2.(...(lambda vn.E)...))
                # This ensures all lambdas have exactly one parameter
                #     LAMBDA        LAMBDA
                #      /   \   ->   /    \
                #     V++   E      V     .E
                
                if len(self.children) > 2:  # Multiple parameters
                    Ey = self.children[-1]  # The body expression
                    # Create nested lambda structure
                    current_lambda = NodeFactory.get_node_with_parent("lambda", self.depth + 1, self, [], True)
                    self.children.insert(1, current_lambda)

                    # Process each parameter except the first
                    i = 2
                    while self.children[i] != Ey:
                        V = self.children[i]
                        self.children.pop(i)
                        V.set_depth(current_lambda.depth + 1)
                        V.set_parent(current_lambda)
                        current_lambda.children.append(V)

                        # Create deeper nesting if needed
                        if len(self.children) > 3:
                            current_lambda = NodeFactory.get_node_with_parent("lambda", current_lambda.depth + 1, current_lambda, [], True)
                            current_lambda.get_parent().children.append(current_lambda)

                    # Attach body to innermost lambda
                    current_lambda.children.append(Ey)
                    self.children.pop(2)
                    
            elif self.data == "within":
                # Transform: within construct for nested bindings
                # x1 = E1 within x2 = E2  →  x2 = gamma(lambda x1.E2, E1)
                # This allows inner binding to reference outer binding
                #           WITHIN                  EQUAL
                #          /      \                /     \
                #        EQUAL   EQUAL    ->      X2     GAMMA
                #       /    \   /    \                  /    \
                #      X1    E1 X2    E2               LAMBDA  E1
                #                                      /    \
                #                                     X1    E2
                
                # Extract components from both equal nodes
                X1 = self.children[0].children[0]  # Variable from first binding
                X2 = self.children[1].children[0]  # Variable from second binding
                E1 = self.children[0].children[1]  # Expression from first binding
                E2 = self.children[1].children[1]  # Expression from second binding
                
                # Create gamma and lambda nodes for the transformation
                gamma = NodeFactory.get_node_with_parent("gamma", self.depth + 1, self, [], True)
                lambda_ = NodeFactory.get_node_with_parent("lambda", self.depth + 2, gamma, [], True)
                
                # Adjust depths and parents for the restructured tree
                X1.set_depth(X1.get_depth() + 1)
                X1.set_parent(lambda_)
                X2.set_depth(X1.get_depth() - 1)
                X2.set_parent(self)
                E1.set_depth(E1.get_depth())
                E1.set_parent(gamma)
                E2.set_depth(E2.get_depth() + 1)
                E2.set_parent(lambda_)
                
                # Build the new tree structure
                lambda_.children.append(X1)
                lambda_.children.append(E2)
                gamma.children.append(lambda_)
                gamma.children.append(E1)
                self.children.clear()
                self.children.append(X2)
                self.children.append(gamma)
                self.set_data("=")
                
            elif self.data == "@":
                # Transform: infix operator application
                # E1 @ N E2  →  gamma(gamma(N, E1), E2)
                # This converts infix notation to prefix function application
                #         AT              GAMMA
                #       / | \    ->       /    \
                #      E1 N E2          GAMMA   E2
                #                       /    \
                #                      N     E1
                
                # Create nested gamma structure for curried application
                gamma1 = NodeFactory.get_node_with_parent("gamma", self.depth + 1, self, [], True)
                e1 = self.children[0]
                e1.set_depth(e1.get_depth() + 1)
                e1.set_parent(gamma1)
                n = self.children[1]
                n.set_depth(n.get_depth() + 1)
                n.set_parent(gamma1)
                
                # Build inner gamma(N, E1)
                gamma1.children.append(n)
                gamma1.children.append(e1)
                
                # Remove processed children and restructure
                self.children.pop(0)
                self.children.pop(0)
                self.children.insert(0, gamma1)
                self.set_data("gamma")  # Outer gamma application
                
            elif self.data == "and":
                # Transform: simultaneous definitions
                # x1 = E1 and x2 = E2 and ...  →  (x1, x2, ...) = tau(E1, E2, ...)
                # This handles mutually recursive definitions
                #         SIMULTDEF            EQUAL
                #             |               /     \
                #           EQUAL++  ->     COMMA   TAU
                #           /   \             |      |
                #          X     E           X++    E++
                
                # Create comma (tuple) and tau (tuple constructor) nodes
                comma = NodeFactory.get_node_with_parent(",", self.depth + 1, self, [], True)
                tau = NodeFactory.get_node_with_parent("tau", self.depth + 1, self, [], True)

                # Separate variables and expressions from all equal nodes
                for equal in self.children:
                    equal.children[0].set_parent(comma)    # Variable goes to comma
                    equal.children[1].set_parent(tau)      # Expression goes to tau
                    comma.children.append(equal.children[0])
                    tau.children.append(equal.children[1])

                # Replace children with comma and tau
                self.children.clear()
                self.children.append(comma)
                self.children.append(tau)
                self.set_data("=")
                
            elif self.data == "rec":
                # Transform: recursive definition
                # rec x = E  →  x = gamma(Y*, lambda x.E)
                # This uses the Y combinator for recursion
                #        REC                 EQUAL
                #         |                 /     \
                #       EQUAL     ->       X     GAMMA
                #      /     \                   /    \
                #     X       E                YSTAR  LAMBDA
                #                                     /     \
                #                                     X      E
                
                # Extract variable and expression from the recursive definition
                X = self.children[0].children[0]  # Recursive variable
                E = self.children[0].children[1]  # Recursive expression
                
                # Create a copy of X for the left side of assignment
                F = NodeFactory.get_node_with_parent(X.get_data(), self.depth + 1, self, X.children, True)
                
                # Create gamma, Y*, and lambda nodes for fixed-point computation
                G = NodeFactory.get_node_with_parent("gamma", self.depth + 1, self, [], True)
                Y = NodeFactory.get_node_with_parent("<Y*>", self.depth + 2, G, [], True)  # Y combinator
                L = NodeFactory.get_node_with_parent("lambda", self.depth + 2, G, [], True)

                # Adjust depths and parents for lambda body
                X.set_depth(L.depth + 1)
                X.set_parent(L)
                E.set_depth(L.depth + 1)
                E.set_parent(L)
                
                # Build the lambda(X.E) structure
                L.children.append(X)
                L.children.append(E)
                
                # Build gamma(Y*, lambda(X.E))
                G.children.append(Y)
                G.children.append(L)
                
                # Create final assignment: X = gamma(Y*, lambda(X.E))
                self.children.clear()
                self.children.append(F)
                self.children.append(G)
                self.set_data("=")

            # Mark this node as standardized to prevent re-processing
            self.is_standardized = True

class NodeFactory:
    """Factory class for creating nodes with different configurations."""
    def __init__(self):
        pass

    @staticmethod
    def get_node(data, depth):
        """
        Create a basic node with the given data and depth.
        
        Args:
            data: The data content for the node (operator, value, etc.)
            depth: The depth level in the tree (distance from root)
            
        Returns:
            Node: A newly created node with empty children list
        """
        node = Node()
        node.set_data(data)
        node.set_depth(depth)
        node.children = []  # Initialize empty children list
        return node

    @staticmethod
    def get_node_with_parent(data, depth, parent, children, is_standardized):
        """
        Create a fully configured node with all properties set.
        
        Args:
            data: The data content for the node
            depth: The depth level in the tree
            parent: The parent node reference
            children: List of child nodes
            is_standardized: Whether the node is already in standardized form
            
        Returns:
            Node: A fully configured node ready for use
        """
        node = Node()
        node.set_data(data)
        node.set_depth(depth)
        node.set_parent(parent)
        node.children = children
        node.is_standardized = is_standardized
        return node