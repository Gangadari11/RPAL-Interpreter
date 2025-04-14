class ASTNode:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
    
    def __str__(self, level=0):
        result = "  " * level + f"{self.type}"
        if self.value is not None:
            result += f": {self.value}"
        result += "\n"
        for child in self.children:
            result += child.__str__(level + 1)
        return result

class RPALParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = []
        self.current_token_idx = 0
        self.current_token = None
    
    def error(self, expected=None):
        if self.current_token:
            if expected:
                raise Exception(f"Syntax error at line {self.current_token.line}, column {self.current_token.column}: Expected {expected}, got {self.current_token.type} '{self.current_token.value}'")
            else:
                raise Exception(f"Syntax error at line {self.current_token.line}, column {self.current_token.column}")
        else:
            raise Exception("Syntax error: Unexpected end of input")
    
    def eat(self, token_type=None, token_value=None):
        if self.current_token is None:
            self.error(token_type)
        
        if token_type and self.current_token.type != token_type:
            self.error(token_type)
        
        if token_value and self.current_token.value != token_value:
            self.error(f"'{token_value}'")
        
        current_token = self.current_token
        self.current_token_idx += 1
        if self.current_token_idx < len(self.tokens):
            self.current_token = self.tokens[self.current_token_idx]
        else:
            self.current_token = None
        
        return current_token
    
    def peek(self, ahead=1):
        peek_idx = self.current_token_idx + ahead - 1
        if peek_idx < len(self.tokens):
            return self.tokens[peek_idx]
        return None
    
    def parse(self, input_text):
        self.tokens = self.lexer.tokenize(input_text)
        if self.tokens:
            self.current_token = self.tokens[0]
            ast = self.E()
            if self.current_token is not None:
                self.error("End of input")
            return ast
        return None
    
    # E -> 'let' D 'in' E
    # E -> 'fn' Vb+ '.' E
    # E -> Ew
    def E(self):
        if self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'let':
            node = ASTNode('let')
            self.eat('KEYWORD', 'let')
            node.add_child(self.D())
            self.eat('KEYWORD', 'in')
            node.add_child(self.E())
            return node
        elif self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'fn':
            node = ASTNode('lambda')
            self.eat('KEYWORD', 'fn')
            
            # Parse one or more variable bindings
            vars_node = ASTNode('vars')
            while self.current_token and self.current_token.type == 'IDENTIFIER':
                vars_node.add_child(ASTNode('var', self.current_token.value))
                self.eat('IDENTIFIER')
            
            if vars_node.children:
                node.add_child(vars_node)
            else:
                self.error("variable name")
            
            self.eat('OPERATOR', '.')
            node.add_child(self.E())
            return node
        else:
            return self.Ew()
    
    # Ew -> T 'where' Dr
    # Ew -> T
    def Ew(self):
        t_node = self.T()
        
        if self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'where':
            node = ASTNode('where')
            self.eat('KEYWORD', 'where')
            node.add_child(t_node)
            node.add_child(self.Dr())
            return node
        else:
            return t_node
    
    # T -> Ta (',' Ta)+
    # T -> Ta
    def T(self):
        first_ta = self.Ta()
        
        if self.current_token and self.current_token.type == 'COMMA':
            node = ASTNode('tau')
            node.add_child(first_ta)
            
            while self.current_token and self.current_token.type == 'COMMA':
                self.eat('COMMA')
                node.add_child(self.Ta())
            
            return node
        else:
            return first_ta
    
    # Ta -> Ta 'aug' Tc
    # Ta -> Tc
    def Ta(self):
        left = self.Tc()
        
        while self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'aug':
            node = ASTNode('aug')
            self.eat('KEYWORD', 'aug')
            node.add_child(left)
            node.add_child(self.Tc())
            left = node
        
        return left
    
    # Tc -> B '->' Tc '|' Tc
    # Tc -> B
    def Tc(self):
        left = self.B()
        
        if self.current_token and self.current_token.type == 'OPERATOR' and self.current_token.value == '->':
            node = ASTNode('->')
            self.eat('OPERATOR', '->')
            node.add_child(left)
            node.add_child(self.Tc())
            
            self.eat('OPERATOR', '|')
            node.add_child(self.Tc())
            
            return node
        else:
            return left
    
    # B -> B 'or' Bt
    # B -> Bt
    def B(self):
        left = self.Bt()
        
        while self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'or':
            node = ASTNode('or')
            self.eat('KEYWORD', 'or')
            node.add_child(left)
            node.add_child(self.Bt())
            left = node
        
        return left
    
    # Bt -> Bt '&' Bs
    # Bt -> Bs
    def Bt(self):
        left = self.Bs()
        
        while self.current_token and self.current_token.type == 'OPERATOR' and self.current_token.value == '&':
            node = ASTNode('&')
            self.eat('OPERATOR', '&')
            node.add_child(left)
            node.add_child(self.Bs())
            left = node
        
        return left
    
    # Bs -> 'not' Bp
    # Bs -> Bp
    def Bs(self):
        if self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'not':
            node = ASTNode('not')
            self.eat('KEYWORD', 'not')
            node.add_child(self.Bp())
            return node
        else:
            return self.Bp()
    
    # Bp -> A ('gr'|'>'|'ge'|'>='|'ls'|'<'|'le'|'<='|'eq'|'ne') A
    # Bp -> A
    def Bp(self):
        left = self.A()
        
        if self.current_token and self.current_token.type in ('KEYWORD', 'OPERATOR'):
            op_mapping = {
                'gr': 'gr', '>': 'gr',
                'ge': 'ge', '>=': 'ge',
                'ls': 'ls', '<': 'ls',
                'le': 'le', '<=': 'le',
                'eq': 'eq', '==': 'eq',
                'ne': 'ne', '/=': 'ne'
            }
            
            if self.current_token.value in op_mapping:
                node = ASTNode(op_mapping[self.current_token.value])
                self.eat()  # Eat the operator
                node.add_child(left)
                node.add_child(self.A())
                return node
        
        return left
    
    # A -> A '+'|'-' At
    # A -> At
    def A(self):
        left = self.At()
        
        while self.current_token and self.current_token.type == 'OPERATOR' and self.current_token.value in ('+', '-'):
            op = self.current_token.value
            self.eat('OPERATOR')
            node = ASTNode(op)
            node.add_child(left)
            node.add_child(self.At())
            left = node
        
        return left
    
    # At -> At '*'|'/' Af
    # At -> Af
    def At(self):
        left = self.Af()
        
        while self.current_token and self.current_token.type == 'OPERATOR' and self.current_token.value in ('*', '/'):
            op = self.current_token.value
            self.eat('OPERATOR')
            node = ASTNode(op)
            node.add_child(left)
            node.add_child(self.Af())
            left = node
        
        return left
    
    # Af -> Ap '**' Af
    # Af -> Ap
    def Af(self):
        left = self.Ap()
        
        if self.current_token and self.current_token.type == 'OPERATOR' and self.current_token.value == '**':
            node = ASTNode('**')
            self.eat('OPERATOR', '**')
            node.add_child(left)
            node.add_child(self.Af())
            return node
        else:
            return left
    
    # Ap -> Ap '@' '<IDENTIFIER>' R
    # Ap -> R
    def Ap(self):
        left = self.R()
        
        while self.current_token and self.current_token.type == 'OPERATOR' and self.current_token.value == '@':
            node = ASTNode('@')
            self.eat('OPERATOR', '@')
            
            if self.current_token and self.current_token.type == 'IDENTIFIER':
                id_node = ASTNode('id', self.current_token.value)
                self.eat('IDENTIFIER')
                node.add_child(left)
                node.add_child(id_node)
                node.add_child(self.R())
                left = node
            else:
                self.error("identifier")
        
        return left
        
    # R -> R Rn
    # R -> Rn
    def R(self):
        left = self.Rn()
        
        # Handle function application (gamma) - cases where Rn is directly followed by another Rn
        while self.current_token and (
            self.current_token.type in ('IDENTIFIER', 'INTEGER', 'STRING', 'LPAREN') or
            (self.current_token.type == 'KEYWORD' and self.current_token.value in ('true', 'false', 'nil'))
        ):
            # Function application
            node = ASTNode('gamma')
            node.add_child(left)
            node.add_child(self.Rn())
            left = node
        
        return left
    
    # Rn -> '<IDENTIFIER>'
    # Rn -> '<INTEGER>'
    # Rn -> '<STRING>'
    # Rn -> 'true'
    # Rn -> 'false'
    # Rn -> 'nil'
    # Rn -> '(' E ')'
    # Rn -> 'dummy'
    def Rn(self):
        if not self.current_token:
            self.error("expression")
        
        if self.current_token.type == 'IDENTIFIER':
            node = ASTNode('id', self.current_token.value)
            self.eat('IDENTIFIER')
            return node
        elif self.current_token.type == 'INTEGER':
            node = ASTNode('int', self.current_token.value)
            self.eat('INTEGER')
            return node
        elif self.current_token.type == 'STRING':
            node = ASTNode('str', self.current_token.value)
            self.eat('STRING')
            return node
        elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'true':
            node = ASTNode('true')
            self.eat('KEYWORD', 'true')
            return node
        elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'false':
            node = ASTNode('false')
            self.eat('KEYWORD', 'false')
            return node
        elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'nil':
            node = ASTNode('nil')
            self.eat('KEYWORD', 'nil')
            return node
        elif self.current_token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.E()
            self.eat('RPAREN')
            return node
        else:
            self.error("valid expression")
    
    # D -> Da 'within' D
    # D -> Da
    def D(self):
        da_node = self.Da()
        
        if self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'within':
            node = ASTNode('within')
            self.eat('KEYWORD', 'within')
            node.add_child(da_node)
            node.add_child(self.D())
            return node
        else:
            return da_node
    
    # Da -> Dr ('and' Dr)+
    # Da -> Dr
    def Da(self):
        first_dr = self.Dr()
        
        if self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'and':
            node = ASTNode('and')
            node.add_child(first_dr)
            
            while self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'and':
                self.eat('KEYWORD', 'and')
                node.add_child(self.Dr())
            
            return node
        else:
            return first_dr
    
    # Dr -> 'rec' Db
    # Dr -> Db
    def Dr(self):
        if self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'rec':
            node = ASTNode('rec')
            self.eat('KEYWORD', 'rec')
            node.add_child(self.Db())
            return node
        else:
            return self.Db()
    
    # Db -> Vl '=' E
    # Db -> '<IDENTIFIER>' Vb+ '=' E
    # Db -> '(' D ')'
    def Db(self):
        if self.current_token and self.current_token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.D()
            self.eat('RPAREN')
            return node
        elif self.current_token and self.current_token.type == 'IDENTIFIER':
            id_name = self.current_token.value
            self.eat('IDENTIFIER')
            
            # Check if it's a function definition with params
            if self.current_token and self.current_token.type == 'IDENTIFIER':
                node = ASTNode('fcn_form')
                id_node = ASTNode('id', id_name)
                node.add_child(id_node)
                
                # Parse variable bindings
                vars_node = ASTNode('vars')
                while self.current_token and self.current_token.type == 'IDENTIFIER':
                    vars_node.add_child(ASTNode('var', self.current_token.value))
                    self.eat('IDENTIFIER')
                
                node.add_child(vars_node)
                
                self.eat('OPERATOR', '=')
                node.add_child(self.E())
                
                return node
            else:
                # Simple variable assignment
                node = ASTNode('=')
                id_node = ASTNode('id', id_name)
                node.add_child(id_node)
                
                self.eat('OPERATOR', '=')
                node.add_child(self.E())
                
                return node
        else:
            self.error("identifier or '('")
    
    # Vl -> '<IDENTIFIER>' list ','
    def Vl(self):
        if self.current_token and self.current_token.type == 'IDENTIFIER':
            node = ASTNode('=')
            id_node = ASTNode('id', self.current_token.value)
            self.eat('IDENTIFIER')
            node.add_child(id_node)
            
            self.eat('OPERATOR', '=')
            node.add_child(self.E())
            
            return node
        else:
            self.error("identifier")

# Example usage
if __name__ == "__main__":
    from rpal_lexer import RPALLexer  # Make sure to import your lexer class
    
    lexer = RPALLexer()
    parser = RPALParser(lexer)
    
    # Example RPAL program
    program = """
    let
        factorial = fn n.
            n = 0 -> 1 | n * factorial(n-1)
    in
        factorial(5)
    """
    
    try:
        ast = parser.parse(program)
        print(ast)
    except Exception as e:
        print(f"Error: {e}")