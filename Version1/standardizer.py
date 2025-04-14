# # standardizer.py
# # Converts AST to Standardized Tree (ST) for RPAL language

# from typing import List, Optional
# from lexer import RPALToken, RPALTokenType
# from parser import NodeType, ASTNode, RPALParser

# # Import the Node class from the provided code
# from node import Node, NodeFactory

# class Standardizer:
#     """
#     Converts a parsed AST to a Standardized Tree (ST) according to RPAL rules
#     """
#     def __init__(self):
#         self.node_factory = NodeFactory()
    
#     def convert_ast_node_to_st_node(self, ast_node: ASTNode, depth: int = 0, parent: Optional[Node] = None) -> Node:
#         """
#         Convert an ASTNode to a standardizable Node
        
#         Args:
#             ast_node: The AST node to convert
#             depth: Current depth in the tree
#             parent: Parent node in the standardized tree
            
#         Returns:
#             A standardizable Node object
#         """
#         # Create a new Node
#         node = self.node_factory.get_node(self._convert_node_type_to_string(ast_node.type, ast_node.value), depth)
#         node.set_parent(parent)
        
#         # Add children recursively
#         for i in range(ast_node.children_count):
#             # Pop a node from the AST stack (assumed to be the next child)
#             child_node = self.ast_nodes.pop(0)
#             child = self.convert_ast_node_to_st_node(child_node, depth + 1, node)
#             node.children.append(child)
            
#         return node
    
#     def _convert_node_type_to_string(self, node_type: NodeType, value: str) -> str:
#         """
#         Convert a NodeType enum to a string representation
        
#         Args:
#             node_type: The NodeType enum value
#             value: The original value string
            
#         Returns:
#             A string representation for the standardizable node
#         """
#         # Map node types to their string representations
#         if node_type == NodeType.LET:
#             return "let"
#         elif node_type == NodeType.FUNCTION_FORM:
#             return "function_form"
#         elif node_type == NodeType.WHERE:
#             return "where"
#         elif node_type == NodeType.GAMMA:
#             return "gamma"
#         elif node_type == NodeType.LAMBDA:
#             return "lambda"
#         elif node_type == NodeType.TAU:
#             return "tau"
#         elif node_type == NodeType.REC:
#             return "rec"
#         elif node_type == NodeType.AUG:
#             return "aug"
#         elif node_type == NodeType.CONDITIONAL:
#             return "->"
#         elif node_type == NodeType.OR:
#             return "or"
#         elif node_type == NodeType.AND:
#             return "&"
#         elif node_type == NodeType.NOT:
#             return "not"
#         elif node_type == NodeType.COMPARE:
#             return value  # gr, ge, ls, le, eq, ne
#         elif node_type == NodeType.PLUS:
#             return "+"
#         elif node_type == NodeType.MINUS:
#             return "-"
#         elif node_type == NodeType.NEG:
#             return "neg"
#         elif node_type == NodeType.MULTIPLY:
#             return "*"
#         elif node_type == NodeType.DIVIDE:
#             return "/"
#         elif node_type == NodeType.POWER:
#             return "**"
#         elif node_type == NodeType.AT:
#             return "@"
#         elif node_type == NodeType.TRUE:
#             return "true"
#         elif node_type == NodeType.FALSE:
#             return "false"
#         elif node_type == NodeType.NIL:
#             return "nil"
#         elif node_type == NodeType.DUMMY:
#             return "dummy"
#         elif node_type == NodeType.WITHIN:
#             return "within"
#         elif node_type == NodeType.AND_DEF:
#             return "and"
#         elif node_type == NodeType.EQUAL:
#             return "="
#         elif node_type == NodeType.COMMA:
#             return ","
#         elif node_type == NodeType.EMPTY_TUPLE:
#             return "()"
#         elif node_type == NodeType.IDENTIFIER:
#             return value  # Return the actual identifier name
#         elif node_type == NodeType.INTEGER:
#             return value  # Return the integer value as string
#         elif node_type == NodeType.STRING:
#             return value  # Return the string value with quotes
#         else:
#             return str(value)  # Default fallback

#     def convert_parser_output_to_st(self, parser: RPALParser) -> Node:
#         """
#         Convert the parser's AST stack to a standardizable tree
        
