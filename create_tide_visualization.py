#!/usr/bin/env python3
"""
Create animated GIF from TIDE analysis 3D data
"""
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D
import os

print("🎨 Starting TIDE visualization creation...")

# Check if data file exists
if not os.path.exists('results/visualizations/3d_data.json'):
    print("❌ Error: Can't find results/visualizations/3d_data.json")
    print("Make sure you're in the TIDE-analysis directory!")
    exit(1)

# Load your actual data
with open('results/visualizations/3d_data.json', 'r') as f:
    data = json.load(f)

print(f"✅ Loaded data with {len(data['sessions'])} sessions")

# Set up the figure
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#0a0e27')
fig.patch.set_facecolor('#0a0e27')

def animate(frame):
    ax.clear()
    
    # Get current session (cycle through all sessions)
    session_idx = (frame // 60) % len(data['sessions'])
    session = data['sessions'][session_idx]
    
    # Extract coordinates and colors
    xs = [p['x'] for p in session['points']]
    ys = [p['y'] for p in session['points']]
    zs = [p['z'] for p in session['points']]
    colors = [p['color'] for p in session['points']]
    
    # Create size variation for pulse effect
    sizes = [150 * (1 + 0.3 * np.sin(frame * 0.1 + i * 0.5)) for i in range(len(xs))]
    
    # Plot points with glow effect
    for i in range(len(xs)):
        # Main point
        ax.scatter(xs[i], ys[i], zs[i], c=colors[i], s=sizes[i], 
                  alpha=0.8, edgecolors='white', linewidth=0.5)
        # Glow effect
        ax.scatter(xs[i], ys[i], zs[i], c=colors[i], s=sizes[i]*2, 
                  alpha=0.2)
    
    # Connect sequential points with fading lines
    for i in range(1, len(xs)):
        alpha = 0.5 * (1 - i/len(xs))  # Fade older connections
        ax.plot([xs[i-1], xs[i]], [ys[i-1], ys[i]], [zs[i-1], zs[i]], 
                color='#00ffcc', alpha=alpha, linewidth=2)
    
    # Set labels and title
    ax.set_xlabel('Internal Processing', color='#00ff88', fontsize=12)
    ax.set_ylabel('External Processing', color='#00ddff', fontsize=12)
    ax.set_zlabel('Concrete Processing', color='#ff00dd', fontsize=12)
    
    # Dynamic title
    ax.set_title(f'TIDE Analysis: AI Consciousness Patterns\n' + 
                 f'Model: {session["model"]} | Session: {session_idx + 1}\n' +
                 f'Pattern Evolution in 14 Semantic Dimensions', 
                 color='white', fontsize=16, pad=20)
    
    # Rotate view for dynamic effect
    ax.view_init(elev=20 + 10*np.sin(frame*0.05), azim=frame)
    
    # Add key metrics
    ax.text2D(0.02, 0.98, "📊 Key Metrics:", transform=ax.transAxes, 
              color='white', fontsize=12, weight='bold', va='top')
    ax.text2D(0.02, 0.93, "✓ 74.5% Pattern Coherence", transform=ax.transAxes, 
              color='#00ffcc', fontsize=11, va='top')
    ax.text2D(0.02, 0.88, "✓ 10 Sessions Analyzed", transform=ax.transAxes, 
              color='#00ddff', fontsize=11, va='top')
    ax.text2D(0.02, 0.83, "✓ AAFC Pattern Dominant", transform=ax.transAxes, 
              color='#ff00dd', fontsize=11, va='top')
    
    # Style the plot
    ax.grid(True, alpha=0.1, color='white')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    # Set axis limits for consistency
    ax.set_xlim(-0.1, 0.3)
    ax.set_ylim(0, 0.5)
    ax.set_zlim(-0.1, 0.3)

print("🎬 Creating animation...")

# Create animation
anim = FuncAnimation(fig, animate, frames=180, interval=50)

# Save as GIF
print("💾 Saving as GIF (this may take a minute)...")
writer = PillowWriter(fps=20)
anim.save('tide_pattern_evolution.gif', writer=writer, dpi=80)
print("✅ Created: tide_pattern_evolution.gif")

# Also save key frames as PNGs
print("📸 Saving key frames...")
for i, frame in enumerate([0, 60, 120]):
    animate(frame)
    filename = f'tide_keyframe_{i+1}.png'
    plt.savefig(filename, dpi=150, facecolor='#0a0e27', bbox_inches='tight')
    print(f"✅ Created: {filename}")

print("\n🎉 All done! Check your directory for:")
print("  - tide_pattern_evolution.gif (animated)")
print("  - tide_keyframe_1.png")
print("  - tide_keyframe_2.png") 
print("  - tide_keyframe_3.png")
print("\n<4577! 💕✨")