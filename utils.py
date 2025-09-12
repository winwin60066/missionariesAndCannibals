from state import State

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
        print("\n[No solution found. The problem is unsolvable with given values]\n")
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