#         Args:
#             parser: The RPALParser instance with AST nodes
            
#         Returns:
#             Root node of the standardizable tree
#         """
#         # Make a copy of the parser's AST nodes
#         self.ast_nodes = parser.ast.copy()
        
#         if not self.ast_nodes:
#             raise ValueError("Parser has not produced any AST nodes")
        
#         # Start with the root node
#         root_node = self.ast_nodes.pop(0)
#         root = self.convert_ast_node_to_st_node(root_node)
        
#         return root

#     def standardize(self, parser: RPALParser) -> Node:
#         """
#         Convert AST to Standardized Tree
        
#         Args:
#             parser: The RPALParser instance with parsed AST
            
#         Returns:
#             Root node of the standardized tree
#         """
#         # Convert parser output to standardizable tree
#         root = self.convert_parser_output_to_st(parser)
        
#         # Apply standardization to the tree
#         root.standardize()
        
#         return root

# def print_st_tree(node: Node, indent: int = 0) -> List[str]:
#     """
#     Print the standardized tree with proper indentation
    
#     Args:
#         node: The current node to print
#         indent: Current indentation level
        
#     Returns:
#         List of strings representing the standardized tree
#     """
#     result = []
#     dots = "." * indent
    
#     # Print node data with indentation
#     result.append(f"{dots}{node.get_data()}")
    
#     # Print all children recursively
#     for child in node.get_children():
#         result.extend(print_st_tree(child, indent + 1))
    
#     return result



from typing import List, Optional

# Import from your existing modules
from lexer import RPALTokenType
from parser import ASTNode, NodeType

class STNode:
    """
    Node for the Standardized Tree (ST)
    """
    def __init__(self, node_type: NodeType, value: str):
        self.node_type = node_type
        self.value = value
        self.children = []
    
    def add_child(self, child: 'STNode') -> None:
        """Add a child node to this node"""
        self.children.append(child)
    
    def __str__(self) -> str:
        """String representation for debugging"""
        return f"STNode({self.node_type.name}, '{self.value}', {len(self.children)} children)"
    
    def print_st(self, indent: int = 0) -> List[str]:
        """
        Print the ST with proper indentation
        
        Args:
            indent: Current indentation level
            
        Returns:
            List of strings representing the ST
        """
        dots = "." * indent
        result = []
        
        # Print this node
        if self.node_type in [NodeType.IDENTIFIER, NodeType.INTEGER, NodeType.STRING, 
                             NodeType.TRUE, NodeType.FALSE, NodeType.NIL, NodeType.DUMMY]:
            result.append(f"{dots}<{self.node_type.name}:{self.value}>")
        else:
            result.append(f"{dots}{self.value}")
        
        # Print children with increased indentation
        for child in self.children:
            result.extend(child.print_st(indent + 1))
        
        return result

