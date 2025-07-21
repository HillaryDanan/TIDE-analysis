#!/usr/bin/env python3
"""
Test API connections before running main automation
"""

import os
from dotenv import load_dotenv
import anthropic
try:
    import openai
except ImportError:
    openai = None
from google import generativeai as genai

# Load environment variables
load_dotenv()

def test_anthropic():
    """Test Anthropic/Claude API"""
    print("🔍 Testing Anthropic (Claude) API...")
    try:
        client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=10,
            messages=[{"role": "user", "content": "Say hello"}]
        )
        print("  ✅ Claude API working!")
        print(f"  Response: {response.content[0].text}")
        return True
    except Exception as e:
        print(f"  ❌ Claude API error: {str(e)}")
        return False

def test_openai():
    """Test OpenAI/GPT-4 API"""
    print("\n🔍 Testing OpenAI (GPT-4) API...")
    try:
        import openai
        api_key = os.getenv('OPENAI_API_KEY')
        
        # Check OpenAI version and use appropriate method
        if hasattr(openai, '__version__') and openai.__version__.startswith('1.'):
            # New version (1.x)
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4",
                max_tokens=10,
                messages=[{"role": "user", "content": "Say hello"}]
            )
            response_text = response.choices[0].message.content
        else:
            # Old version (0.x)
            openai.api_key = api_key
            response = openai.ChatCompletion.create(
                model="gpt-4",
                max_tokens=10,
                messages=[{"role": "user", "content": "Say hello"}]
            )
            response_text = response.choices[0].message.content
            
        print("  ✅ OpenAI API working!")
        print(f"  Response: {response_text}")
        return True
    except Exception as e:
        print(f"  ❌ OpenAI API error: {str(e)}")
        return False

def test_google():
    """Test Google/Gemini API"""
    print("\n🔍 Testing Google (Gemini) API...")
    try:
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Say hello")
        print("  ✅ Gemini API working!")
        print(f"  Response: {response.text}")
        return True
    except Exception as e:
        print(f"  ❌ Gemini API error: {str(e)}")
        return False

def check_environment():
    """Check if all required environment variables are set"""
    print("🔍 Checking environment variables...")
    
    required_vars = ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'GOOGLE_API_KEY']
    missing = []
    
    for var in required_vars:
        if os.getenv(var):
            print(f"  ✅ {var} is set")
        else:
            print(f"  ❌ {var} is missing")
            missing.append(var)
            
    return len(missing) == 0

def main():
    print("="*50)
    print("🚀 TIDE API Connection Test")
    print("="*50)
    
    # Check environment
    env_ok = check_environment()
    
    if not env_ok:
        print("\n⚠️  Please set missing environment variables in .env file!")
        return
        
    # Test each API
    anthropic_ok = test_anthropic()
    openai_ok = test_openai()
    google_ok = test_google()
    
    print("\n" + "="*50)
    print("📊 Summary:")
    print(f"  Anthropic/Claude: {'✅ Working' if anthropic_ok else '❌ Failed'}")
    print(f"  OpenAI/GPT-4: {'✅ Working' if openai_ok else '❌ Failed'}")
    print(f"  Google/Gemini: {'✅ Working' if google_ok else '❌ Failed'}")
    
    if anthropic_ok and openai_ok and google_ok:
        print("\n🎉 All APIs working! You're ready to run tide_automation.py")
    else:
        print("\n⚠️  Fix the failed APIs before running automation")
        
    print("="*50)
    print("\n<4577! 💕")

if __name__ == "__main__":
    main()