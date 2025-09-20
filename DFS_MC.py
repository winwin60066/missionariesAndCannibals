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

def main(ML, CL, boat_capacity):
    boat = "left"
    m_total, c_total = ML, CL

    tracemalloc.start()
    start_time = time.time()

    solution, stats = dfs(ML, CL, boat, m_total, c_total, boat_capacity)
    total_children, total_nodes = stats

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("Solution found:")
    depth = print_solution(solution)
    if total_nodes > 0:
        branching_factor = total_children / total_nodes
        print(f"\nApproximate branching factor: {branching_factor:.2f}")
        print(f"Time taken: {end_time - start_time:.6f} seconds")
        print(f"Peak memory used: {peak / 1024:.2f} KB")
        print("-"*61, "\n")

def checkMax(state, boat_capacity): 
    if state.boat == "left":
        availableMis = min(state.ML, boat_capacity)
        availableCan = min(state.CL, boat_capacity)
    else:
        availableMis = min(state.MR, boat_capacity)
        availableCan = min(state.CR, boat_capacity)
    return availableMis, availableCan
    
def nextChild(currentState):
    children = [] #currentState frontier
    maxM, maxC = checkMax(currentState, currentState.boat_capacity)
    
    for m in range(0, maxM+1): 
        for c in range(0, maxC+1):
            if 1 <= m+c <= currentState.boat_capacity:
                if currentState.boat == "left":
                    newState = State(currentState.ML - m, currentState.CL - c, "right", currentState.m_total, currentState.c_total, currentState.boat_capacity)
                else: #right
                    newState = State(currentState.ML + m, currentState.CL + c, "left", currentState.m_total, currentState.c_total, currentState.boat_capacity)
                
                if newState.valid():
                    newState.parent = currentState #Track
                    children.append(newState)
                    
    return children    

def print_solution(solution):
    if not solution:
        print("\n[No solution found. The problem is unsolvable with given values]")
        return None
    
    path = []
    #backtrack from goal to start
    while solution:
        path.append(solution)
        solution = solution.parent
    #Reverse to get initial
    path.reverse()
    
    for state in path:
        print(f"Left Side: Missionaries = {state.ML}, Cannibals = {state.CL} | Right Side: Missionaries = {state.MR}, Cannibals = {state.CR} | Boat at '{state.boat}' side ")
    
    depth = len(path) - 1
    print(f"\n[Solution depth (Number of moves): {depth}]")
    return depth


def dfs(ML, CL, boat, m_total, c_total, boat_capacity):
    initialState = State(ML, CL, boat, m_total, c_total, boat_capacity)
    if initialState.goal():
        return initialState
    frontier = list()
    explored = set() #Prevent doubled state
    
    frontier.append(initialState)
    
    #Branching Factor use
    total_nodes_expanded = 0
    total_children_generated = 0
    
    while frontier:
        state = frontier.pop()  # Changed from pop(0) to pop() for DFS
        if state.goal():
            return state, (total_children_generated, total_nodes_expanded)
            
        explored.add(state)
        children = nextChild(state) #Generate moves
        
        total_nodes_expanded += 1
        total_children_generated += len(children)
        
        for child in children:
            if (child not in explored) and (child not in frontier):
                frontier.append(child)
    
    return None, (total_children_generated, total_nodes_expanded)

if __name__ == "__main__":

    test_cases = [
        (1, 2, 2),
        (2, 2, 2),
        (1, 1, 2),
        (3, 2, 2),
        (3, 3, 2),
        (2, 1, 2),
        (4, 3, 2),
        (3, 4, 2),
        (3, 3, 3),
        (5, 5, 3),
    ]

    print("\n[Start of Depth-First Search Algorithm]")
    print("\n---------------- Missionaries and Cannibals (Depth-First Search) ----------------\n")
    for idx, (M, C, B) in enumerate(test_cases, start=1):
        print(f"----------------------- Test Case {idx} -----------------------\nScenario: Missionaries = {M}, Cannibals = {C}, Boat = {B}")
        print("-"*60)
        main(M, C, B)

    print("[End of Depth-First Search Algorithm]\n")
