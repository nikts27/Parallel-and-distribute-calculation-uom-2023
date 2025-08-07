#server reply class
class Reply:
    
    def __init__(self, n):
        self.result = n
    
    def __str__(self):
        return str(self.result)
    
    #built object from string
    @classmethod
    def from_string(cls, string):
        try:
            result = float(string)
        except ValueError:
            result = string
        return cls(result)
    
    def setResult(self, n):
        self.result = n
    
    def getResult(self):
        return self.result