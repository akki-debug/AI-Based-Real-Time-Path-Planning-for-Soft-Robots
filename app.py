import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import time
import random

# Load robot and obstacle icons
robot_icon = Image.open("robot_icon.png")
obstacle_icon = Image.open("obstacle_icon.png")

# Helper: Display a single grid with the robot moving
def display_grid_with_robot(grid_size, start, goal, path, obstacles, robot_icon):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, grid_size[1])
    ax.set_ylim(0, grid_size[0])
    ax.set_xticks(np.arange(grid_size[1]))
    ax.set_yticks(np.arange(grid_size[0]))
    ax.grid(True)
    ax.set_aspect('equal')

    # Draw obstacles
    for obs in obstacles:
        ax.imshow(obstacle_icon, extent=(obs[1], obs[1] + 1, obs[0], obs[0] + 1))

    # Draw start and goal
    ax.text(start[1] + 0.5, start[0] + 0.5, "S", color="green", ha="center", va="center", fontsize=12, weight="bold")
    ax.text(goal[1] + 0.5, goal[0] + 0.5, "G", color="red", ha="center", va="center", fontsize=12, weight="bold")

    for step in path:
        ax.clear()  # Clear the previous state
        ax.set_xlim(0, grid_size[1])
        ax.set_ylim(0, grid_size[0])
        ax.set_xticks(np.arange(grid_size[1]))
        ax.set_yticks(np.arange(grid_size[0]))
        ax.grid(True)
        ax.set_aspect('equal')

        # Draw obstacles
        for obs in obstacles:
            ax.imshow(obstacle_icon, extent=(obs[1], obs[1] + 1, obs[0], obs[0] + 1))

        # Redraw start and goal
        ax.text(start[1] + 0.5, start[0] + 0.5, "S", color="green", ha="center", va="center", fontsize=12, weight="bold")
        ax.text(goal[1] + 0.5, goal[0] + 0.5, "G", color="red", ha="center", va="center", fontsize=12, weight="bold")

        # Draw robot
        ax.imshow(robot_icon, extent=(step[1], step[1] + 1, step[0], step[0] + 1))

        # Show the plot
        st.pyplot(fig)
        time.sleep(0.5)  # Delay to simulate walking

# Function to generate random obstacles
def generate_random_obstacles(grid_size, num_obstacles):
    obstacles = []
    while len(obstacles) < num_obstacles:
        obs = (random.randint(0, grid_size[0] - 1), random.randint(0, grid_size[1] - 1))
        if obs not in obstacles:
            obstacles.append(obs)
    return obstacles

# Simple pathfinding for demonstration (replace with actual algorithm for a real app)
def find_simple_path(start, goal, obstacles):
    # Just return a hardcoded path for demonstration
    # In a real scenario, a pathfinding algorithm like A* should be used.
    return [start, (0, 1), (0, 2), (1, 2), goal]

# Streamlit App
st.title("Real-Time Walking Robot")

# Scenario selection
scenario = st.selectbox("Select a Scenario", ["Scenario 1: 5x5 Grid", "Scenario 2: 7x7 Grid with Obstacles", "Scenario 3: 10x10 Complex Grid"])

# Based on the selected scenario, set up the grid size, obstacles, and robot path
if scenario == "Scenario 1: 5x5 Grid":
    grid_size = (5, 5)
    start = (0, 0)
    goal = (4, 4)
    obstacles = [(1, 1), (1, 2), (2, 1)]  # Example simple obstacles
    path = find_simple_path(start, goal, obstacles)
elif scenario == "Scenario 2: 7x7 Grid with Obstacles":
    grid_size = (7, 7)
    start = (0, 0)
    goal = (6, 6)
    obstacles = generate_random_obstacles(grid_size, 10)  # Generate 10 random obstacles
    path = find_simple_path(start, goal, obstacles)
elif scenario == "Scenario 3: 10x10 Complex Grid":
    grid_size = (10, 10)
    start = (0, 0)
    goal = (9, 9)
    obstacles = generate_random_obstacles(grid_size, 20)  # Generate 20 random obstacles
    path = find_simple_path(start, goal, obstacles)

# Display scenario information
st.write(f"**Grid Size:** {grid_size}")
st.write(f"**Start Position:** {start}")
st.write(f"**Goal Position:** {goal}")
st.write(f"**Obstacles:** {obstacles}")
st.write(f"**Path Taken:** {path}")

# Display the grid and simulate walking
if st.button("Start Robot Walk"):
    display_grid_with_robot(grid_size, start, goal, path, obstacles, robot_icon)