class Standardizer:
    """
    Transforms an AST into a Standardized Tree (ST) by applying standardization rules
    """
    def __init__(self, ast_root: ASTNode):
        """
        Initialize the standardizer with the root of an AST
        
        Args:
            ast_root: Root of the AST to be standardized
        """
        self.ast_root = ast_root
        self.st_root = None
    
    def standardize(self) -> STNode:
        """
        Convert the AST to a standardized tree
        
        Returns:
            The root of the standardized tree
        """
        if not self.ast_root:
            return None
        
        # Start the standardization process
        self.st_root = self._standardize_node(self.ast_root)
        return self.st_root
    
    def _standardize_node(self, ast_node: ASTNode) -> STNode:
        """
        Recursively standardize a node and its children
        
        Args:
            ast_node: Current AST node to standardize
            
        Returns:
            Standardized node corresponding to the AST node
        """
        # Base case: leaf nodes with no transformations needed
        if ast_node.type in [NodeType.IDENTIFIER, NodeType.INTEGER, NodeType.STRING, 
                           NodeType.TRUE, NodeType.FALSE, NodeType.NIL, NodeType.DUMMY]:
            return STNode(ast_node.type, ast_node.value)
        
        # Apply transformation rules based on node type
        # 1. let transformation: let -> gamma(lambda, ...)
        if ast_node.type == NodeType.LET:
            return self._transform_let(ast_node)
            
        # 2. where transformation: where -> let
        elif ast_node.type == NodeType.WHERE:
            return self._transform_where(ast_node)
            
        # 3. function_form transformation
        elif ast_node.type == NodeType.FUNCTION_FORM:
            return self._transform_function_form(ast_node)
            
        # 4. lambda with multiple arguments
        elif ast_node.type == NodeType.LAMBDA:
            return self._transform_lambda(ast_node)
            
        # 5. within transformation
        elif ast_node.type == NodeType.WITHIN:
            return self._transform_within(ast_node)
            
        # 6. @ (application) transformation
        elif ast_node.type == NodeType.AT:
            return self._transform_at(ast_node)
            
        # 7. and transformation
        elif ast_node.type == NodeType.AND_DEF:
            return self._transform_and(ast_node)
            
        # 8. rec transformation
        elif ast_node.type == NodeType.REC:
            return self._transform_rec(ast_node)
            
        # Default: standardize children and add them to this node
        else:
            st_node = STNode(ast_node.type, ast_node.value)
            
            for i in range(ast_node.children_count):
                # Get the i-th child
                child_ast = self._get_ast_child(ast_node, i)
                # Standardize it and add to the ST node
                if child_ast:
                    st_node.add_child(self._standardize_node(child_ast))
            
            return st_node
    
    def _get_ast_child(self, ast_node: ASTNode, index: int) -> Optional[ASTNode]:
        """
        Get the i-th child of an AST node
        
        Args:
            ast_node: Parent AST node
            index: Index of the child to retrieve
            
        Returns:
            The i-th child of ast_node, or None if out of bounds
        """
        # In the actual implementation, this would depend on how children are stored
        # For a flat representation, you might need to traverse the AST structure
        # For now, we'll assume there's a way to get the i-th child
        if index < ast_node.children_count:
            # Mock implementation - this would need to be replaced with actual logic
            # to retrieve the i-th child from your AST representation
            child_index = index  # This is a placeholder
            return ast_node.children[child_index] if hasattr(ast_node, 'children') else None
        return None
    
    # Rule 1: let -> gamma(lambda, ...)
    def _transform_let(self, ast_node: ASTNode) -> STNode:
        """
        Transform 'let' expressions to 'gamma(lambda, ...)'
        let = X E P -> gamma(lambda X P, E)
        
        Args:
            ast_node: Let node to transform
            
        Returns:
            Transformed standardized node
        """
        # Create gamma node
        gamma_node = STNode(NodeType.GAMMA, "gamma")
        
        # Create lambda node
        lambda_node = STNode(NodeType.LAMBDA, "lambda")
        gamma_node.add_child(lambda_node)
        
        # Get definition and expression parts
        definition = self._get_ast_child(ast_node, 0)  # = X E
        expression = self._get_ast_child(ast_node, 1)  # P
        
        # Get variable name and value from definition
        variable = self._get_ast_child(definition, 0)  # X
        value = self._get_ast_child(definition, 1)     # E
        
        # Build the structure: lambda X P
        lambda_node.add_child(self._standardize_node(variable))
        lambda_node.add_child(self._standardize_node(expression))
        
        # Add E to gamma
        gamma_node.add_child(self._standardize_node(value))
        
        return gamma_node
    
    # Rule 2: where -> let
    def _transform_where(self, ast_node: ASTNode) -> STNode:
        """
        Transform 'where' expressions to 'let'
        where P = X E -> let = X E P
        
        Args:
            ast_node: Where node to transform
            
        Returns:
            Transformed standardized node
        """
        # Get parts of where expression
        expression = self._get_ast_child(ast_node, 0)  # P
        definition = self._get_ast_child(ast_node, 1)  # = X E
        
        # Create let node
        let_node = STNode(NodeType.LET, "let")
        
        # Add definition and expression to let
        let_node.add_child(self._standardize_node(definition))
        let_node.add_child(self._standardize_node(expression))
        
        # Now transform the let node (since we've effectively created a let)
        return self._transform_let(let_node)
    
    # Rule 3: function_form -> = (lambda ...)
    def _transform_function_form(self, ast_node: ASTNode) -> STNode:
        """
        Transform function forms to 'lambda' expressions
        function_form P V1 V2 ... E -> = P lambda V1 lambda V2 ... E
        
        Args:
            ast_node: Function form node to transform
            
        Returns:
            Transformed standardized node
        """
        # Create equal node
        equal_node = STNode(NodeType.EQUAL, "=")
        
        # Get function name
        function_name = self._get_ast_child(ast_node, 0)  # P
        equal_node.add_child(self._standardize_node(function_name))
        
        # Get parameters and body
        parameters = []
        for i in range(1, ast_node.children_count - 1):
            parameters.append(self._get_ast_child(ast_node, i))  # V1, V2, ...
        
        body = self._get_ast_child(ast_node, ast_node.children_count - 1)  # E
        
        # Build nested lambdas
        current_lambda = None
        prev_lambda = None
        
        # Start from the innermost lambda and work outward
        for i in range(len(parameters) - 1, -1, -1):
            current_lambda = STNode(NodeType.LAMBDA, "lambda")
            current_lambda.add_child(self._standardize_node(parameters[i]))
            
            if prev_lambda:
                current_lambda.add_child(prev_lambda)
            else:
                # For the innermost lambda, add the body
                current_lambda.add_child(self._standardize_node(body))
            
            prev_lambda = current_lambda
        
        equal_node.add_child(current_lambda)
        return equal_node
    
    # Rule 4: lambda with multiple arguments -> nested lambda
    def _transform_lambda(self, ast_node: ASTNode) -> STNode:
        """
        Transform multi-argument lambdas to nested single-argument lambdas
        lambda V1 V2 ... E -> lambda V1 lambda V2 ... E
        
        Args:
            ast_node: Lambda node to transform
            
        Returns:
            Transformed standardized node
        """
        # If there's only one parameter, no transformation needed
        if ast_node.children_count == 2:
            lambda_node = STNode(NodeType.LAMBDA, "lambda")
            lambda_node.add_child(self._standardize_node(self._get_ast_child(ast_node, 0)))
            lambda_node.add_child(self._standardize_node(self._get_ast_child(ast_node, 1)))
            return lambda_node
        
        # Get parameters and body
        parameters = []
        for i in range(ast_node.children_count - 1):
            parameters.append(self._get_ast_child(ast_node, i))
        
        body = self._get_ast_child(ast_node, ast_node.children_count - 1)
        
        # Build nested lambdas
        current_lambda = None
        prev_lambda = None
        
        # Start from the innermost lambda and work outward
        for i in range(len(parameters) - 1, -1, -1):
            current_lambda = STNode(NodeType.LAMBDA, "lambda")
            current_lambda.add_child(self._standardize_node(parameters[i]))
            
            if prev_lambda:
                current_lambda.add_child(prev_lambda)
            else:
                # For the innermost lambda, add the body
                current_lambda.add_child(self._standardize_node(body))
            
            prev_lambda = current_lambda
        
        return current_lambda
    
    # Rule 5: within -> nested gamma(lambda(...))
    def _transform_within(self, ast_node: ASTNode) -> STNode:
        """
        Transform 'within' expressions
        within = X1 E1 = X2 E2 -> = X2 gamma lambda X1 E2 E1
        
        Args:
            ast_node: Within node to transform
            
        Returns:
            Transformed standardized node
        """
        # Get outer and inner definitions
        outer_def = self._get_ast_child(ast_node, 0)  # = X1 E1
        inner_def = self._get_ast_child(ast_node, 1)  # = X2 E2
        
        # Get components
        outer_var = self._get_ast_child(outer_def, 0)  # X1
        outer_val = self._get_ast_child(outer_def, 1)  # E1
        inner_var = self._get_ast_child(inner_def, 0)  # X2
        inner_val = self._get_ast_child(inner_def, 1)  # E2
        
        # Create equal node
        equal_node = STNode(NodeType.EQUAL, "=")
        equal_node.add_child(self._standardize_node(inner_var))  # X2
        
        # Create gamma node
        gamma_node = STNode(NodeType.GAMMA, "gamma")
        equal_node.add_child(gamma_node)
        
        # Create lambda node
        lambda_node = STNode(NodeType.LAMBDA, "lambda")
        gamma_node.add_child(lambda_node)
        
        # Add X1 and E2 to lambda
        lambda_node.add_child(self._standardize_node(outer_var))  # X1
        lambda_node.add_child(self._standardize_node(inner_val))  # E2
        
        # Add E1 to gamma
        gamma_node.add_child(self._standardize_node(outer_val))  # E1
        
        return equal_node
    
    # Rule 6: @ (application) -> nested gamma
    def _transform_at(self, ast_node: ASTNode) -> STNode:
        """
        Transform @ expressions to nested gamma
        @ E1 N E2 -> gamma gamma N E1 E2
        
        Args:
            ast_node: At node to transform
            
        Returns:
            Transformed standardized node
        """
        # Get components
        e1 = self._get_ast_child(ast_node, 0)  # E1
        n = self._get_ast_child(ast_node, 1)   # N
        e2 = self._get_ast_child(ast_node, 2)  # E2
        
        # Create outer gamma node
        outer_gamma = STNode(NodeType.GAMMA, "gamma")
        
        # Create inner gamma node
        inner_gamma = STNode(NodeType.GAMMA, "gamma")
        outer_gamma.add_child(inner_gamma)
        
        # Add N and E1 to inner gamma
        inner_gamma.add_child(self._standardize_node(n))   # N
        inner_gamma.add_child(self._standardize_node(e1))  # E1
        
        # Add E2 to outer gamma
        outer_gamma.add_child(self._standardize_node(e2))  # E2
        
        return outer_gamma
    
    # Rule 7: and -> = (, tau)
    def _transform_and(self, ast_node: ASTNode) -> STNode:
        """
        Transform 'and' definitions
        and = X1 E1 = X2 E2 ... -> = , X1 X2 ... tau E1 E2 ...
        
        Args:
            ast_node: And node to transform
            
        Returns:
            Transformed standardized node
        """
        # Create equal node
        equal_node = STNode(NodeType.EQUAL, "=")
        
        # Create comma node for variables
        comma_node = STNode(NodeType.COMMA, ",")
        equal_node.add_child(comma_node)
        
        # Create tau node for values
        tau_node = STNode(NodeType.TAU, "tau")
        equal_node.add_child(tau_node)
        
        # Process each definition
        for i in range(ast_node.children_count):
            definition = self._get_ast_child(ast_node, i)  # = Xi Ei
            variable = self._get_ast_child(definition, 0)  # Xi
            value = self._get_ast_child(definition, 1)     # Ei
            
            # Add variable to comma node
            comma_node.add_child(self._standardize_node(variable))
            
            # Add value to tau node
            tau_node.add_child(self._standardize_node(value))
        
        return equal_node
    
    # Rule 8: rec -> = X gamma <Y*> lambda(X E)
    def _transform_rec(self, ast_node: ASTNode) -> STNode:
        """
        Transform recursive definitions
        rec = X E -> = X gamma <Y*> lambda X E
        
        Args:
            ast_node: Rec node to transform
            
        Returns:
            Transformed standardized node
        """
        # Get definition
        definition = self._get_ast_child(ast_node, 0)  # = X E
        
        # Get variable and value
        variable = self._get_ast_child(definition, 0)  # X
        value = self._get_ast_child(definition, 1)     # E
        
        # Create equal node
        equal_node = STNode(NodeType.EQUAL, "=")
        equal_node.add_child(self._standardize_node(variable))  # X
        
        # Create gamma node
        gamma_node = STNode(NodeType.GAMMA, "gamma")
        equal_node.add_child(gamma_node)
        
        # Create Y* node (representing the fixed-point combinator)
        y_node = STNode(NodeType.IDENTIFIER, "<Y*>")
        gamma_node.add_child(y_node)
        
        # Create lambda node
        lambda_node = STNode(NodeType.LAMBDA, "lambda")
        gamma_node.add_child(lambda_node)
        
        # Add X and E to lambda
        lambda_node.add_child(self._standardize_node(variable))  # X
        lambda_node.add_child(self._standardize_node(value))     # E
        
        return equal_node
    
    def print_st(self) -> List[str]:
        """
        Print the standardized tree
        
        Returns:
            List of strings representing the standardized tree
        """
        if not self.st_root:
            return []
        
        return self.st_root.print_st()

# Function to standardize an AST
def standardize_ast(ast_root: ASTNode) -> STNode:
    """
    Standardize an Abstract Syntax Tree
    
    Args:
        ast_root: Root node of the AST
        
    Returns:
        Root node of the standardized tree
    """
    standardizer = Standardizer(ast_root)
    return standardizer.standardize()