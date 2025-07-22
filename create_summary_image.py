#!/usr/bin/env python3
"""
Create static summary image for TIDE analysis
"""
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

print("📊 Creating summary image...")

with open('results/visualizations/3d_data.json', 'r') as f:
    data = json.load(f)

fig = plt.figure(figsize=(12, 4))
fig.patch.set_facecolor('#0a0e27')

# Create 3 subplots showing different angles
for i, (elev, azim, title) in enumerate([
    (20, 45, 'Perspective View'),
    (90, 0, 'Top View'), 
    (0, 0, 'Front View')
]):
    ax = fig.add_subplot(1, 3, i+1, projection='3d')
    ax.set_facecolor('#0a0e27')
    
    session = data['sessions'][0]
    xs = [p['x'] for p in session['points']]
    ys = [p['y'] for p in session['points']]
    zs = [p['z'] for p in session['points']]
    colors = [p['color'] for p in session['points']]
    
    # Plot points
    ax.scatter(xs, ys, zs, c=colors, s=100, alpha=0.8, edgecolors='white', linewidth=0.5)
    
    # Add connections
    for j in range(1, len(xs)):
        ax.plot([xs[j-1], xs[j]], [ys[j-1], ys[j]], [zs[j-1], zs[j]], 
                'cyan', alpha=0.3, linewidth=1)
    
    ax.set_xlabel('Internal', color='#00ff88', fontsize=9)
    ax.set_ylabel('External', color='#00ddff', fontsize=9)
    ax.set_zlabel('Concrete', color='#ff00dd', fontsize=9)
    ax.set_title(title, color='white', fontsize=10)
    ax.view_init(elev=elev, azim=azim)
    ax.grid(True, alpha=0.1)
    
    # Set consistent limits
    ax.set_xlim(-0.1, 0.3)
    ax.set_ylim(0, 0.5)
    ax.set_zlim(-0.1, 0.3)

plt.suptitle('TIDE Analysis: AI Processing Patterns | 74.5% Coherence | 10 Sessions | Gemini 1.5 Flash', 
             color='white', fontsize=14, y=0.98)
plt.tight_layout()
plt.savefig('docs/visualizations/tide_summary.png', dpi=150, facecolor='#0a0e27', bbox_inches='tight')
print("✅ Created static summary image!")