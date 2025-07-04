# RPAL-Interpreter



# RPAL Language Interpreter

A complete implementation of a lexical analyzer, parser, and CSE (Control-Stack-Environment) machine for the RPAL (Right-reference Pedagogic Algorithmic Language) functional programming language.

## Project Overview

This interpreter implements the full RPAL language specification including:
- Lexical analysis (tokenization)
- Syntax analysis (parsing) 
- Abstract Syntax Tree (AST) generation
- Tree standardization
- CSE machine execution

## Features

- **Complete RPAL Language Support**: Handles all RPAL constructs including let expressions, lambda functions, recursion, conditionals, and built-in functions
- **Built-in Functions**: Supports Print, Conc, Stem, Stern, Order, and type checking functions
- **Partial Application**: Proper handling of curried functions and partial application
- **Lambda Closures**: Correct implementation of lexical scoping and closures
- **Error Handling**: Comprehensive error detection and reporting
- **Debug Modes**: Optional AST and standardized tree printing for debugging

## Project Structure

```
RPAL-Interpreter/
├── myrpal.py                 # Main interpreter entry point
├── lexer/
│   └── lexer.py             # Lexical analyzer
├── parser/
│   └── parser.py            # Syntax analyzer and AST builder
├── ast/
│   ├── ast_node.py          # AST node definitions
│   └── ast_printer.py       # AST utilities and factory
├── cse_machine/
│   └── cse_machine.py       # CSE machine implementation
├── utils/
│   ├── token_types.py       # Token type definitions
│   └── helper_functions.py  # Utility functions
├── inputs/                  # Sample RPAL programs
│   ├── conc.1              # String concatenation example
│   ├── defns.1             # Function definition example
│   └── ...                 # More test files
└── README.md               # This file
```

## Installation

### Prerequisites
- Python 3.7 or higher

### Setup
1. Clone or download the project
2. Navigate to the project directory
3. No additional dependencies required (uses only Python standard library)

## Usage

### Running RPAL Programs

#### Basic Execution
``` bash
python myrpal.py <filename>
```
#### Examples
``` bash
# Run a .txt file containing RPAL code
python myrpal.py program.txt

# Run sample programs
python myrpal.py inputs/conc.1
python myrpal.py inputs/defns.1
```

### Command Line Options

``` bash
python myrpal.py <filename> [options]
```

**Options:**
- -ast : Print the Abstract Syntax Tree and exit
- -st : Print the Standardized Tree and exit

#### Examples with Options
``` bash
# View the AST of a program
python myrpal.py program.txt -ast

# View the standardized tree
python myrpal.py program.txt -st

# Normal execution (default)
python myrpal.py program.txt
```

## Creating RPAL Programs

### File Format
- Create a text file with \`.txt\` extension (or any extension)
- Write RPAL code using standard RPAL syntax
- Save the file in UTF-8 encoding

### Sample Program (save as \`hello.txt\`)
``` rpal
Print 'Hello, World!'
```

### Run the Program
``` bash
python myrpal.py hello.txt
```

**Output:**
```
Hello, World!
```

## RPAL Language Examples

### 1. String Concatenation (\`concat_example.txt\`)
``` rpal
let Conc x y = Conc x y in
let S = 'Hello' and T = 'World'
and Mark = Conc 'Hello '
in
Print (Conc S T, Mark T)
```

**Run:**
``` bash
python myrpal.py concat_example.txt
```

**Output:**
```
(HelloWorld, Hello World)
```

### 2. Lambda Functions (\`lambda_example.txt\`)
``` rpal
Print (
let f x y =
(let g x y =
(let h x y = x y x
in h)
in g)
in f
)
```

**Run:**
``` bash
python myrpal.py lambda_example.txt
```

**Output:**
```
[lambda closure: x: 2]
```

### 3. Arithmetic Operations (\`math_example.txt\`)
``` rpal
let add x y = x + y in
let multiply x y = x * y in
Print (add 5 3, multiply 4 6)
```

**Run:**
``` bash
python myrpal.py math_example.txt
```

**Output:**
```
(8, 24)
```

### 4. Conditional Expressions (\`conditional_example.txt\`)
``` rpal
let max x y = x > y -> x | y in
Print (max 10 5, max 3 8)
```

**Run:**
``` bash
python myrpal.py conditional_example.txt
```

**Output:**
```
(10, 8)
```

### 5. Recursive Functions (\`factorial_example.txt\`)
``` rpal
let rec factorial n = 
  n eq 0 -> 1 | n * factorial (n - 1)
