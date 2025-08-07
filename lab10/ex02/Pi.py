class Pi():
    
    def __init__(self):
        self.result = 0
        self.workers = 0
        
    def addTo(self, num):
        self.result += num
        self.workers += 1
        
    def printResult(self):
        print("Final result = " + str(self.result/self.workers))