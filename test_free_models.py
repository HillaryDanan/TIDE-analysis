#!/usr/bin/env python3
"""
Test with free/accessible models
"""

import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

def test_gpt35():
    """Test GPT-3.5 which is cheaper and more accessible"""
    print("🔍 Testing OpenAI (GPT-3.5-turbo) API...")
    try:
        import openai
        from openai import OpenAI
        
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # This model is more accessible
            max_tokens=10,
            messages=[{"role": "user", "content": "Say hello"}]
        )
        print("  ✅ GPT-3.5-turbo API working!")
        print(f"  Response: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"  ❌ OpenAI API error: {str(e)}")
        return False

def test_gemini_flash():
    """Test Gemini Flash (free tier available)"""
    print("\n🔍 Testing Google (Gemini 1.5 Flash) API...")
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        model = genai.GenerativeModel('gemini-1.5-flash')  # Free tier model
        response = model.generate_content("Say hello")
        print("  ✅ Gemini 1.5 Flash API working!")
        print(f"  Response: {response.text}")
        return True
    except Exception as e:
        print(f"  ❌ Gemini API error: {str(e)}")
        return False

def update_config_for_free_models():
    """Update config to use accessible models"""
    config_updates = {
        "models": [
            "gpt-3.5-turbo",
            "gemini-1.5-flash"
        ],
        "sessions_per_model": 2,  # Start small
        "rate_limit_seconds": 30,  # Faster for testing
        "prompts_per_task": 5,  # Fewer prompts to save credits
        "features": {
            "internal": ["social", "emotion", "polarity", "morality", "thought", "self_motion"],
            "external": ["space", "time", "number"],
            "concrete": ["visual", "color", "auditory", "smell_taste", "tactile"]
        }
    }
    
    with open('config.json', 'w') as f:
        json.dump(config_updates, f, indent=2)
    
    print("\n✅ Updated config.json to use free/accessible models")

def main():
    print("="*50)
    print("🆓 Testing Free/Accessible Models")
    print("="*50)
    
    # Test what works
    gpt_ok = test_gpt35()
    gemini_ok = test_gemini_flash()
    
    if gpt_ok or gemini_ok:
        print("\n🎉 At least one model works!")
        update_config_for_free_models()
        print("\nYou can now run:")
        print("  python tide_automation.py")
        print("\nThis will use only the working models!")
    else:
        print("\n😕 No models working yet. Check:")
        print("1. OpenAI: Make sure you have ANY credits (even $1)")
        print("2. Google: Make sure API key is correct")
        
    print("="*50)

if __name__ == "__main__":
    main()