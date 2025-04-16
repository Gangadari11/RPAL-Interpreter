# Makefile for RPAL Language Interpreter

# Python command
PYTHON = python3

# Source files
SOURCES = myrpal.py \
          lexer/lexical_analyzer.py \
          parser/parser.py \
          ast/ast.py \
          ast/ast_factory.py \
          ast/node.py \
          csem/csemachine.py \
          csem/cse_factory.py \
          csem/nodes.py

# Default target
all: check

# Check if Python is installed
check:
	@which $(PYTHON) > /dev/null || (echo "Python is not installed"; exit 1)
	@echo "Python is installed"

# Run the interpreter
run:
	$(PYTHON) myrpal.py $(ARGS)

# Clean generated files
clean:
	rm -rf __pycache__
	rm -rf lexer/__pycache__
	rm -rf parser/__pycache__
	rm -rf ast/__pycache__
	rm -rf csem/__pycache__
	find . -name "*.pyc" -delete

# Test the interpreter with a sample program
test:
	@echo "Testing the interpreter with a sample program..."
	@echo "let Sum(A) = Psum (A,Order A ) where rec Psum (T,N) = N eq 0 -> 0 | Psum(T,N-1)+T N in Print ( Sum (1,2,3,4,5) )" > test.rpal
	$(PYTHON) myrpal.py test.rpal
	rm test.rpal

# Help target
help:
	@echo "Available targets:"
	@echo "  all    - Check if Python is installed"
	@echo "  run    - Run the interpreter (use ARGS='file_name [-ast]')"
	@echo "  clean  - Remove generated files"
	@echo "  test   - Test the interpreter with a sample program"
	@echo "  help   - Display this help message"

.PHONY: all check run clean test help
