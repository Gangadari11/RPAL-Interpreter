"""
Node classes for CSE Machine
Defines the structure and behavior of nodes in the CSE machine.
"""

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
