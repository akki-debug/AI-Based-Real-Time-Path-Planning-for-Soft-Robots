import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import time

# Load icons
robot_icon = Image.open("robot_icon.png")
obstacle_icon = Image.open("obstacle_icon.png")

# Helper: Visualize grid with robot movement in real-time
def visualize_realtime(grid_size, start, goal, obstacles, path, robot_icon, obstacle_icon):
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

    # Robot's real-time movement
    for i, position in enumerate(path):
        ax.imshow(robot_icon, extent=(position[1], position[1] + 1, position[0], position[0] + 1))
        st.pyplot(fig)  # Update plot in Streamlit
        if i < len(path) - 1:
            time.sleep(0.5)  # Pause to simulate movement
            ax.clear()  # Clear the previous state of the grid
            ax.set_xlim(0, grid_size[1])
            ax.set_ylim(0, grid_size[0])
            ax.set_xticks(np.arange(grid_size[1]))
            ax.set_yticks(np.arange(grid_size[0]))
            ax.grid(True)

            # Redraw the grid with obstacles
            for obs in obstacles:
                ax.imshow(obstacle_icon, extent=(obs[1], obs[1] + 1, obs[0], obs[0] + 1))
            ax.text(start[1] + 0.5, start[0] + 0.5, "S", color="green", ha="center", va="center", fontsize=12, weight="bold")
            ax.text(goal[1] + 0.5, goal[0] + 0.5, "G", color="red", ha="center", va="center", fontsize=12, weight="bold")

# Helper: Find all paths and the shortest path
def find_paths(grid_size, start, goal, obstacles):
    queue = [(start, [start])]
    visited = set()
    paths = []

    while queue:
        current, path = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            paths.append(path)
            continue

        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_step = (x + dx, y + dy)
            if 0 <= next_step[0] < grid_size[0] and 0 <= next_step[1] < grid_size[1]:
                if next_step not in obstacles and next_step not in path:
                    queue.append((next_step, path + [next_step]))

    shortest_path = min(paths, key=len) if paths else None
    return paths, shortest_path

# Scenarios
def scenario_1():
    return (3, 3), (0, 0), (2, 2), [(1, 1)]

def scenario_2():
    return (5, 5), (0, 0), (4, 4), [(1, 1), (2, 2), (3, 3)]

def scenario_3():
    return (7, 7), (0, 0), (6, 6), [(2, 2), (3, 3), (4, 4), (5, 5)]

# Streamlit App
st.title("AI-Based Real-Time Path Planning for Robots")

# Select Scenario
scenario = st.selectbox("Choose a Scenario", ["Scenario 1", "Scenario 2", "Scenario 3"])

# Get scenario details
if scenario == "Scenario 1":
    grid_size, start, goal, obstacles = scenario_1()
elif scenario == "Scenario 2":
    grid_size, start, goal, obstacles = scenario_2()
else:
    grid_size, start, goal, obstacles = scenario_3()

# Display grid information
st.write(f"**Grid Size:** {grid_size}")
st.write(f"**Start Position:** {start}")
st.write(f"**Goal Position:** {goal}")
st.write(f"**Obstacles:** {obstacles}")

# Find paths and visualize
paths, shortest_path = find_paths(grid_size, start, goal, obstacles)

if paths:
    st.write(f"**Number of Paths Found:** {len(paths)}")
    st.write(f"**Shortest Path:** {shortest_path}")
    visualize_realtime(grid_size, start, goal, obstacles, shortest_path, robot_icon, obstacle_icon)
else:
    st.write("No paths found from start to goal.")

