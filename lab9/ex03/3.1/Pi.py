import multiprocessing

class PiCalc(multiprocessing.Process):
    
    def __init__(self, blockNumber, numberOfSteps, pi_ref):
        super(PiCalc, self).__init__()
        self.blockNum = blockNumber
        self.steps = numberOfSteps
        self.step = 1.0/numberOfSteps
        self.num_processes = multiprocessing.cpu_count()
        self.lock = multiprocessing.Lock()
        self.pi = pi_ref
    
    def run(self):
        local_sum = 0
    
        # Αναγωγή με μοιραζόμενη μεταβλητή και κλείδωμα 
        block = self.steps//self.num_processes
        start = self.blockNum * block
        stop = start + block
        if self.blockNum==self.num_processes-1:
           stop = self.steps

        for j in range(start, stop):
            x = (j + 0.5) * self.step
            local_sum += 4.0 / (1.0 + x**2)
        
        with self.lock:
            self.pi.value += local_sum
            
    def getPi(self):
        return self.pi.value
    