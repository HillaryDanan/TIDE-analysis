#!/usr/bin/env python3
"""
Setup TIDE to use only Gemini (since it's working!)
"""

import json

def create_gemini_config():
    """Create config for Gemini-only testing"""
    config = {
        "models": [
            "gemini-1.5-flash"  # Only use the working model!
        ],
        "sessions_per_model": 3,  # Run 3 sessions
        "rate_limit_seconds": 2,  # Gemini is fast, minimal delay needed
        "prompts_per_task": 5,  # 5 prompts per dimension
        "features": {
            "internal": ["social", "emotion", "polarity", "morality", "thought", "self_motion"],
            "external": ["space", "time", "number"],
            "concrete": ["visual", "color", "auditory", "smell_taste", "tactile"]
        }
    }
    
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Updated config.json to use only Gemini!")
    print("   - Will test 3 sessions")
    print("   - 5 prompts per dimension (internal/external/concrete)")
    print("   - Total: 45 prompts across all sessions")

def fix_collector_for_gemini():
    """Make sure tide_collector.py uses the right Gemini model"""
    with open('tide_collector.py', 'r') as f:
        content = f.read()
    
    # Fix Gemini model name
    content = content.replace("gemini-pro", "gemini-1.5-flash")
    
    with open('tide_collector.py', 'w') as f:
        f.write(content)
    
    print("✅ Updated tide_collector.py for Gemini 1.5 Flash")

def main():
    print("🚀 Setting up TIDE for Gemini-only testing")
    print("="*50)
    
    create_gemini_config()
    fix_collector_for_gemini()
    
    print("\n🎯 You're ready! Run these commands:")
    print("\n1. Test with demo data first:")
    print("   python demo_mode.py")
    print("\n2. Then run real analysis with Gemini:")
    print("   python tide_automation.py")
    print("\n💡 This will analyze Gemini's consciousness patterns!")
    print("="*50)

if __name__ == "__main__":
    main()