from lexer import tokenize_rpal
from parser import RPALParser
from standardizer import standardize_ast

def test_standardizer():
    # Test case from the input file
    source_code = """
    let Sum(A) = Psum (A,Order A) 
    where rec Psum(T,N) = N eq 0 -> 0 
    | Psum(T,N-1)+T N 
    in Print (Sum (1,2,3,4,5))
    """
    
    # Tokenize the source code
    tokens = tokenize_rpal(source_code)
    
    # Parse tokens into AST
    parser = RPALParser(tokens)
    ast_root = parser.parse()
    
    if not ast_root:
        print("Failed to parse the input code")
        return
    
    # Print the original AST
    print("Original AST:")
    print("============")
    ast_lines = parser.print_ast()
    for line in ast_lines:
        print(line)
    
    # Standardize the AST
    st_root = standardize_ast(ast_root)
    
    if not st_root:
        print("Failed to standardize the AST")
        return
    
    # Print the standardized tree
    print("\nStandardized Tree:")
    print("================")
    st_lines = st_root.print_st()
    for line in st_lines:
        print(line)

if __name__ == "__main__":
    test_standardizer()