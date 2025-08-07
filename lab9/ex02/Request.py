#client request class
class Request:
    
    def __init__(self, a, b, op):
        self.operator = op
        self.n1 = a
        self.n2 = b
    
    def __str__(self):
        return f"{self.n1} {self.operator} {self.n2}"
    
    #built object from string
    @classmethod
    def from_string(cls, string):
        parts = string.split()
        if len(parts) != 3:
            raise ValueError("Invalid request format")
        return cls(parts[0], parts[2], parts[1])
    
    def getOperator(self):
        return self.operator
    
    def getFirstNumber(self):
        return self.n1
    
    def getSecondNumber(self):
        return self.n2