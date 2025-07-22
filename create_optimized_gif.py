#!/usr/bin/env python3
"""
Create optimized GIF for GitHub
"""
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D

print("🎨 Creating optimized GIF...")

with open('results/visualizations/3d_data.json', 'r') as f:
    data = json.load(f)

# Smaller figure size
fig = plt.figure(figsize=(6, 5))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#0a0e27')
fig.patch.set_facecolor('#0a0e27')

def animate(frame):
    ax.clear()
    
    # Use only first session to reduce size
    session = data['sessions'][0]
    
    # Sample points (every 3rd point to reduce complexity)
    points = session['points'][::3]
    
    xs = [p['x'] for p in points]
    ys = [p['y'] for p in points]
    zs = [p['z'] for p in points]
    colors = [p['color'] for p in points]
    
    # Simple pulse effect
    size = 80 * (1 + 0.2 * np.sin(frame * 0.1))
    
    # Plot points
    ax.scatter(xs, ys, zs, c=colors, s=size, alpha=0.8)
    
    # Simple connections
    for i in range(1, len(xs)):
        ax.plot([xs[i-1], xs[i]], [ys[i-1], ys[i]], [zs[i-1], zs[i]], 
                'cyan', alpha=0.3, linewidth=1)
    
    # Minimal labels
    ax.set_xlabel('Internal', color='#00ff88', fontsize=10)
    ax.set_ylabel('External', color='#00ddff', fontsize=10)
    ax.set_zlabel('Concrete', color='#ff00dd', fontsize=10)
    
    # Simple title
    ax.set_title('TIDE Analysis: 74.5% Pattern Coherence', 
                 color='white', fontsize=12)
    
    # Rotate view
    ax.view_init(elev=20, azim=frame*3)
    
    # Remove grid for cleaner look
    ax.grid(False)
    ax.set_xlim(-0.1, 0.3)
    ax.set_ylim(0, 0.5)
    ax.set_zlim(-0.1, 0.3)

# Create animation with fewer frames
anim = FuncAnimation(fig, animate, frames=60, interval=100)

# Save with optimization
writer = PillowWriter(fps=10)
anim.save('docs/visualizations/tide_optimized.gif', writer=writer, dpi=50)

print("✅ Created optimized GIF!")
print("📊 This version is much smaller and GitHub-friendly")