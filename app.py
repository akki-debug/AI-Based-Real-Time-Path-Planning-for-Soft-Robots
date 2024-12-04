import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image
import random

# Load icons for robot and obstacles
robot_icon = Image.open("robot_icon.png")
obstacle_icon = Image.open("obstacle_icon.png")

# Environment class
class ComplexEnvironment:
    def __init__(self, grid_size, start, goal, obstacles):
        self.grid_size = grid_size
        self.start = start
        self.goal = goal
        self.state = start
        self.obstacles = obstacles

    def reset(self):
        self.state = self.start
        return self.state

    def step(self, action):
        x, y = self.state
        if action == 0:  # Up
            x -= 1
        elif action == 1:  # Down
            x += 1
        elif action == 2:  # Left
            y -= 1
        elif action == 3:  # Right
            y += 1

        # Check bounds and obstacles
        if (0 <= x < self.grid_size[0] and 0 <= y < self.grid_size[1]) and (x, y) not in self.obstacles:
            self.state = (x, y)

        done = self.state == self.goal
        return self.state, done

# Random walk for demonstration
def random_walk_path(env):
    path = [env.reset()]
    done = False
    while not done:
        action = np.random.choice(4)  # Random action: 0=Up, 1=Down, 2=Left, 3=Right
        next_state, done = env.step(action)
        path.append(next_state)
    return path

# Visualization function
def animate_robot(grid_size, path, obstacles, robot_icon, obstacle_icon):
    fig, ax = plt.subplots(figsize=(6, 6))

    # Initial grid setup
    ax.set_xlim(0, grid_size[1])
    ax.set_ylim(0, grid_size[0])
    ax.set_xticks(np.arange(grid_size[1]))
    ax.set_yticks(np.arange(grid_size[0]))
    ax.grid(True)

    # Plot obstacles
    for obs in obstacles:
        ax.imshow(obstacle_icon, extent=(obs[1], obs[1] + 1, obs[0], obs[0] + 1))

    robot_plot = ax.imshow(robot_icon, extent=(0, 1, 0, 1))  # Initial robot position

    def update(frame):
        x, y = path[frame]
        robot_plot.set_extent((y, y + 1, x, x + 1))
        return robot_plot,

    ani = FuncAnimation(fig, update, frames=len(path), interval=500, blit=True)
    return ani

# Predefined scenarios
def get_scenarios():
    scenarios = {
        "Scenario 1: Basic (3x3 Grid)": {
            "grid_size": (3, 3),
            "start": (0, 0),
            "goal": (2, 2),
            "obstacles": [(1, 1)],
        },
        "Scenario 2: Medium Complexity (5x5 Grid)": {
            "grid_size": (5, 5),
            "start": (0, 0),
            "goal": (4, 4),
            "obstacles": [(1, 1), (1, 2), (2, 1), (3, 3)],
        },
        "Scenario 3: Large Grid (10x10 with Random Obstacles)": {
            "grid_size": (10, 10),
            "start": (0, 0),
            "goal": (9, 9),
            "obstacles": [(random.randint(1, 9), random.randint(1, 9)) for _ in range(20)],
        },
    }
    return scenarios

# Streamlit UI
st.title("AI-Based-Real-Time-Path-Planning-for-Soft-Robots")

# Select scenario
scenarios = get_scenarios()
scenario_name = st.selectbox("Choose a Scenario", list(scenarios.keys()))
scenario = scenarios[scenario_name]

grid_size = scenario["grid_size"]
start = scenario["start"]
goal = scenario["goal"]
obstacles = scenario["obstacles"]

# Load the environment
env = ComplexEnvironment(grid_size, start, goal, obstacles)

# Generate a random path
path = random_walk_path(env)

# Animate the robot's movement
st.write(f"### {scenario_name}")
ani = animate_robot(grid_size, path, obstacles, robot_icon, obstacle_icon)

# Save the animation as a GIF and display in Streamlit
from matplotlib.animation import PillowWriter

output_path = "robot_animation.gif"
ani.save(output_path, writer=PillowWriter(fps=2))

st.image(output_path)             
