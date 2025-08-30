class State:
    def __init__(self,ML,CL,boat,m_total,C_total,boat_capacity):
        self.ML = ML
        self.CL = CL
        self.boat = boat
        self.m_total = m_total
        self.C_total = C_total
        self.boat_capacity = boat_capacity
        


    @property
    def MR(self):
        return self.m_total - self.ML

    @property
    def CR(self):
        return self.C_total - self.CL

    def is_valid(self):
        # check if state is valid

        #when there is negative amount
        if self.ML < 0 or self.MR < 0 or self.CL < 0 or self.CR < 0:
            return False

        #when missionaries on left is lesser than cannibals but missionaries > 0
        if self.ML < self.CL and self.ML > 0:
            return False

        #when on right
        if self.MR < self.CR and self.MR > 0:
            return False

        return True

    #is goal only if all M&C on right side including boat
    def is_goal(self):
        return (self.ML == 0 and
                self.CL == 0 and
                self.MR == self.m_total and
                self.CR == self.C_total and
                self.boat == "right")

    def __eq__(self, other):
        return(
            self.ML == other.ML and
            self.CL == other.CL and
            self.MR == other.MR and
            self.CR == other.CR and
            self.boat == other.boat
        ) #return boolean

    def __hash__(self):
        return hash((self.ML,self.CL,self.MR,self.CR,self.boat))

    def __str__(self):
        return f"Left Side: Missionaries = {self.ML}, Cannibals = {self.CL} | Right Side: Missionaries = {self.MR}, Cannibals = {self.CR} | Boat at {self.boat} side"

def get_valid_moves(state):
    moves = []
    # Determine which side the boat is on
    if state.boat == "left":
        max_m = state.ML
        max_c = state.CL
        new_boat = "right"
    else:
        max_m = state.MR
        max_c = state.CR
        new_boat = "left"

    # Try all combinations of 1 to boat_capacity people
    for m in range(0, min(state.boat_capacity, max_m) + 1):
        for c in range(0, min(state.boat_capacity - m, max_c) + 1):
            if m + c == 0:
                continue
            if state.boat == "left":
                new_state = State(
                    ML=state.ML - m,
                    CL=state.CL - c,
                    boat=new_boat,
                    m_total=state.m_total,
                    C_total=state.C_total,
                    boat_capacity=state.boat_capacity
                )
            else:
                new_state = State(
                    ML=state.ML + m,
                    CL=state.CL + c,
                    boat=new_boat,
                    m_total=state.m_total,
                    C_total=state.C_total,
                    boat_capacity=state.boat_capacity
                )

            if new_state.is_valid():
                moves.append(new_state)
    return moves


def dfsAlgorithm(start_state, goal_state):
    stack = [(start_state, [start_state])]
    visited = set()

    while stack:
        current, path = stack.pop()
        if current == goal_state:
            return path
        if current in visited:
            continue
        visited.add(current)

        for neighbor in get_valid_moves(current):
            stack.append((neighbor, path + [neighbor]))

    return None


def main():
    problems = [
        (3, 3, 2),
        (2, 2, 2),
        (4, 4, 2),
        (3, 3, 1),
        (5, 5, 3),
        (6, 6, 2),
        (1, 1, 1),
        (2, 3, 2),
        (3, 2, 2),
        (4, 3, 2)
    ]

    start_states = [
        (1,2,"left"),
        (2,2,"left"),
        (1,1,"left"),
        (3,2,"left"),
        (3,3,"left"),
        (2,1,"left"),
        (4,3,"left"),
        (3,4,"left"),
        (3,3,"left"),
        (5,5,"left")
    ]

    goal_states = [
        (0,0,"right"),
        (0,0,"right"),
        (0,0,"right"),
        (0,0,"right"),
        (0,0,"right"),
        (0,0,"right"),
        (0,0,"right"),
        (0,0,"right"),
        (0,0,"right"),
        (0,0,"right")
    ]


    print("---------- Missionaries And Cannibals ----------")
    print("[Depth-First Search]")
    print("Number of missionaries must be more than number of cannibals")

    for i in range(len(problems)):
        M_total, C_total, boat_capacity = problems[i]
        start_M, start_C, start_boat = start_states[i]
        goal_M, goal_C, goal_boat = goal_states[i]

        start_state = State(ML=start_M, CL=start_C, boat=start_boat,
                            m_total=M_total, C_total=C_total,
                            boat_capacity=boat_capacity)
        goal_state = State(ML=goal_M, CL=goal_C, boat=goal_boat,
                            m_total=M_total, C_total=C_total,
                            boat_capacity=boat_capacity)

        print(f"\n--- Test case {i + 1} ---")
        solution_path = dfsAlgorithm(start_state, goal_state)
        if solution_path:
            print("Solutions found: \n")
            for step in solution_path:
                print(step)
        else:
            print("No solution found.")

    print("\n[End of DFS algorithm]\n")


if __name__ == "__main__":
    main()
