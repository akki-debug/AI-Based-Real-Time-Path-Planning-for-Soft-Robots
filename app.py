import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import heapq

# Load icons
robot_icon = Image.open("robot_icon.png")  # Add a small robot icon (e.g., 32x32 PNG)
obstacle_icon = Image.open("obstacle_icon.png")  # Add a small obstacle icon (e.g., 32x32 PNG)

# Define scenarios
def get_scenarios():
    return {
        "Scenario 1: Simple Grid": {
            "grid_size": (3, 3),
            "start": (0, 0),
            "goal": (2, 2),
            "obstacles": [(1, 1)],
        },
        "Scenario 2: Medium Complexity": {
            "grid_size": (5, 5),
            "start": (0, 0),
            "goal": (4, 4),
            "obstacles": [(1, 1), (2, 2), (3, 3)],
        },
        "Scenario 3: High Complexity": {
            "grid_size": (7, 7),
            "start": (0, 0),
            "goal": (6, 6),
            "obstacles": [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
        },
    }

# Function to get valid neighbors in the grid
def get_neighbors(node, grid_size, obstacles):
    x, y = node
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid_size[0] and 0 <= ny < grid_size[1] and (nx, ny) not in obstacles:
            neighbors.append((nx, ny))
    return neighbors

# Function to find all paths using DFS
def find_all_paths(grid_size, start, goal, obstacles):
    def dfs(node, path):
        if node == goal:
            paths.append(list(path))
            return
        for neighbor in get_neighbors(node, grid_size, obstacles):
            if neighbor not in path:  # Avoid cycles
                path.append(neighbor)
                dfs(neighbor, path)
                path.pop()

    paths = []
    dfs(start, [start])
    return paths

# Function to find the shortest path using A*
def find_shortest_path(grid_size, start, goal, obstacles):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for neighbor in get_neighbors(current, grid_size, obstacles):
            tentative_g_score = g_score[current] + 1  # Assume uniform cost
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                heapq.heappush(open_set, (tentative_g_score + heuristic(neighbor, goal), neighbor))
    return []

# Visualization
def visualize_paths(grid_size, start, goal, obstacles, path, robot_icon, obstacle_icon):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, grid_size[1])
    ax.set_ylim(0, grid_size[0])
    ax.set_xticks(np.arange(grid_size[1]))
    ax.set_yticks(np.arange(grid_size[0]))
    ax.grid(True)

    # Draw obstacles
    for obs in obstacles:
        ax.imshow(obstacle_icon, extent=(obs[1], obs[1] + 1, obs[0], obs[0] + 1))

    # Draw start and goal
    ax.text(start[1] + 0.5, start[0] + 0.5, "S", color="green", ha="center", va="center", fontsize=12, weight="bold")
    ax.text(goal[1] + 0.5, goal[0] + 0.5, "G", color="red", ha="center", va="center", fontsize=12, weight="bold")

    # Draw path
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        ax.arrow(y1 + 0.5, x1 + 0.5, y2 - y1, x2 - x1, head_width=0.2, head_length=0.2, fc="blue", ec="blue")

    # Draw robot icon at start
    ax.imshow(robot_icon, extent=(start[1], start[1] + 1, start[0], start[0] + 1))

    st.pyplot(fig)

# Streamlit App
st.title("Pathfinding Robot Visualization")

# Select a scenario
scenarios = get_scenarios()
scenario_name = st.selectbox("Choose a Scenario", list(scenarios.keys()))
scenario = scenarios[scenario_name]

grid_size = scenario["grid_size"]
start = scenario["start"]
goal = scenario["goal"]
obstacles = scenario["obstacles"]

st.write(f"### Scenario: {scenario_name}")
st.write(f"Grid Size: {grid_size}, Start: {start}, Goal: {goal}")
st.write("Obstacles:", obstacles)

# Find all paths
st.write("Finding all paths from Start to Goal...")
all_paths = find_all_paths(grid_size, start, goal, obstacles)
st.write(f"Total Paths Found: {len(all_paths)}")
if all_paths:
    st.write("Example Path:", all_paths[0])

# Find the shortest path
shortest_path = find_shortest_path(grid_size, start, goal, obstacles)
st.write("Shortest Path:", shortest_path)

# Visualize the shortest path
if shortest_path:
    st.write("Visualizing the Shortest Path...")
    visualize_paths(grid_size, start, goal, obstacles, shortest_path, robot_icon, obstacle_icon)
