import random

ACTIONS = ["up", "down", "left", "right"]
ARROWS = {"up": "↑", "down": "↓", "left": "←", "right": "→"}
DELTAS = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}


def generate_random_policy(n, obstacles, start, end):
    """
    Assign a random action to each non-obstacle, non-terminal cell.
    Returns: dict { "r,c": arrow_symbol }
    """
    policy = {}
    obstacle_set = set(map(tuple, obstacles))
    for r in range(n):
        for c in range(n):
            cell = (r, c)
            if cell == tuple(end):
                policy[f"{r},{c}"] = "G"   # Goal
            elif cell in obstacle_set:
                policy[f"{r},{c}"] = "X"   # Obstacle
            else:
                action = random.choice(ACTIONS)
                policy[f"{r},{c}"] = ARROWS[action]
    return policy


def policy_evaluation(n, policy, obstacles, start, end, gamma=0.9, theta=1e-6):
    """
    Iterative Policy Evaluation.
    Reward: -1 per step; reaching end = reward 0 (terminal).
    Returns: dict { "r,c": float }
    """
    obstacle_set = set(map(tuple, obstacles))
    end_t = tuple(end)

    # Map arrow → delta
    arrow_to_delta = {v: DELTAS[k] for k, v in ARROWS.items()}

    # Initialise V
    V = {}
    for r in range(n):
        for c in range(n):
            V[(r, c)] = 0.0

    # Iterative update
    for _ in range(10000):
        delta = 0.0
        for r in range(n):
            for c in range(n):
                cell = (r, c)
                if cell == end_t or cell in obstacle_set:
                    continue

                arrow = policy.get(f"{r},{c}", "↑")
                if arrow not in arrow_to_delta:
                    continue

                dr, dc = arrow_to_delta[arrow]
                nr, nc = r + dr, c + dc

                # Out of bounds or obstacle → stay in place
                if nr < 0 or nr >= n or nc < 0 or nc >= n or (nr, nc) in obstacle_set:
                    nr, nc = r, c

                reward = 0.0 if (nr, nc) == end_t else -1.0
                new_v = reward + gamma * V[(nr, nc)]
                delta = max(delta, abs(new_v - V[cell]))
                V[cell] = new_v

        if delta < theta:
            break

    # Convert to serialisable dict
    return {f"{r},{c}": round(V[(r, c)], 3) for r in range(n) for c in range(n)}
