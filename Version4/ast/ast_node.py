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
                # P where X = E   ->   let X = E in P
                #       WHERE               LET
                #       /   \             /     \
                #      P    EQUAL   ->  EQUAL   P
                #           /   \       /   \
                #          X     E     X     E

                temp = self.children[0]
                self.children[0] = self.children[1]
                self.children[1] = temp
                self.set_data("let")
                self.standardize()

            elif self.data == "fcn_form":

                #       FCN_FORM                EQUAL
                #       /   |   \              /    \
                #      P    V+   E    ->      P     +LAMBDA
                #                                    /     \
                #                                    V     .
                Ex = self.children[-1]
                current_lambda = NodeFactory.get_node_with_parent("lambda", self.depth + 1, self, [], True)
                self.children.insert(1,current_lambda)

                i = 2
                while self.children[i] != Ex:
                    V = self.children[i]
                    self.children.pop(i)
                    V.set_depth(current_lambda.depth + 1)
                    V.set_parent(current_lambda)
                    current_lambda.children.append(V)

                    if len(self.children) > 3:
                        current_lambda = NodeFactory.get_node_with_parent("lambda", current_lambda.depth + 1, current_lambda, [], True)
                        current_lambda.get_parent().children.append(current_lambda)

                current_lambda.children.append(Ex)
                self.children.pop(2)
                self.set_data("=")

            elif self.data == "lambda":

                #     LAMBDA        LAMBDA
                #      /   \   ->   /    \
                #     V++   E      V     .E

                if len(self.children) > 2:
                    Ey = self.children[-1]
                    Ey = self.children[-1]
                    current_lambda = NodeFactory.get_node_with_parent("lambda", self.depth + 1, self, [], True)
                    current_lambda = NodeFactory.get_node_with_parent("lambda", self.depth + 1, self, [], True)
                    self.children.insert(1, current_lambda)

                    i = 2
                    while self.children[i] != Ey:
                        V = self.children[i]
                        self.children.pop(i)
                        V.set_depth(current_lambda.depth + 1)
                        V.set_parent(current_lambda)
                        current_lambda.children.append(V)

                        if len(self.children) > 3:
                            current_lambda = NodeFactory.get_node_with_parent("lambda", current_lambda.depth + 1, current_lambda, [], True)
                            current_lambda.get_parent().children.append(current_lambda)

                    current_lambda.children.append(Ey)
                    self.children.pop(2)

            elif self.data == "within":

               #           WITHIN                  EQUAL
                #          /      \                /     \
                #        EQUAL   EQUAL    ->      X2     GAMMA
                #       /    \   /    \                  /    \
                #      X1    E1 X2    E2               LAMBDA  E1
                #                                      /    \
                #                                     X1    E2
                
                X1 = self.children[0].children[0]
                X2 = self.children[1].children[0]
                E1 = self.children[0].children[1]
                E2 = self.children[1].children[1]
                gamma = NodeFactory.get_node_with_parent("gamma", self.depth + 1, self, [], True)
                lambda_ = NodeFactory.get_node_with_parent("lambda", self.depth + 2, gamma, [], True)
                X1.set_depth(X1.get_depth() + 1)
                X1.set_parent(lambda_)
                X2.set_depth(X1.get_depth() - 1)
                X2.set_parent(self)
                E1.set_depth(E1.get_depth() + 1)
                E1.set_parent(gamma)
                E2.set_depth(X1.get_depth() + 1)
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
                
                #         @              GAMMA
                #       / | \    ->       /    \
                #      E1 N E2          GAMMA   E2
                #                       /    \
                #                      N     E1
                
                gamma1 = NodeFactory.get_node_with_parent("gamma", self.depth + 1, self, [], True)
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
                
                #            and                 =
                #             |               /     \
                #            =++  ->          ,     TAU
                #           /   \             |      |
                #          X     E           X++    E++
                
                comma = NodeFactory.get_node_with_parent(",", self.depth + 1, self, [], True)
                tau = NodeFactory.get_node_with_parent("tau", self.depth + 1, self, [], True)

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
                
                #        REC                   =
                #         |                 /     \
                #         =        ->       X     GAMMA
                #      /     \                   /    \
                #     X       E                Y*   LAMBDA
                #                                     /     \
                #                                     X      E
                
                X = self.children[0].children[0]
                E = self.children[0].children[1]
                F = NodeFactory.get_node_with_parent(X.get_data(), self.depth + 1, self, X.children, True)
                G = NodeFactory.get_node_with_parent("gamma", self.depth + 1, self, [], True)
                Y = NodeFactory.get_node_with_parent("<Y*>", self.depth + 2, G, [], True)
                L = NodeFactory.get_node_with_parent("lambda", self.depth + 2, G, [], True)

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

class  NodeFactory:
    """Factory class for creating nodes."""
    def __init__(self):
        pass

    @staticmethod
    def get_node(data, depth):
        """
        Create aa node with the given data and depth.
        
        Args:
            data: The node for the node
            depth: the depth of the node
            
        Returns:
            Node: The created node
        """

        node = Node()
        node.set_data(data)
        node.set_depth(depth)
        node.children = []
        return node
    
    @staticmethod
    def get_node_with_parent(data, depth, parent, children, is_standarized):
        """
        Create a node with the given data, depth, parent, children, and standarization status.
        
        Args:
            data: The data for the node 
            depth: The depth of the node
            parent: The parent of the node
            children: The children of the node
            is_staandarized: Whether the node is standarized
            
        Returns:
            Node: The created node
        """

        node = Node()
        node.set_data(data)
        node.set_data(depth)
        node.set_parent(parent)
        node.children = children
        node.is_standardized = is_standarized
        return node