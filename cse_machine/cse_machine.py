

"""
Fixed CSE Machine for RPAL Language
Properly handles built-in functions and partial application.
"""

from utils.helper_functions import convert_string_to_bool

class Symbol:
    """Base class for symbols in the CSE machine."""
    def __init__(self, data):
        self.data = data

    def set_data(self, data):
        """Set the data of the symbol."""
        self.data = data

    def get_data(self):
        """Get the data of the symbol."""
        return self.data
    
class Rand(Symbol):
    """Class representing a rand symbol."""
    def __init__(self, data):
        super().__init__(data)

    def get_data(self):
        """Get the data of the rand symbol."""
        return super().get_data()

class Rator(Symbol):
    """Class representing a rator symbol."""
    def __init__(self, data):
        super().__init__(data)

class B(Symbol):
    """Class representing a B symbol."""
    def __init__(self):
        super().__init__("b")
        self.symbols = []

class Beta(Symbol):
    """Class representing a Beta symbol."""
    def __init__(self):
        super().__init__("beta")
        
class Bool(Rand):
    """Class representing a Boolean symbol."""
    def __init__(self, data):
        super().__init__(data)

class Bop(Rator):
    """Class representing a binary operator symbol."""
    def __init__(self, data):
        super().__init__(data)
        
class Delta(Symbol):
    """Class representing a Delta symbol."""
    def __init__(self, i):
        super().__init__("delta")
        self.index = i
        self.symbols = []

    def set_index(self, i):
        """Set the index of the Delta symbol."""
        self.index = i

    def get_index(self):
        """Get the index of the Delta symbol."""
        return self.index

class Dummy(Rand):
    """Class representing a Dummy symbol."""
    def __init__(self):
        super().__init__("dummy")

class E(Symbol):
    """Class representing an E symbol."""
    def __init__(self, i):
        super().__init__("e")
        self.index = i
        self.parent = None
        self.is_removed = False
        self.values = {}

    def set_parent(self, e):
        """Set the parent of the E symbol."""
        self.parent = e

    def get_parent(self):
        """Get the parent of the E symbol."""
        return self.parent

    def set_index(self, i):
        """Set the index of the E symbol."""
        self.index = i

    def get_index(self):
        """Get the index of the E symbol."""
        return self.index

    def set_is_removed(self, is_removed):
        """Set whether the E symbol is removed."""
        self.is_removed = is_removed

    def get_is_removed(self):
        """Get whether the E symbol is removed."""
        return self.is_removed

    def lookup(self, id):
        """
        Look up an identifier in the environment.
        
        Args:
            id: The identifier to look up
            
        Returns:
            Symbol: The symbol associated with the identifier
        """
        for key in self.values:
            if key.get_data() == id.get_data():
                return self.values[key]
        if self.parent is not None:
            return self.parent.lookup(id)
        else:
            # Return built-in function if it exists
            builtin_name = id.get_data()
            if builtin_name in ["Print", "Conc", "Stem", "Stern", "Order", "Isinteger", "Isstring", "Istuple", "Isdummy", "Istruthvalue", "Isfunction"]:
                return BuiltinFunction(builtin_name)
            return Symbol(id.get_data())

class Err(Symbol):
    """Class representing an error symbol."""
    def __init__(self):
        super().__init__("")

class Eta(Symbol):
    """Class representing an Eta symbol."""
    def __init__(self):
        super().__init__("eta")
        self.index = None
        self.environment = None
        self.identifier = None
        self.lambda_ = None

    def set_index(self, i):
        """Set the index of the Eta symbol."""
        self.index = i

    def get_index(self):
        """Get the index of the Eta symbol."""
        return self.index

    def set_environment(self, e):
        """Set the environment of the Eta symbol."""
        self.environment = e

    def get_environment(self):
        """Get the environment of the Eta symbol."""
        return self.environment

    def set_identifier(self, identifier):
        """Set the identifier of the Eta symbol."""
        self.identifier = identifier

    def set_lambda(self, lambda_):
        """Set the lambda of the Eta symbol."""
        self.lambda_ = lambda_

    def get_lambda(self):
        """Get the lambda of the Eta symbol."""
        return self.lambda_

class Gamma(Symbol):
    """Class representing a Gamma symbol."""
    def __init__(self):
        super().__init__("gamma")

class Id(Rand):
    """Class representing an identifier symbol."""
    def __init__(self, data):
        super().__init__(data)
    
    def get_data(self):
        """Get the data of the identifier symbol."""
        return super().get_data()

