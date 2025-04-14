from enum import Enum
from typing import List, Optional

# Import your lexer classes
from lexer import RPALTokenType, RPALToken

class NodeType(Enum):
    """
    Enumeration of all possible AST node types for RPAL language
    """
    LET = 1            # let expressions
    FUNCTION_FORM = 2  # function definitions
    IDENTIFIER = 3     # variable names
    INTEGER = 4        # integer literals
    STRING = 5         # string literals
    WHERE = 6          # where expressions
    GAMMA = 7          # function application
    LAMBDA = 8         # lambda expressions
    TAU = 9            # tuple constructor
    REC = 10           # recursive definitions
    AUG = 11           # augmentation
    CONDITIONAL = 12   # conditional expressions
    OR = 13            # logical OR
    AND = 14           # logical AND
    NOT = 15           # logical NOT
    COMPARE = 16       # comparison operators (gr, ge, ls, le, eq, ne)
    PLUS = 17          # addition
    MINUS = 18         # subtraction
    NEG = 19           # unary negation
    MULTIPLY = 20      # multiplication
    DIVIDE = 21        # division
    POWER = 22         # exponentiation
    AT = 23            # at operator
    TRUE = 24          # boolean true
    FALSE = 25         # boolean false
    NIL = 26           # nil value
    DUMMY = 27         # dummy placeholder
    WITHIN = 28        # within definitions
    AND_DEF = 29       # and in definitions
    EQUAL = 30         # equality in definitions
    COMMA = 31         # comma-separated list
    EMPTY_TUPLE = 32   # empty tuple

class ASTNode:
    """
    Represents a node in the Abstract Syntax Tree
    """
    def __init__(self, node_type: NodeType, value: str, children_count: int):
        """
        Initialize a new AST node
        
        Args:
            node_type: Type of this node from NodeType enum
            value: String value of this node
            children_count: Number of children this node has
        """
        self.type = node_type
        self.value = value
        self.children_count = children_count
    
    def __str__(self):
        """Return a string representation of the node for debugging"""
        return f"Node({self.type.name}, '{self.value}', children={self.children_count})"
    
    def __repr__(self):
        """Return a formal representation of the node"""
        return self.__str__()

