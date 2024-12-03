import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Simple 3x3 Environment Setup
class SimpleEnvironment:
    def __init__(self, grid_size, obstacles, start, goal):
        self.grid_size = grid_size
        self.obstacles = obstacles
        self.start = start
        self.goal = goal
        self.state = start

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

        reward = 1 if self.state == self.goal else -1
        done = self.state == self.goal
        return self.state, reward, done

    def render(self, path):
        grid = np.zeros(self.grid_size)
        for obs in self.obstacles:
            grid[obs] = -1
        grid[self.goal] = 2
        for step in path:
            grid[step] = 0.5
        grid[self.start] = 1
        return grid


# Streamlit Interface
st.title("3x3 Robot Path Planning Demo")

# Define the grid and environment
grid_size = (3, 3)
obstacles = [(1, 1)]
start = (0, 0)
goal = (2, 2)

env = SimpleEnvironment(grid_size, obstacles, start, goal)

# Path Planning Algorithm (Random Walk for Demo)
def random_walk_path(env):
    path = [env.reset()]
    done = False
    while not done:
        action = np.random.choice(4)  # Random action: 0=Up, 1=Down, 2=Left, 3=Right
        next_state, _, done = env.step(action)
        path.append(next_state)
    return path

# Generate the path
path = random_walk_path(env)

# Visualize the environment with path
grid = env.render(path)

# Plot the grid
fig, ax = plt.subplots(figsize=(5, 5))
sns.heatmap(grid, annot=True, fmt=".1f", cmap="coolwarm", cbar=False, linewidths=0.5, linecolor="black", ax=ax)
ax.set_title("Robot Path Visualization")
st.pyplot(fig)
