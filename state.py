import time
import tracemalloc

class State:
    def __init__(self, ML, CL, boat, m_total, c_total, boat_capacity):
        self.ML = ML
        self.CL = CL
        self.boat = boat
        self.m_total = m_total
        self.c_total = c_total
        self.boat_capacity = boat_capacity
        self.parent = None

    @property
    def CR(self):
        return self.c_total - self.CL

    @property
    def MR(self):
        return self.m_total - self.ML
        
    def goal(self): #Goal state
        if (self.ML == 0 and self.CL == 0 and self.boat == "right"):
            return True
        else:
            return False
    
    def valid(self):
        if(
            (self.ML >= 0 and self.MR >= 0 ) and
            (self.CL >= 0 and self.CR >= 0 ) and 
            (self.ML == 0 or self.ML >= self.CL) and 
            (self.MR == 0 or self.MR >= self.CR)
        ):
            return True
        else:
            return False
        
    def __eq__(self, other):  #Check equal state
        return (self.CL == other.CL 
                and self.ML == other.ML
                and self.boat == other.boat)
    
    def __hash__(self): #Store unique state
        return hash((self.ML, self.CL, self.boat))