in
Print (factorial 5)
```

**Run:**
``` bash
python myrpal.py factorial_example.txt
```

**Output:**
```
120
```

## Built-in Functions

| Function | Description | Example |
|----------|-------------|---------|
| Print | Output values | Print 'Hello' |
| Conc | String concatenation | Conc 'Hello' 'World'  |
| Stem | First character of string | Stem 'Hello'  → \'H' |
| Stern | String without first character | Stern 'Hello'  →  'ello' |
| Order | Length of tuple |  Order (1,2,3) →  3 |
| Isinteger | Check if integer | Isinteger 42  → true |
| Isstring | Check if string | Isstring 'hello' → true |
| Istuple | Check if tuple | Istuple (1,2) → true |
| Isdummy | Check if dummy | Isdummy dummy → true |
| Istruthvalue | Check if boolean | Istruthvalue true → true |
| Isfunction | Check if function | Isfunction (lambda x.x) → true |

## Debugging

### View AST Structure
``` bash
python myrpal.py program.txt -ast
```

This shows the parsed Abstract Syntax Tree before standardization.

### View Standardized Tree
``` bash
python myrpal.py program.txt -st
```

This shows the standardized tree that will be executed by the CSE machine.

## Error Handling

The interpreter provides detailed error messages for:
- **Lexical errors**: Invalid tokens or characters
- **Syntax errors**: Malformed expressions or missing operators
- **Runtime errors**: Stack underflow, type mismatches, etc.

### Example Error
``` rpal
let x = 5
```

**Error:**
```
Parse error: 'in' expected
```

## Troubleshooting

### Common Issues

1. **File not found**
   - Ensure the file path is correct
   - Check file permissions

2. **Parse errors**
   - Verify RPAL syntax is correct
   - Check for missing keywords (\`in\`, \`let\`, etc.)

3. **Stack underflow**
   - Usually indicates incorrect function application
   - Check function arity and arguments

### Getting Help

1. Use -ast flag to examine the parsed structure
2. Use -st flag to see the standardized tree
3. Check the sample programs in the inputs/ directory

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with various RPAL programs
5. Submit a pull request

## License

This project is for educational purposes. Please check with your institution's academic integrity policies before using.

## Acknowledgments

- Based on the RPAL language specification
- Implements the CSE machine evaluation model
- Follows functional programming language design principles


# How to Run RPAL Programs with .txt Files

## Basic Usage
python myrpal.py filename.txt

## Examples

# 1. Create a simple program file
echo "Print 'Hello World'" > hello.txt
python myrpal.py hello.txt

# 2. String concatenation example
echo "let Conc x y = Conc x y in Print (Conc 'Hello' 'World')" > concat.txt
python myrpal.py concat.txt

# 3. Lambda function example  
echo "Print (let f x = x + 1 in f)" > lambda.txt
python myrpal.py lambda.txt

# 4. View AST structure
python myrpal.py hello.txt -ast

# 5. View standardized tree
python myrpal.py hello.txt -st

## File Requirements
- Any text file with RPAL code
- UTF-8 encoding recommended
- File extension doesn't matter (.txt, .rpal, .prog, etc.)

## Sample Programs to Try

### factorial.txt
let rec factorial n = 
  n eq 0 -> 1 | n * factorial (n - 1)
in
Print (factorial 5)

### fibonacci.txt
let rec fib n =
  n le 1 -> n | fib(n-1) + fib(n-2)
in
Print (fib 10)

### tuple_example.txt
let tuple = (1, 'hello', true) in
Print (Order tuple, tuple)

### conditional.txt
let max x y = x > y -> x | y in
let min x y = x &lt; y -> x | y in
Print (max 10 5, min 10 5)


## 2. System Architecture

### 2.1 Overall System Flow

```
RPAL Source Code
       ↓
   Lexical Analyzer (Tokenizer)
       ↓
   List of Tokens
       ↓
   Parser
       ↓
   Abstract Syntax Tree (AST)
       ↓
   Standardizer
       ↓
   Standardized Tree (ST)
       ↓
   CSE Machine
       ↓
   Program Output
```


### 2.2 Component Interaction Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   myrpal.py     │───▶│   lexer.py      │───▶│   parser.py     │
│   (Main Driver) │    │   (Tokenizer)   │    │   (AST Builder) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                                              │
         ▼                                              ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Output        │◀───│  cse_machine.py │◀───│  ast_printer.py │
│   (Results)     │    │  (Executor)     │    │  (Standardizer) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```


2.3 Module Structure
```
myrpal/
├── myrpal.py                 # Main driver
├── lexer/
│   └── lexer.py              # Lexical analyzer
├── parser/
│   └── parser.py             # Recursive descent parser
├── ast/
│   ├── ast_node.py           # AST node structure
│   └── ast_printer.py        # Standardization + AST display
├── cse_machine/
│   └── cse_machine.py        # Stack-based execution machine
└── utils/
    ├── token_types.py        # Enum and constants
    └── helper_functions.py   # General utilities
```

