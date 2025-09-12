from state import State
from utils import nextChild

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