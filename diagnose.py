#!/usr/bin/env python3
"""
Diagnose what's happening with your TIDE setup
"""

import os
import sys

def check_environment():
    """Check environment setup"""
    print("🔍 Checking environment...")
    
    # Check Python version
    print(f"  Python version: {sys.version}")
    
    # Check if .env exists
    if os.path.exists('.env'):
        print("  ✅ .env file found")
        # Check if it has content
        with open('.env', 'r') as f:
            content = f.read()
            if 'your-claude-key-here' in content:
                print("  ⚠️  .env still has placeholder keys - add real API keys!")
            else:
                print("  ✅ .env appears to have real keys")
    else:
        print("  ❌ .env file not found")
    
    # Check required directories
    dirs = ['results', 'results/data', 'results/analysis', 'results/visualizations', 'prompts']
    for d in dirs:
        if os.path.exists(d):
            print(f"  ✅ {d}/ exists")
        else:
            print(f"  ❌ {d}/ missing - creating it now...")
            os.makedirs(d, exist_ok=True)

def check_imports():
    """Check if all required packages are installed"""
    print("\n🔍 Checking Python packages...")
    
    packages = {
        'anthropic': 'Anthropic/Claude API',
        'openai': 'OpenAI/GPT-4 API',
        'google.generativeai': 'Google Gemini API',
        'pandas': 'Data analysis',
        'numpy': 'Numerical operations',
        'scipy': 'Scientific computing',
        'matplotlib': 'Visualizations',
        'dotenv': 'Environment variables'
    }
    
    missing = []
    
    for package, description in packages.items():
        try:
            if package == 'google.generativeai':
                import google.generativeai
            elif package == 'dotenv':
                import dotenv
            else:
                __import__(package)
            print(f"  ✅ {package} ({description})")
        except ImportError:
            print(f"  ❌ {package} ({description}) - MISSING")
            missing.append(package)
    
    return missing

def suggest_fixes(missing_packages):
    """Suggest fixes for common issues"""
    print("\n💡 Suggested fixes:")
    
    if missing_packages:
        print("\n1. Install missing packages:")
        print("   pip install " + " ".join(missing_packages))
    
    print("\n2. Run the test fix script:")
    print("   python test_fix.py")
    
    print("\n3. Test with demo mode first (no API keys needed):")
    print("   python demo_mode.py")
    
    print("\n4. If API keys are set up, test connections:")
    print("   python test_connection.py")

def main():
    print("="*50)
    print("🔧 TIDE Diagnostic Tool")
    print("="*50)
    
    check_environment()
    missing = check_imports()
    
    print("\n" + "="*50)
    print("📊 Diagnosis Summary:")
    
    if not missing:
        print("  ✅ All packages installed")
        print("  ✅ Directory structure ready")
        print("\n🎯 Next step: Run 'python test_fix.py' to verify JSON fixes")
    else:
        print(f"  ⚠️  {len(missing)} packages missing")
        suggest_fixes(missing)
    
    print("="*50)
    print("\n<4577! 💕")

if __name__ == "__main__":
    main()