class Int(Rand):
    """Class representing an integer symbol."""
    def __init__(self, data):
        super().__init__(data)

class Lambda(Symbol):
    """Class representing a Lambda symbol."""
    def __init__(self, i):
        super().__init__("lambda")
        self.index = i
        self.environment = None
        self.identifiers = []
        self.delta = None

    def set_environment(self, n):
        """Set the environment of the Lambda symbol."""
        self.environment = n

    def get_environment(self):
        """Get the environment of the Lambda symbol."""
        return self.environment

    def set_delta(self, delta):
        """Set the delta of the Lambda symbol."""
        self.delta = delta

    def get_delta(self):
        """Get the delta of the Lambda symbol."""
        return self.delta
        
    def get_index(self):
        """Get the index of the Lambda symbol."""
        return self.index

class Str(Rand):
    """Class representing a string symbol."""
    def __init__(self, data):
        super().__init__(data)

class Tau(Symbol):
    """Class representing a Tau symbol."""
    def __init__(self, n):
        super().__init__("tau")
        self.set_n(n)

    def set_n(self, n):
        """Set the n of the Tau symbol."""
        self.n = n

    def get_n(self):
        """Get the n of the Tau symbol."""
        return self.n

class Tup(Rand):
    """Class representing a tuple symbol."""
    def __init__(self):
        super().__init__("tup")
        self.symbols = []

class Uop(Rator):
    """Class representing a unary operator symbol."""
    def __init__(self, data):
        super().__init__(data)

class Ystar(Symbol):
    """Class representing a Y* symbol."""
    def __init__(self):
        super().__init__("<Y*>")

class BuiltinFunction(Symbol):
    """Class representing a built-in function."""
    def __init__(self, name):
        super().__init__(name)
        self.name = name
        self.arity = self.get_arity(name)
        self.args = []

    def get_arity(self, name):
        """Get the arity (number of arguments) for a built-in function."""
        arities = {
            "Print": 1,
            "Conc": 2,
            "Stem": 1,
            "Stern": 1,
            "Order": 1,
            "Isinteger": 1,
            "Isstring": 1,
            "Istuple": 1,
            "Isdummy": 1,
            "Istruthvalue": 1,
            "Isfunction": 1
        }
        return arities.get(name, 0)

    def add_arg(self, arg):
        """Add an argument to the function."""
        self.args.append(arg)

    def is_fully_applied(self):
        """Check if the function has all its arguments."""
        return len(self.args) >= self.arity

    def apply(self):
        """Apply the function with its arguments."""
        if self.name == "Print":
            result = self.format_output(self.args[0])
            print(result)
            return Dummy()  # Print returns dummy
        elif self.name == "Conc":
            s1, s2 = self.args[0], self.args[1]
            result = Str("'" + s1.get_data().strip("'") + s2.get_data().strip("'") + "'")
            return result
        elif self.name == "Stem":
            s = self.args[0]
            if isinstance(s, Str):
                content = s.get_data().strip("'")
                if content:
                    return Str("'" + content[0] + "'")
                else:
                    return Str("''")
            return s
        elif self.name == "Stern":
            s = self.args[0]
            if isinstance(s, Str):
                content = s.get_data().strip("'")
                if len(content) > 1:
                    return Str("'" + content[1:] + "'")
                else:
                    return Str("''")
            return s
        elif self.name == "Order":
            tup = self.args[0]
            if isinstance(tup, Tup):
                return Int(str(len(tup.symbols)))
            return Int("0")
        elif self.name == "Isinteger":
            return Bool("true" if isinstance(self.args[0], Int) else "false")
        elif self.name == "Isstring":
            return Bool("true" if isinstance(self.args[0], Str) else "false")
        elif self.name == "Istuple":
            return Bool("true" if isinstance(self.args[0], Tup) else "false")
        elif self.name == "Isdummy":
            return Bool("true" if isinstance(self.args[0], Dummy) else "false")
        elif self.name == "Istruthvalue":
            return Bool("true" if isinstance(self.args[0], Bool) else "false")
        elif self.name == "Isfunction":
            return Bool("true" if isinstance(self.args[0], (Lambda, BuiltinFunction)) else "false")
        
        return Err()

    def format_output(self, value):
        """Format a value for output."""
        if isinstance(value, Str):
            return value.get_data().strip("'")
        elif isinstance(value, Tup):
            if len(value.symbols) == 0:
                return "()"
            formatted = []
            for symbol in value.symbols:
                formatted.append(self.format_output(symbol))
            return "(" + ", ".join(formatted) + ")"
        elif isinstance(value, Lambda):
            # Format lambda closure with parameter names and index
            param_names = []
            for identifier in value.identifiers:
                param_names.append(identifier.get_data())
            param_str = ", ".join(param_names)
            return f"[lambda closure: {param_str}: {value.get_index()}]"
        elif isinstance(value, BuiltinFunction):
            # Format built-in functions
            if value.is_fully_applied():
                return f"[builtin function: {value.name}]"
            else:
                return f"[partial builtin function: {value.name}]"
        elif isinstance(value, Dummy):
            return "dummy"
        elif isinstance(value, Bool):
            return value.get_data()
        elif isinstance(value, Int):
            return value.get_data()
        else:
            return str(value.get_data())

