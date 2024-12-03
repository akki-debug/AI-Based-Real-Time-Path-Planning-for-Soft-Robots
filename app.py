import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import time
from itertools import permutations

# Load icons
robot_icon = Image.open("robot_icon.png")
obstacle_icon = Image.open("obstacle_icon.png")

# Helper: Visualize grid with paths and robot movement
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

    # Draw the path dynamically
    robot_position = start
    for next_position in path[1:]:
        ax.imshow(robot_icon, extent=(robot_position[1], robot_position[1] + 1, robot_position[0], robot_position[0] + 1))

        # Update the arrow visualization as the robot moves
        ax.arrow(robot_position[1] + 0.5, robot_position[0] + 0.5,
                 next_position[1] - robot_position[1], next_position[0] - robot_position[0],
                 head_width=0.2, head_length=0.2, fc="blue", ec="blue")

        st.pyplot(fig)  # Display the current state
        time.sleep(0.5)  # Pause to show movement
        robot_position = next_position
        ax.clear()  # Clear the grid for the next step

        # Redraw the grid, obstacles, start, and goal
        ax.set_xlim(0, grid_size[1])
        ax.set_ylim(0, grid_size[0])
        ax.set_xticks(np.arange(grid_size[1]))
        ax.set_yticks(np.arange(grid_size[0]))
        ax.grid(True)
        for obs in obstacles:
            ax.imshow(obstacle_icon, extent=(obs[1], obs[1] + 1, obs[0], obs[0] + 1))
        ax.text(start[1] + 0.5, start[0] + 0.5, "S", color="green", ha="center", va="center", fontsize=12, weight="bold")
        ax.text(goal[1] + 0.5, goal[0] + 0.5, "G", color="red", ha="center", va="center", fontsize=12, weight="bold")

    # Final position of the robot
    ax.imshow(robot_icon, extent=(robot_position[1], robot_position[1] + 1, robot_position[0], robot_position[0] + 1))
    st.pyplot(fig)

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
    visualize_paths(grid_size, start, goal, obstacles, shortest_path, robot_icon, obstacle_icon)
else:
    st.write("No paths found from start to goal.")

