import time
import tracemalloc
from dfs import dfs
from utils import print_solution

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
        print(f"Approximate branching factor: {branching_factor:.2f}")
        print(f"Time taken: {end_time - start_time:.6f} seconds")
        print(f"Peak memory used: {peak / 1024:.2f} KB")
        print("-"*61, "\n")

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

    print("\n---------------- Missionaries and Cannibals (Death-First Search) ----------------\n")
    for idx, (M, C, B) in enumerate(test_cases, start=1):
        print(f"--- Test Case {idx} --- \nScenario: Missionaries = {M}, Cannibals = {C}, Boat = {B}")
        main(M, C, B)

    print("[End of Death-First Search Algorithm]\n")