class CSEMachine:
    """Class representing a CSE machine."""
    def __init__(self, control, stack, environment):
        self.control = control
        self.stack = stack
        self.environment = environment

    def execute(self):
        """Execute the CSE machine."""
        current_environment = self.environment[0]
        j = 1
        while self.control:
            current_symbol = self.control.pop()
            
            if isinstance(current_symbol, Id):
                self.stack.insert(0, current_environment.lookup(current_symbol))
            elif isinstance(current_symbol, Lambda):
                current_symbol.set_environment(current_environment.get_index())
                self.stack.insert(0, current_symbol)
            elif isinstance(current_symbol, Gamma):
                if len(self.stack) < 2:
                    raise RuntimeError("Stack underflow: not enough arguments for gamma")
                
                next_symbol = self.stack.pop(0)
                
                if isinstance(next_symbol, Lambda):
                    # Handle Lambda expression
                    lambda_expr = next_symbol
                    e = E(j)
                    j += 1
                    if len(lambda_expr.identifiers) == 1:
                        temp = self.stack.pop(0)
                        e.values[lambda_expr.identifiers[0]] = temp
                    else:
                        tup = self.stack.pop(0)
                        for i, id in enumerate(lambda_expr.identifiers):
                            e.values[id] = tup.symbols[i]
                    for env in self.environment:
                        if env.get_index() == lambda_expr.get_environment():
                            e.set_parent(env)
                    current_environment = e
                    self.control.append(e)
                    self.control.append(lambda_expr.get_delta())
                    self.stack.insert(0, e)
                    self.environment.append(e)
                elif isinstance(next_symbol, BuiltinFunction):
                    # Handle built-in function
                    arg = self.stack.pop(0)
                    next_symbol.add_arg(arg)
                    
                    if next_symbol.is_fully_applied():
                        result = next_symbol.apply()
                        self.stack.insert(0, result)
                    else:
                        # Return partially applied function
                        self.stack.insert(0, next_symbol)
                elif isinstance(next_symbol, Tup):
                    # Handle Tup expression
                    tup = next_symbol
                    i = int(self.stack.pop(0).get_data())
                    self.stack.insert(0, tup.symbols[i - 1])
                elif isinstance(next_symbol, Ystar):
                    # Handle Ystar expression
                    lambda_expr = self.stack.pop(0)
                    eta = Eta()
                    eta.set_index(lambda_expr.get_index())
                    eta.set_environment(lambda_expr.get_environment())
                    eta.set_identifier(lambda_expr.identifiers[0])
                    eta.set_lambda(lambda_expr)
                    self.stack.insert(0, eta)
                elif isinstance(next_symbol, Eta):
                    # Handle Eta expression
                    eta = next_symbol
                    lambda_expr = eta.get_lambda()
                    self.control.append(Gamma())
                    self.control.append(Gamma())
                    self.stack.insert(0, eta)
                    self.stack.insert(0, lambda_expr)
                else:
                    raise RuntimeError(f"Cannot apply gamma to {type(next_symbol)}")
                    
            elif isinstance(current_symbol, E):
                # Handle E expression
                if len(self.stack) > 1:
                    self.stack.pop(1)
                self.environment[current_symbol.get_index()].set_is_removed(True)
                y = len(self.environment)
                while y > 0:
                    if not self.environment[y - 1].get_is_removed():
                        current_environment = self.environment[y - 1]
                        break
                    else:
                        y -= 1
            elif isinstance(current_symbol, Rator):
                if isinstance(current_symbol, Uop):
                    # Handle Unary operation
                    rator = current_symbol
                    rand = self.stack.pop(0)
                    self.stack.insert(0, self.apply_unary_operation(rator, rand))
                if isinstance(current_symbol, Bop):
                    # Handle Binary operation
                    rator = current_symbol
                    rand1 = self.stack.pop(0)
                    rand2 = self.stack.pop(0)
                    self.stack.insert(0, self.apply_binary_operation(rator, rand1, rand2))
            elif isinstance(current_symbol, Beta):
                # Handle Beta expression
                if (self.stack[0].get_data() == "true"):
                    self.control.pop()
                else:
                    self.control.pop(-2)
                self.stack.pop(0)
            elif isinstance(current_symbol, Tau):
                # Handle Tau expression
                tau = current_symbol
                tup = Tup()
                for _ in range(tau.get_n()):
                    tup.symbols.append(self.stack.pop(0))
                self.stack.insert(0, tup)
            elif isinstance(current_symbol, Delta):
                # Handle Delta expression
                self.control.extend(current_symbol.symbols)
            elif isinstance(current_symbol, B):
                # Handle B expression
                self.control.extend(current_symbol.symbols)
            else:
                self.stack.insert(0, current_symbol)

    def convert_string_to_bool(self, data):
        """
        Convert a string to a boolean.
        
        Args:
            data: The string to convert
            
        Returns:
            bool: The converted boolean
        """
        if data == "true":
            return True
        elif data == "false":
            return False

    def apply_unary_operation(self, rator, rand):
        """
        Apply a unary operation.
        
        Args:
            rator: The operator
            rand: The operand
            
        Returns:
            Symbol: The result of the operation
        """
        if rator.get_data() == "neg":
            val = int(rand.get_data())
            return Int(str(-1 * val))
        elif rator.get_data() == "not":
            val = self.convert_string_to_bool(rand.get_data())
            return Bool(str(not val).lower())
        else:
            return Err()

    def apply_binary_operation(self, rator, rand1, rand2):
        """
        Apply a binary operation.
        
        Args:
            rator: The operator
            rand1: The first operand
            rand2: The second operand
            
        Returns:
            Symbol: The result of the operation
        """
        if rator.get_data() == "+":
            val1 = int(rand1.get_data())
            val2 = int(rand2.get_data())
            return Int(str(val1 + val2))
        elif rator.data == "-":
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Int(str(val1 - val2))
        elif rator.data == "*":
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Int(str(val1 * val2))
        elif rator.data == "/":
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Int(str(int(val1 / val2)))
        elif rator.data == "**":
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Int(str(val1 ** val2))
        elif rator.data == "&":
            val1 = self.convert_string_to_bool(rand1.data)
            val2 = self.convert_string_to_bool(rand2.data)
            return Bool(str(val1 and val2).lower())
        elif rator.data == "or":
            val1 = self.convert_string_to_bool(rand1.data)
            val2 = self.convert_string_to_bool(rand2.data)
            return Bool(str(val1 or val2).lower())
        elif rator.data == "eq":
            val1 = rand1.data
            val2 = rand2.data
            return Bool(str(val1 == val2).lower())
        elif rator.data == "ne":
            val1 = rand1.data
            val2 = rand2.data
            return Bool(str(val1 != val2).lower())
        elif rator.data == "ls":
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Bool(str(val1 < val2).lower())
        elif rator.data == "le":
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Bool(str(val1 <= val2).lower())
        elif rator.data == "gr":
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Bool(str(val1 > val2).lower())
        elif rator.data == "ge":
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Bool(str(val1 >= val2).lower())
        elif rator.data == "aug":
            if isinstance(rand2, Tup):
                rand1.symbols.extend(rand2.symbols)
            else:
                rand1.symbols.append(rand2)
            return rand1
        else:
            return Err()

    def get_tuple_value(self, tup):
        """
        Get the value of a tuple.
        
        Args:
            tup: The tuple
            
        Returns:
            str: The string representation of the tuple
        """
        temp = "("
        for symbol in tup.symbols:
            if isinstance(symbol, Tup):
                temp += self.get_tuple_value(symbol) + ", "
            else:
                temp += symbol.get_data() + ", "
        temp = temp[:-2] + ")" if len(tup.symbols) > 0 else temp + ")"
        return temp

    def get_answer(self):
        """
        Get the answer from the CSE machine.
        
        Returns:
            str: The answer, or empty string if result is dummy from Print
        """
        self.execute()
        if isinstance(self.stack[0], Tup):
            return self.get_tuple_value(self.stack[0])
        elif isinstance(self.stack[0], Dummy):
            return ""  # Don't print dummy result from Print function
        return self.stack[0].get_data()

