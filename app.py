import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
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
def plot_robot(grid_size, path, obstacles, robot_icon, obstacle_icon, step):
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

    # Plot the robot's position
    x, y = path[step]
    ax.imshow(robot_icon, extent=(y, y + 1, x, x + 1))

    st.pyplot(fig)

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
st.title("Multi-Scenario Robot Path Visualization")

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

# Display title
st.write(f"### {scenario_name}")

# Use st.empty to dynamically update the output
placeholder = st.empty()

# Animate robot step by step
for step in range(len(path)):
    # Plot the current step of the path
    plot_robot(grid_size, path, obstacles, robot_icon, obstacle_icon, step)

    # Pause for a short period to create the animation effect
    st.time.sleep(0.5)  # Adjust this to control the animation speed
