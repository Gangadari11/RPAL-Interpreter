class Token:
    def __init__(self, type, value, line=1, column=1):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, {self.value}, line={self.line}, column={self.column})"

class RPALLexer:
    reserved = {
        'let': 'KEYWORD', 'in': 'KEYWORD', 'fn': 'KEYWORD', 'where': 'KEYWORD',
        'rec': 'KEYWORD', 'within': 'KEYWORD', 'and': 'KEYWORD', 'or': 'KEYWORD',
        'gr': 'KEYWORD', 'ge': 'KEYWORD', 'ls': 'KEYWORD', 'le': 'KEYWORD',
        'nil': 'KEYWORD', 'true': 'KEYWORD', 'false': 'KEYWORD', 'not': 'KEYWORD',
        'aug': 'KEYWORD', 'isnil': 'KEYWORD', 'neg': 'KEYWORD', 'Stem': 'KEYWORD',
        'Stern': 'KEYWORD', 'Order': 'KEYWORD', 'Print': 'KEYWORD',
        'Conc': 'KEYWORD', 'eq': 'KEYWORD', 'ne': 'KEYWORD'
    }

    token_types = [
        'IDENTIFIER', 'INTEGER', 'STRING', 'OPERATOR',
        'LPAREN', 'RPAREN', 'COMMA', 'SEMICOLON', 'KEYWORD'
    ]

    operator_symbols = {
        '->', '**', '>=', '<=', '==', '/=', '><', '||', '::', ':=',
        '+', '-', '*', '/', '<', '>', '&', '.', '@', '|', ':', '~', '=',
        '!', '#', '%', '^', '[', ']', '{', '}', '"', '?'
    }

    multi_char_ops = ['->', '**', '>=', '<=', '==', '/=', '><', '||', '::', ':=']
    
    def __init__(self):
        self.input = ""
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.current_char = None
    
    def error(self):
        raise Exception(f"Illegal character '{self.current_char}' at line {self.line}, column {self.column}")
    
    def advance(self):
        self.position += 1
        self.column += 1
        if self.position >= len(self.input):
            self.current_char = None
        else:
            self.current_char = self.input[self.position]
    
    def peek(self, ahead=1):
        peek_pos = self.position + ahead
        if peek_pos >= len(self.input):
            return None
        return self.input[peek_pos]
    
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        self.advance()
        self.advance()
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
    
    def handle_newline(self):
        self.advance()
        self.line += 1
        self.column = 1
    
    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)
    
    def identifier_or_keyword(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        if result in self.reserved:
            return result, self.reserved[result]
        return result, 'IDENTIFIER'
    
    def string(self):
        self.advance()
        result = ''
        while self.current_char is not None and self.current_char != "'":
            if self.current_char == '\\' and self.peek() is not None:
                self.advance()
                if self.current_char == 'n':
                    result += '\n'
                elif self.current_char == 't':
                    result += '\t'
                elif self.current_char == 'r':
                    result += '\r'
                elif self.current_char == "'":
                    result += "'"
                elif self.current_char == '\\':
                    result += '\\'
                else:
                    result += self.current_char
            else:
                result += self.current_char
            self.advance()
        if self.current_char == "'":
            self.advance()
        else:
            raise Exception(f"Unterminated string at line {self.line}, column {self.column}")
        return result
    
    def operator(self):
        for op in sorted(self.multi_char_ops, key=len, reverse=True):
            op_length = len(op)
            if self.position + op_length <= len(self.input):
                potential_op = self.input[self.position:self.position + op_length]
                if potential_op == op:
                    result = potential_op
                    for _ in range(op_length):
                        self.advance()
                    return result
        result = self.current_char
        self.advance()
        return result
    
    def tokenize(self, input_text):
        self.input = input_text
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.current_char = self.input[0] if self.input else None

        while self.current_char is not None:
            if self.current_char in ' \t\r':
                self.skip_whitespace()
                continue
            if self.current_char == '\n':
                self.handle_newline()
                continue
            if self.current_char == '/' and self.peek() == '/':
                self.skip_comment()
                continue
            if self.current_char.isdigit():
                token_value = self.integer()
                self.tokens.append(Token('INTEGER', token_value, self.line, self.column - len(str(token_value))))
                continue
            if self.current_char.isalpha():
                token_value, token_type = self.identifier_or_keyword()
                self.tokens.append(Token(token_type, token_value, self.line, self.column - len(token_value)))
                continue
            if self.current_char == "'":
                token_value = self.string()
                self.tokens.append(Token('STRING', token_value, self.line, self.column - len(token_value) - 2))
                continue
            if self.current_char == '(':
                self.tokens.append(Token('LPAREN', '(', self.line, self.column))
                self.advance()
                continue
            if self.current_char == ')':
                self.tokens.append(Token('RPAREN', ')', self.line, self.column))
                self.advance()
                continue
            if self.current_char == ',':
                self.tokens.append(Token('COMMA', ',', self.line, self.column))
                self.advance()
                continue
            if self.current_char == ';':
                self.tokens.append(Token('SEMICOLON', ';', self.line, self.column))
                self.advance()
                continue
            current_char_str = self.current_char
            if any(op.startswith(current_char_str) for op in self.operator_symbols):
                token_value = self.operator()
                self.tokens.append(Token('OPERATOR', token_value, self.line, self.column - len(token_value)))
                continue
            self.error()
        return self.tokens
