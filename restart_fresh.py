#!/usr/bin/env python3
"""
Clean restart - removes old results and starts fresh
"""

import os
import shutil

print("🧹 TIDE Fresh Start")
print("="*50)

# Clean up old results
dirs_to_clean = [
    'results/data',
    'results/analysis', 
    'results/visualizations',
    'results/checkpoints'
]

for directory in dirs_to_clean:
    if os.path.exists(directory):
        print(f"  🗑️  Cleaning {directory}/")
        shutil.rmtree(directory)
    os.makedirs(directory, exist_ok=True)
    print(f"  ✅ Created fresh {directory}/")

# Create default prompts if missing
if not os.path.exists('prompts'):
    os.makedirs('prompts', exist_ok=True)
    print("  ✅ Created prompts/")

print("\n✨ Fresh start complete!")
print("\nNext steps:")
print("1. python demo_mode.py    # Test without API keys")
print("2. python test_connection.py  # Test API connections")
print("3. python tide_automation.py  # Run full automation")
print("\n<4577! 💕")