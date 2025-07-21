#!/usr/bin/env python3
"""
Quick test to verify the JSON serialization fixes work
"""

import json
import numpy as np
from tide_analyzer import TIDEAnalyzer

def test_json_serialization():
    """Test that our analysis results can be JSON serialized"""
    print("🧪 Testing JSON serialization fixes...")
    
    # Create test data
    test_session = {
        'timestamp': '2024-01-01',
        'model': 'test-model',
        'responses': {
            'concrete': [{
                'prompt': 'test',
                'response': 'test response',
                'features': {f: 0.5 for f in ['visual', 'tactile', 'social', 'emotion']},
                'pattern': 'CCDF'
            }],
            'internal': [{
                'prompt': 'test2',
                'response': 'test response 2',
                'features': {f: 0.7 for f in ['visual', 'tactile', 'social', 'emotion']},
                'pattern': 'AADS'
            }]
        }
    }
    
    # Run analyzer
    config = {
        'features': {
            'internal': ['social', 'emotion'],
            'external': ['space', 'time'],
            'concrete': ['visual', 'tactile']
        }
    }
    
    analyzer = TIDEAnalyzer(config)
    
    try:
        # Analyze session
        results = analyzer.analyze_session(test_session)
        
        # Try to serialize to JSON
        json_str = json.dumps(results, indent=2)
        
        print("✅ JSON serialization successful!")
        print("\nSample output:")
        print(json_str[:500] + "...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_constant_values():
    """Test handling of constant values in correlations"""
    print("\n🧪 Testing constant value handling...")
    
    # Create data with constant values
    test_values = [0.5, 0.5, 0.5, 0.5, 0.5]
    
    config = {'features': {}}
    analyzer = TIDEAnalyzer(config)
    
    try:
        trend = analyzer.calculate_trend(test_values)
        print(f"✅ Constant values handled correctly: trend = '{trend}'")
        return True
    except Exception as e:
        print(f"❌ Error with constant values: {str(e)}")
        return False

def main():
    print("="*50)
    print("🔧 TIDE JSON Serialization Fix Test")
    print("="*50)
    
    test1 = test_json_serialization()
    test2 = test_constant_values()
    
    print("\n" + "="*50)
    if test1 and test2:
        print("🎉 All tests passed! You can now run tide_automation.py")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    print("="*50)
    print("\n<4577! 💕")

if __name__ == "__main__":
    main()