import matplotlib
matplotlib.use('TkAgg')  # Important for some backends

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

path = 'points.npy'

all_points = np.load(path)

lines = [(0, 1), (1, 2), (1, 3), (1, 6), (2, 4),
         (3, 5), (6, 7), (6, 8), (7, 9), (8, 10)]

fig, ax = plt.subplots()
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)


# 1. Create scatter plot OUTSIDE the update function
scatter, = ax.plot([], [], 'bo', lw=2)   # Use 'plot' for scatter


line_objects = [ax.plot([], [], 'r-', lw=2)[0] for _ in lines]  # Red lines

def update(frame):
    current_points = all_points[frame]

    # 2. Update scatter plot data
    scatter.set_data(current_points[:, 0], current_points[:, 1])


    for i, (start, end) in enumerate(lines):
        line_objects[i].set_data([current_points[start][0], current_points[end][0]],
                                 [current_points[start][1], current_points[end][1]])

    # 3. Return both scatter and lines
    return [scatter] + line_objects



ani = animation.FuncAnimation(fig, update, frames=len(all_points), interval=33.333, blit=True) # Slower frame rate for better visualization

plt.show()