class CSEMachineFactory:
    """Factory class for creating CSE machines."""
    def __init__(self):
        self.e0 = E(0)
        self.i = 1
        self.j = 0

    def get_symbol(self, node):
        """
        Get a symbol from a node.
        
        Args:
            node: The node
            
        Returns:
            Symbol: The symbol
        """
        data = node.get_data()
        if data in ("not", "neg"):
            return Uop(data)  # Unary operator symbol
        elif data in ("+", "-", "*", "/", "**", "&", "or", "eq", "ne", "ls", "le", "gr", "ge", "aug"):
            return Bop(data)  # Binary operator symbol
        elif data == "gamma":
            return Gamma()  # Gamma symbol
        elif data == "tau":
            return Tau(len(node.get_children()))  # Tau symbol with the number of children
        elif data == "<Y*>":
            return Ystar()  # Y* symbol
        else:
            if data.startswith("<IDENTIFIER:"):
                return Id(data[12:-1])  # Identifier symbol
            elif data.startswith("<INTEGER:"):
                return Int(data[9:-1])  # Integer symbol
            elif data.startswith("<STRING:"):
                return Str(data[9:-2])  # String symbol
            elif data.startswith("<NIL"):
                return Tup()  # Tuple symbol
            elif data.startswith("<TRUE_VALUE:t"):
                return Bool("true")  # Boolean true symbol
            elif data.startswith("<TRUE_VALUE:f"):
                return Bool("false")  # Boolean false symbol
            elif data.startswith("<dummy>"):
                return Dummy()  # Dummy symbol
            else:
                return Err()  # Error symbol

    def get_b(self, node):
        """
        Get a B symbol from a node.
        
        Args:
            node: The node
            
        Returns:
            B: The B symbol
        """
        b = B()
        b.symbols = self.get_pre_order_traverse(node)
        return b

    def get_lambda(self, node):
        """
        Get a Lambda symbol from a node.
        
        Args:
            node: The node
            
        Returns:
            Lambda: The Lambda symbol
        """
        lambda_expr = Lambda(self.i)
        self.i += 1
        lambda_expr.set_delta(self.get_delta(node.get_children()[1]))
        if node.get_children()[0].get_data() == ",":
            for identifier in node.get_children()[0].get_children():
                lambda_expr.identifiers.append(Id(identifier.get_data()[12:-1]))
        else:
            lambda_expr.identifiers.append(Id(node.get_children()[0].get_data()[12:-1]))
        return lambda_expr

    def get_pre_order_traverse(self, node):
        """
        Get a pre-order traversal of a node.
        
        Args:
            node: The node
            
        Returns:
            list: The pre-order traversal
        """
        symbols = []
        if node.get_data() == "lambda":
            symbols.append(self.get_lambda(node))  # Lambda expression symbol
        elif node.get_data() == "->":
            symbols.append(self.get_delta(node.get_children()[1]))  # Delta symbol
            symbols.append(self.get_delta(node.get_children()[2]))  # Delta symbol
            symbols.append(Beta())  # Beta symbol
            symbols.append(self.get_b(node.get_children()[0]))  # B symbol
        else:
            symbols.append(self.get_symbol(node))
            for child in node.get_children():
                symbols.extend(self.get_pre_order_traverse(child))
        return symbols

    def get_delta(self, node):
        """
        Get a Delta symbol from a node.
        
        Args:
            node: The node
            
        Returns:
            Delta: The Delta symbol
        """
        delta = Delta(self.j)
        self.j += 1
        delta.symbols = self.get_pre_order_traverse(node)
        return delta

    def get_control(self, ast):
        """
        Get the control for a CSE machine.
        
        Args:
            ast: The AST
            
        Returns:
            list: The control
        """
        control = [self.e0, self.get_delta(ast.get_root())]
        return control

    def get_stack(self):
        """
        Get the stack for a CSE machine.
        
        Args:
            ast: The AST
            
        Returns:
            list: The stack
        """
        return [self.e0]

    def get_environment(self):
        """
        Get the environment for a CSE machine.
        
        Args:
            ast: The AST
            
        Returns:
            list: The environment
        """
        return [self.e0]

    def get_cse_machine(self, ast):
        """
        Get a CSE machine from an AST.
        
        Args:
            ast: The AST
            
        Returns:
            CSEMachine: The CSE machine
        """
        control = self.get_control(ast)
        stack = self.get_stack()
        environment = self.get_environment()
        return CSEMachine(control, stack, environment)