class RPALParser:
    """
    Parser for RPAL language that builds an Abstract Syntax Tree (AST)
    """
    def __init__(self, tokens: List[RPALToken]):
        """
        Initialize the parser with a list of tokens
        
        Args:
            tokens: List of tokens from the lexical analyzer
        """
        self.tokens = tokens.copy()  # Make a copy to avoid modifying the original
        self.ast = []  # Stack used to build the AST
        self.string_ast = []  # String representation of the AST
    
    def parse(self) -> List[ASTNode]:
        """
        Parse the tokens and build an AST
        
        Returns:
            The built Abstract Syntax Tree as a list of nodes
        """
        # Add an end-of-tokens marker
        self.tokens.append(RPALToken(RPALTokenType.EOF, "EOF"))
        
        # Start parsing from the entry point
        self.E()
        
        # Check if we consumed all tokens
        if self.tokens[0].token_type == RPALTokenType.EOF:
            return self.ast
        else:
            print("Error: Parsing incomplete. Remaining tokens:")
            for token in self.tokens:
                print(f"<{token.token_type.name}, '{token.value}'>")
            return None
    
    def convert_ast_to_string(self) -> List[str]:
        """
        Convert the AST to a string representation
        
        Returns:
            A list of strings representing the AST
        """
        dots = ""  # Indentation dots
        stack = []  # Stack for managing nodes during traversal
        
        # While there are nodes in the AST
        while self.ast:
            if not stack:
                # If stack is empty, process the next node from AST
                if self.ast[-1].children_count == 0:
                    # For leaf nodes, add them directly to string representation
                    self.add_to_string_ast(dots, self.ast.pop())
                else:
                    # For non-leaf nodes, push to stack for further processing
                    node = self.ast.pop()
                    stack.append(node)
            else:
                if self.ast[-1].children_count > 0:
                    # If next AST node has children, push to stack and increase indentation
                    node = self.ast.pop()
                    stack.append(node)
                    dots += "."
                else:
                    # For leaf nodes, add to stack, increase indentation
                    stack.append(self.ast.pop())
                    dots += "."
                    
                    # Process completed subtrees
                    while stack[-1].children_count == 0:
                        self.add_to_string_ast(dots, stack.pop())
                        if not stack:
                            break
                        dots = dots[:-1]  # Decrease indentation
                        node = stack.pop()
                        node.children_count -= 1  # Decrement children count
                        stack.append(node)
        
        # Reverse the list to get correct order
        self.string_ast.reverse()
        return self.string_ast
    
    def add_to_string_ast(self, dots: str, node: ASTNode) -> None:
        """
        Add a node's string representation to the string AST
        
        Args:
            dots: Current indentation string
            node: Node to add to the string AST
        """
        # Special handling for leaf nodes with values
        if node.type in [NodeType.IDENTIFIER, NodeType.INTEGER, NodeType.STRING, 
                         NodeType.TRUE, NodeType.FALSE, NodeType.NIL, NodeType.DUMMY]:
            self.string_ast.append(f"{dots}<{node.type.name}:{node.value}>")
        # Special handling for function forms
        elif node.type == NodeType.FUNCTION_FORM:
            self.string_ast.append(f"{dots}function_form")
        # Default handling for other node types
        else:
            self.string_ast.append(f"{dots}{node.value}")
    
    # Grammar rule implementations follow
    # Each method implements a non-terminal in the RPAL grammar
    
    def E(self) -> None:
        """
        Parse E -> 'let' D 'in' E | 'fn' Vb+ '.' E | Ew
        """
        # Check if tokens are available
        if not self.tokens:
            print("Error: Unexpected end of tokens in E")
            return
        
        token = self.tokens[0]
        
        # Handle let expressions
        if token.token_type == RPALTokenType.KEYWORD and token.value == "let":
            self.tokens.pop(0)  # Consume 'let'
            self.D()  # Parse definition
            
            # Expect 'in' keyword
            if not self.tokens or self.tokens[0].value != "in":
                print("Error: Expected 'in' in let expression")
                return
            
            self.tokens.pop(0)  # Consume 'in'
            self.E()  # Parse expression
            
            # Add let node to AST with 2 children (definition and expression)
            self.ast.append(ASTNode(NodeType.LET, "let", 2))
        
        # Handle lambda expressions
        elif token.token_type == RPALTokenType.KEYWORD and token.value == "fn":
            self.tokens.pop(0)  # Consume 'fn'
            
            # Count parameters
            param_count = 0
            while self.tokens and (self.tokens[0].token_type == RPALTokenType.IDENTIFIER or 
                                   (self.tokens[0].token_type == RPALTokenType.LPAREN)):
                self.Vb()  # Parse parameter
                param_count += 1
            
            # Expect '.' after parameters
            if not self.tokens or self.tokens[0].value != ".":
                print("Error: Expected '.' after lambda parameters")
                return
            
            self.tokens.pop(0)  # Consume '.'
            self.E()  # Parse body expression
            
            # Add lambda node to AST with param_count + 1 children
            self.ast.append(ASTNode(NodeType.LAMBDA, "lambda", param_count + 1))
        
        # Handle other expressions
        else:
            self.Ew()
    
    def Ew(self) -> None:
        """
        Parse Ew -> T 'where' Dr | T
        """
        self.T()  # Parse tuple expression
        
        # Check for 'where' clause
        if self.tokens and self.tokens[0].value == "where":
            self.tokens.pop(0)  # Consume 'where'
            self.Dr()  # Parse recursive definition
            
            # Add where node to AST with 2 children
            self.ast.append(ASTNode(NodeType.WHERE, "where", 2))
    
    def T(self) -> None:
        """
        Parse T -> Ta (',' Ta)* => 'tau' | Ta
        """
        self.Ta()  # Parse first term
        
        # Count tuple elements
        count = 1
        while self.tokens and self.tokens[0].value == ",":
            self.tokens.pop(0)  # Consume comma
            self.Ta()  # Parse next term
            count += 1
        
        # If we have multiple elements, create a tuple node
        if count > 1:
            self.ast.append(ASTNode(NodeType.TAU, "tau", count))
    
    def Ta(self) -> None:
        """
        Parse Ta -> Tc ('aug' Tc)*
        """
        self.Tc()  # Parse first term
        
        # Handle augmentation
        while self.tokens and self.tokens[0].value == "aug":
            self.tokens.pop(0)  # Consume 'aug'
            self.Tc()  # Parse next term
            
            # Add augmentation node
            self.ast.append(ASTNode(NodeType.AUG, "aug", 2))
    
    def Tc(self) -> None:
        """
        Parse Tc -> B '->' Tc '|' Tc | B
        """
        self.B()  # Parse condition
        
        # Handle conditional expressions
        if self.tokens and self.tokens[0].value == "->":
            self.tokens.pop(0)  # Consume '->'
            self.Tc()  # Parse true branch
            
            # Expect '|' for else branch
            if not self.tokens or self.tokens[0].value != "|":
                print("Error: Expected '|' in conditional expression")
                return
            
            self.tokens.pop(0)  # Consume '|'
            self.Tc()  # Parse false branch
            
            # Add conditional node with 3 children
            self.ast.append(ASTNode(NodeType.CONDITIONAL, "->", 3))
    
    def B(self) -> None:
        """
        Parse B -> Bt ('or' Bt)*
        """
        self.Bt()  # Parse first term
        
        # Handle logical OR
        while self.tokens and self.tokens[0].value == "or":
            self.tokens.pop(0)  # Consume 'or'
            self.Bt()  # Parse next term
            
            # Add OR node
            self.ast.append(ASTNode(NodeType.OR, "or", 2))
    
    def Bt(self) -> None:
        """
        Parse Bt -> Bs ('&' Bs)*
        """
        self.Bs()  # Parse first term
        
        # Handle logical AND
        while self.tokens and self.tokens[0].value == "&":
            self.tokens.pop(0)  # Consume '&'
            self.Bs()  # Parse next term
            
            # Add AND node
            self.ast.append(ASTNode(NodeType.AND, "&", 2))
    
    def Bs(self) -> None:
        """
        Parse Bs -> 'not' Bp | Bp
        """
        # Check for NOT operator
        if self.tokens and self.tokens[0].value == "not":
            self.tokens.pop(0)  # Consume 'not'
            self.Bp()  # Parse expression
            
            # Add NOT node
            self.ast.append(ASTNode(NodeType.NOT, "not", 1))
        else:
            self.Bp()
    
    def Bp(self) -> None:
        """
        Parse Bp -> A (comparison_op A)? 
        where comparison_op is one of: gr, ge, ls, le, eq, ne, >, >=, <, <=
        """
        self.A()  # Parse left operand
        
        # Check for comparison operators
        if self.tokens and self.tokens[0].value in ["gr", "ge", "ls", "le", "eq", "ne", ">", ">=", "<", "<="]:
            op = self.tokens[0].value
            self.tokens.pop(0)  # Consume operator
            self.A()  # Parse right operand
            
            # Map symbols to their corresponding operator names
            op_map = {
                ">": "gr", ">=": "ge", "<": "ls", "<=": "le"
            }
            
            # Use the mapped operator name or the original
            op_name = op_map.get(op, op)
            
            # Add comparison node
            self.ast.append(ASTNode(NodeType.COMPARE, op_name, 2))
    
    def A(self) -> None:
        """
        Parse A -> ('+' | '-')? At (['+' | '-'] At)*
        """
        # Handle unary plus/minus
        if self.tokens and self.tokens[0].value == "+":
            self.tokens.pop(0)  # Consume unary plus (no effect)
            self.At()
        elif self.tokens and self.tokens[0].value == "-":
            self.tokens.pop(0)  # Consume unary minus
            self.At()
            
            # Add negation node
            self.ast.append(ASTNode(NodeType.NEG, "neg", 1))
        else:
            self.At()  # Parse term
        
        # Handle binary plus/minus
        while self.tokens and self.tokens[0].value in ["+", "-"]:
            op = self.tokens[0].value
            self.tokens.pop(0)  # Consume operator
            self.At()  # Parse next term
            
            # Add appropriate operation node
            if op == "+":
                self.ast.append(ASTNode(NodeType.PLUS, "+", 2))
            else:
                self.ast.append(ASTNode(NodeType.MINUS, "-", 2))
    
    def At(self) -> None:
        """
        Parse At -> Af ('*' Af | '/' Af)*
        """
        self.Af()  # Parse first factor
        
        # Handle multiplication/division
        while self.tokens and self.tokens[0].value in ["*", "/"]:
            op = self.tokens[0].value
            self.tokens.pop(0)  # Consume operator
            self.Af()  # Parse next factor
            
            # Add appropriate operation node
            if op == "*":
                self.ast.append(ASTNode(NodeType.MULTIPLY, "*", 2))
            else:
                self.ast.append(ASTNode(NodeType.DIVIDE, "/", 2))
    
    def Af(self) -> None:
        """
        Parse Af -> Ap ('**' Af)?
        """
        self.Ap()  # Parse primary
        
        # Handle exponentiation
        if self.tokens and self.tokens[0].value == "**":
            self.tokens.pop(0)  # Consume '**'
            self.Af()  # Parse exponent
            
            # Add power node
            self.ast.append(ASTNode(NodeType.POWER, "**", 2))
    
    def Ap(self) -> None:
        """
        Parse Ap -> R ('@' <IDENTIFIER> R)*
        """
        self.R()  # Parse first term
        
        # Handle @ operator
        while self.tokens and self.tokens[0].value == "@":
            self.tokens.pop(0)  # Consume '@'
            
            # Expect identifier
            if not self.tokens or self.tokens[0].token_type != RPALTokenType.IDENTIFIER:
                print("Error: Expected identifier after '@'")
                return
            
            # Add identifier node
            self.ast.append(ASTNode(NodeType.IDENTIFIER, self.tokens[0].value, 0))
            self.tokens.pop(0)  # Consume identifier
            
            self.R()  # Parse second term
            
            # Add @ node with 3 children
            self.ast.append(ASTNode(NodeType.AT, "@", 3))
    
    def R(self) -> None:
        """
        Parse R -> Rn (Rn)*  => 'gamma'
        """
        self.Rn()  # Parse first term
        
        # Handle function application (gamma)
        while (self.tokens and 
               (self.tokens[0].token_type in [RPALTokenType.IDENTIFIER, RPALTokenType.INTEGER, RPALTokenType.STRING] or
                self.tokens[0].value in ["true", "false", "nil", "dummy", "("])):
            self.Rn()  # Parse argument
            
            # Add function application node
            self.ast.append(ASTNode(NodeType.GAMMA, "gamma", 2))
    
    def Rn(self) -> None:
        """
        Parse Rn -> <IDENTIFIER> | <INTEGER> | <STRING> | 'true' | 'false' | 'nil' | '(' E ')' | 'dummy'
        """
        if not self.tokens:
            print("Error: Unexpected end of tokens in Rn")
            return
        
        token = self.tokens[0]
        
        # Handle identifiers
        if token.token_type == RPALTokenType.IDENTIFIER:
            self.ast.append(ASTNode(NodeType.IDENTIFIER, token.value, 0))
            self.tokens.pop(0)  # Consume identifier
        
        # Handle integers
        elif token.token_type == RPALTokenType.INTEGER:
            self.ast.append(ASTNode(NodeType.INTEGER, token.value, 0))
            self.tokens.pop(0)  # Consume integer
        
        # Handle strings
        elif token.token_type == RPALTokenType.STRING:
            self.ast.append(ASTNode(NodeType.STRING, token.value, 0))
            self.tokens.pop(0)  # Consume string
        
        # Handle keywords
        elif token.token_type == RPALTokenType.KEYWORD:
            if token.value == "true":
                self.ast.append(ASTNode(NodeType.TRUE, "true", 0))
            elif token.value == "false":
                self.ast.append(ASTNode(NodeType.FALSE, "false", 0))
            elif token.value == "nil":
                self.ast.append(ASTNode(NodeType.NIL, "nil", 0))
            elif token.value == "dummy":
                self.ast.append(ASTNode(NodeType.DUMMY, "dummy", 0))
            else:
                print(f"Error: Unexpected keyword '{token.value}' in Rn")
                return
            self.tokens.pop(0)  # Consume keyword
        
        # Handle parenthesized expressions
        elif token.token_type == RPALTokenType.LPAREN:
            self.tokens.pop(0)  # Consume '('
            self.E()  # Parse expression
            
            # Expect closing parenthesis
            if not self.tokens or self.tokens[0].token_type != RPALTokenType.RPAREN:
                print("Error: Expected ')' after expression")
                return
            
            self.tokens.pop(0)  # Consume ')'
        
        else:
            print(f"Error: Unexpected token '{token.value}' in Rn")
    
    # Definition parsing methods
    
    def D(self) -> None:
        """
        Parse D -> Da 'within' D | Da
        """
        self.Da()  # Parse first definition
        
        # Handle 'within' construct
        if self.tokens and self.tokens[0].value == "within":
            self.tokens.pop(0)  # Consume 'within'
            self.D()  # Parse second definition
            
            # Add within node
            self.ast.append(ASTNode(NodeType.WITHIN, "within", 2))
    
    def Da(self) -> None:
        """
        Parse Da -> Dr ('and' Dr)* => 'and' | Dr
        """
        self.Dr()  # Parse first definition
        
        # Count definitions in 'and' construct
        count = 1
        while self.tokens and self.tokens[0].value == "and":
            self.tokens.pop(0)  # Consume 'and'
            self.Dr()  # Parse next definition
            count += 1
        
        # If we have multiple definitions, create 'and' node
        if count > 1:
            self.ast.append(ASTNode(NodeType.AND_DEF, "and", count))
    
    def Dr(self) -> None:
        """
        Parse Dr -> 'rec' Db | Db
        """
        # Check for recursive definition
        is_recursive = False
        if self.tokens and self.tokens[0].value == "rec":
            self.tokens.pop(0)  # Consume 'rec'
            is_recursive = True
        
        self.Db()  # Parse definition body
        
        # Add recursive node if necessary
        if is_recursive:
            self.ast.append(ASTNode(NodeType.REC, "rec", 1))
    
    def Db(self) -> None:
        """
        Parse Db -> Vl '=' E | <IDENTIFIER> Vb+ '=' E | '(' D ')'
        """
        if not self.tokens:
            print("Error: Unexpected end of tokens in Db")
            return
        
        # Handle parenthesized definition
        if self.tokens[0].token_type == RPALTokenType.LPAREN:
            self.tokens.pop(0)  # Consume '('
            self.D()  # Parse definition
            
            # Expect closing parenthesis
            if not self.tokens or self.tokens[0].token_type != RPALTokenType.RPAREN:
                print("Error: Expected ')' after definition")
                return
            
            self.tokens.pop(0)  # Consume ')'
        
        # Handle identifier-based definitions
        elif self.tokens[0].token_type == RPALTokenType.IDENTIFIER:
            # Look ahead to determine which rule to apply
            if len(self.tokens) > 1:
                next_token = self.tokens[1]
                
                # Function definition: <IDENTIFIER> Vb+ '=' E
                if (next_token.token_type == RPALTokenType.IDENTIFIER or 
                    next_token.token_type == RPALTokenType.LPAREN):
                    # Add function name identifier
                    self.ast.append(ASTNode(NodeType.IDENTIFIER, self.tokens[0].value, 0))
                    self.tokens.pop(0)  # Consume identifier
                    
                    # Parse parameters
                    param_count = 0
                    while (self.tokens and 
                           (self.tokens[0].token_type == RPALTokenType.IDENTIFIER or 
                            self.tokens[0].token_type == RPALTokenType.LPAREN)):
                        self.Vb()  # Parse parameter
                        param_count += 1
                    
                    # Expect '=' operator
                    if not self.tokens or self.tokens[0].value != "=":
                        print("Error: Expected '=' in function definition")
                        return
                    
                    self.tokens.pop(0)  # Consume '='
                    self.E()  # Parse function body
                    
                    # Add function form node
                    self.ast.append(ASTNode(NodeType.FUNCTION_FORM, "fcn_form", param_count + 2))
                
                # Simple variable definition: <IDENTIFIER> '=' E
                elif next_token.value == "=":
                    # Add variable name identifier
                    self.ast.append(ASTNode(NodeType.IDENTIFIER, self.tokens[0].value, 0))
                    self.tokens.pop(0)  # Consume identifier
                    self.tokens.pop(0)  # Consume '='
                    
                    self.E()  # Parse value expression
                    
                    # Add equality node
                    self.ast.append(ASTNode(NodeType.EQUAL, "=", 2))
                
                # Variable list definition: Vl '=' E
                elif next_token.value == ",":
                    self.Vl()  # Parse variable list
                    
                    # Expect '=' operator
                    if not self.tokens or self.tokens[0].value != "=":
                        print("Error: Expected '=' after variable list")
                        return
                    
                    self.tokens.pop(0)  # Consume '='
                    self.E()  # Parse value expression
                    
                    # Add equality node
                    self.ast.append(ASTNode(NodeType.EQUAL, "=", 2))
                
                else:
                    print(f"Error: Unexpected token '{next_token.value}' in Db")
            else:
                print("Error: Unexpected end of tokens in Db")
    
    def Vb(self) -> None:
        """
        Parse Vb -> <IDENTIFIER> | '(' Vl ')' | '(' ')'
        """
        if not self.tokens:
            print("Error: Unexpected end of tokens in Vb")
            return
        
        # Handle parenthesized variables
        if self.tokens[0].token_type == RPALTokenType.LPAREN:
            self.tokens.pop(0)  # Consume '('
            
            # Check for empty tuple
            if self.tokens[0].token_type == RPALTokenType.RPAREN:
                self.tokens.pop(0)  # Consume ')'
                self.ast.append(ASTNode(NodeType.EMPTY_TUPLE, "()", 0))
            else:
                self.Vl()  # Parse variable list
                
                # Expect closing parenthesis
                if not self.tokens or self.tokens[0].token_type != RPALTokenType.RPAREN:
                    print("Error: Expected ')' after variable list")
                    return
                
                self.tokens.pop(0)  # Consume ')'
        
        # Handle identifiers
        elif self.tokens[0].token_type == RPALTokenType.IDENTIFIER:
            # Add identifier node
            self.ast.append(ASTNode(NodeType.IDENTIFIER, self.tokens[0].value, 0))
            self.tokens.pop(0)  # Consume identifier
        
        else:
            print(f"Error: Expected identifier or '(' in Vb, got '{self.tokens[0].value}'")
    
    def Vl(self) -> None:
        """
        Parse Vl -> <IDENTIFIER> (',' <IDENTIFIER>)*
        """
        if not self.tokens:
            print("Error: Unexpected end of tokens in Vl")
            return
        
        # Parse first identifier
        if self.tokens[0].token_type != RPALTokenType.IDENTIFIER:
            print("Error: Expected identifier in variable list")
            return
        
        # Add first identifier node
        self.ast.append(ASTNode(NodeType.IDENTIFIER, self.tokens[0].value, 0))
        self.tokens.pop(0)  # Consume identifier
        
        # Count identifiers in the list
        count = 1
        
        # Parse remaining identifiers
        while self.tokens and self.tokens[0].value == ",":
            self.tokens.pop(0)  # Consume comma
            
            # Expect identifier
            if not self.tokens or self.tokens[0].token_type != RPALTokenType.IDENTIFIER:
                print("Error: Expected identifier after comma in variable list")
                return
            
            # Add identifier node
            self.ast.append(ASTNode(NodeType.IDENTIFIER, self.tokens[0].value, 0))
            self.tokens.pop(0)  # Consume identifier
            
            count += 1
        
        # If we have multiple identifiers, create comma node
        if count > 1:
            self.ast.append(ASTNode(NodeType.COMMA, ",", count))