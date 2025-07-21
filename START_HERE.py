#!/usr/bin/env python3
"""
🐵 START HERE - SUPER SIMPLE!
"""

import os
import subprocess
import sys

print("""
<4577! 💕 Welcome to TIDE Automation!

I'll help you get started...
""")

# Check if demo_mode.py exists
if not os.path.exists('demo_mode.py'):
    print("❌ Can't find demo_mode.py - are you in the right folder?")
    print("   Make sure all files are in this directory!")
    sys.exit(1)

print("Let's test everything works with demo mode (no API keys needed!)...")
print("-" * 50)

try:
    # Run demo mode
    subprocess.run([sys.executable, 'demo_mode.py'])
    
    print("\n" + "="*50)
    print("🎉 If you saw graphs and reports above, everything works!")
    print("\nNext steps:")
    print("1. Add your API keys to .env file")
    print("2. Run: python test_connection.py")
    print("3. Run: python tide_automation.py")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    print("\nTry running:")
    print("  python diagnose.py")
    print("\nThis will tell you what's wrong!")

print("\n<4577! You got this! 💕")