#### 3.1.2 Token Types
```
class TokenType(Enum):
    KEYWORD = 1      # let, in, fn, where, etc.
    IDENTIFIER = 2   # Variable names
    INTEGER = 3      # Numeric literals
    STRING = 4       # String literals
    PUNCTUATION = 5  # (, ), ;, ,
    OPERATOR = 6     # +, -, *, /, etc.
    END_OF_TOKENS = 7
```

#### 3.1.3 Lexical Rules Implementation
```
token_patterns = {
    'COMMENT': r'//.*',
    'KEYWORD': r'(let|in|fn|where|aug|or|not|gr|ge|ls|le|eq|ne|true|false|nil|dummy|within|and|rec)\\b',
    'STRING': r'\\'(?:\\\\\\'|[^\\'])*\\'',
    'IDENTIFIER': r'[a-zA-Z][a-zA-Z0-9_]*',
    'INTEGER': r'\\d+',
    'OPERATOR': r'[+\\-*<>&.@/:=~|$\\#!%^_\\[\\]{}"\\'?]+',
    'SPACES': r'[ \\t\\n]+',
    'PUNCTUATION': r'[();,]'
}
```

#### 3.2.2 Grammar Rules Mapping
```
E   → 'let' D 'in' E | 'fn' Vb+ '.' E | Ew
Ew  → T 'where' Dr | T
T   → Ta (',' Ta)*
Ta  → Ta 'aug' Tc | Tc
Tc  → B '->' Tc '|' Tc | B
B   → B 'or' Bt | Bt
Bt  → Bt '&' Bs | Bs
Bs  → 'not' Bp | Bp
Bp  → A ('gr'|'ge'|'ls'|'le'|'eq'|'ne') A | A
A   → A ('+'|'-') At | At
At  → At ('*'|'/') Af | Af
Af  → Ap '**' Af | Ap
Ap  → Ap '@' '<IDENTIFIER>' R | R
R   → R Rn | Rn
Rn  → '<IDENTIFIER>' | '<INTEGER>' | '<STRING>' | 'true' | 'false' | 'nil' | '(' E ')' | 'dummy'
```

#### 3.3.1 Node Structure
```
class Node:
    def __init__(self):
        self.data = None           # Node content
        self.depth = 0            # Tree depth
        self.parent = None        # Parent reference
        self.children = []        # Child nodes
        self.is_standardized = False
```

#### 3.4.2 Standardization Rules

**Let Expression:**
```
let x = E in P  →  gamma(lambda x.P, E)
```
**Where Expression:**
```
P where x = E  →  let x = E in P
```

**Function Form:**
```
f x1 x2...xn = E  →  f = lambda x1.(lambda x2.(...(lambda xn.E)...))
```

**Lambda with Multiple Parameters:**
```
lambda x1 x2...xn.E  →  lambda x1.(lambda x2.(...(lambda xn.E)...))
```

**Within Expression:**
```
x1 = E1 within x2 = E2  →  x2 = gamma(lambda x1.E2, E1)
```

**Simultaneous Definitions:**
```
x1 = E1 and x2 = E2  →  (x1, x2) = tau(E1, E2)
```

**Recursive Definition:**
```
rec x = E  →  x = gamma(Y*, lambda x.E)
```

**Infix Operator:**
```
E1 @ N E2  →  gamma(gamma(N, E1), E2)
```

#### 3.5.2 Symbol Types
```
# Basic symbols
class Symbol: pass
class Rand(Symbol): pass      # Operands
class Rator(Symbol): pass     # Operators

# Specific symbol types
class Lambda(Symbol): pass    # Lambda expressions
class Gamma(Symbol): pass     # Function application
class Delta(Symbol): pass     # Code blocks
class Beta(Symbol): pass      # Conditional selection
class Tau(Symbol): pass       # Tuple construction
class E(Symbol): pass         # Environment markers
```

```
def execute(self):
    while self.control:
        current_symbol = self.control.pop()
        
        if isinstance(current_symbol, Id):
            # Variable lookup
            self.stack.insert(0, current_environment.lookup(current_symbol))
            
        elif isinstance(current_symbol, Lambda):
            # Lambda closure creation
            current_symbol.set_environment(current_environment.get_index())
            self.stack.insert(0, current_symbol)
            
        elif isinstance(current_symbol, Gamma):
            # Function application
            self.handle_gamma()
            
        # ... other symbol types
```
### 4.1 Main Driver (myrpal.py)

```
def main() -> None:
    """Main entry point for the RPAL interpreter."""
    
def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    
def read_input_file(filename: str) -> str:
    """Read RPAL program from input file."""
```
\`\`\`python
def tokenize(input_str: str) -> List[Token]:
    """
    Tokenize the input string according to RPAL lexical rules.
    
    Args:
        input_str: The input RPAL program as a string
        
    Returns:
        List of Token objects
    """
\`\`\`

