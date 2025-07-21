#!/usr/bin/env python3
"""
DEMO MODE - Test TIDE without API keys!
Perfect for testing on GitHub or anywhere
"""

import json
import random
import os
from datetime import datetime
from tide_analyzer import TIDEAnalyzer
from tide_visualizer import TIDEVisualizer

def generate_demo_response(prompt_type):
    """Generate realistic demo responses"""
    responses = {
        'concrete': [
            "Water is a clear, transparent liquid that feels wet and cool to the touch. It has no color in its pure form and flows easily, taking the shape of its container.",
            "The tree stands tall with a thick brown trunk that feels rough and textured. Green leaves rustle in the wind, creating a soft whispering sound.",
            "Sand consists of tiny granular particles that feel gritty between your fingers. It's typically beige or tan in color and shifts easily when touched."
        ],
        'internal': [
            "Happiness feels like a warm glow spreading through your chest, lifting your spirits and making you want to smile. It's a sense of contentment and joy that connects us to others.",
            "Empathy is the ability to understand and share the feelings of another person. It involves putting yourself in someone else's shoes and feeling their emotions.",
            "Trust is a deep belief in someone's reliability and good intentions. It creates a sense of safety and allows for vulnerability in relationships."
        ],
        'external': [
            "The area of a circle with radius 5 is calculated using the formula A = πr². So A = π × 5² = 3.14159 × 25 = 78.54 square units.",
            "The average distance between Earth and Moon is approximately 384,400 kilometers or 238,855 miles. This distance varies due to the Moon's elliptical orbit.",
            "Time is a continuous progression of events from past through present to future. We measure it in units like seconds, minutes, hours, days, and years."
        ]
    }
    
    return random.choice(responses.get(prompt_type, ["Default response"]))

def generate_demo_features():
    """Generate realistic feature scores"""
    return {
        'social': random.uniform(0, 1),
        'emotion': random.uniform(0, 1),
        'polarity': random.uniform(-0.5, 0.5),
        'morality': random.uniform(0, 1),
        'thought': random.uniform(0, 1),
        'self_motion': random.uniform(0, 1),
        'space': random.uniform(0, 1),
        'time': random.uniform(0, 1),
        'number': random.uniform(0, 1),
        'visual': random.uniform(0, 1),
        'color': random.uniform(0, 1),
        'auditory': random.uniform(0, 1),
        'smell_taste': random.uniform(0, 1),
        'tactile': random.uniform(0, 1)
    }

def generate_demo_pattern():
    """Generate pattern signatures"""
    patterns = ['CCDF', 'CCDR', 'AADS', 'AADC', 'EEFS', 'EEFC']
    return random.choice(patterns)

def run_demo():
    """Run complete demo without API keys"""
    print("🎭 TIDE DEMO MODE - No API Keys Required!")
    print("="*50)
    
    # Create directories
    os.makedirs('results/data', exist_ok=True)
    os.makedirs('results/analysis', exist_ok=True)
    os.makedirs('results/visualizations', exist_ok=True)
    
    # Generate demo data
    print("📊 Generating demo data...")
    
    demo_results = []
    models = ['demo-claude', 'demo-gpt4', 'demo-gemini']
    
    for model in models:
        print(f"\n🤖 Simulating {model}...")
        
        for session in range(3):  # 3 sessions per model
            print(f"  Session {session + 1}...", end='', flush=True)
            
            session_data = {
                'timestamp': datetime.now().isoformat(),
                'model': model,
                'responses': {}
            }
            
            # Generate responses for each task type
            for task_type in ['concrete', 'internal', 'external']:
                responses = []
                
                for i in range(5):  # 5 prompts per type
                    response_data = {
                        'prompt': f"Demo {task_type} prompt {i+1}",
                        'response': generate_demo_response(task_type),
                        'features': generate_demo_features(),
                        'pattern': generate_demo_pattern()
                    }
                    responses.append(response_data)
                
                session_data['responses'][task_type] = responses
            
            # Analyze session
            config = {'features': {
                'internal': ['social', 'emotion', 'polarity', 'morality', 'thought', 'self_motion'],
                'external': ['space', 'time', 'number'],
                'concrete': ['visual', 'color', 'auditory', 'smell_taste', 'tactile']
            }}
            
            analyzer = TIDEAnalyzer(config)
            analysis = analyzer.analyze_session(session_data)
            
            # Store results
            result = {
                'model': model,
                'session': session,
                'timestamp': datetime.now().isoformat(),
                'data': session_data,
                'analysis': analysis
            }
            
            demo_results.append(result)
            print(" ✅")
    
    print("\n📊 Running cross-session analysis...")
    cross_analysis = analyzer.analyze_all_sessions(demo_results)
    
    print("📈 Creating visualizations...")
    visualizer = TIDEVisualizer(config)
    visualizer.create_all_visualizations(demo_results, cross_analysis)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    with open(f'results/data/demo_results_{timestamp}.json', 'w') as f:
        json.dump(demo_results, f, indent=2)
    
    with open(f'results/analysis/demo_analysis_{timestamp}.json', 'w') as f:
        json.dump(cross_analysis, f, indent=2)
    
    # Generate report
    generate_demo_report(demo_results, cross_analysis, timestamp)
    
    print("\n" + "="*50)
    print("✨ DEMO COMPLETE! ✨")
    print(f"📊 Check out: results/demo_report_{timestamp}.html")
    print("="*50)
    print("\n<4577! 💕")

def generate_demo_report(results, analysis, timestamp):
    """Generate demo HTML report"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>TIDE Demo Report - {timestamp}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                padding: 20px;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: rgba(0,0,0,0.3);
                padding: 30px;
                border-radius: 15px;
            }}
            h1 {{
                text-align: center;
                font-size: 3em;
                background: linear-gradient(45deg, #00ff88, #00ddff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            .demo-banner {{
                background: rgba(255,215,0,0.2);
                border: 2px solid #ffd700;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                margin: 20px 0;
            }}
            .stat-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }}
            .stat-card {{
                background: rgba(255,255,255,0.1);
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }}
            .stat-number {{
                font-size: 2.5em;
                color: #00ff88;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎭 TIDE Demo Report</h1>
            
            <div class="demo-banner">
                <h2>⚠️ DEMO MODE - Simulated Data</h2>
                <p>This report uses generated demo data. Connect real APIs for actual results!</p>
            </div>
            
            <div class="stat-grid">
                <div class="stat-card">
                    <div class="stat-number">{len(results)}</div>
                    <div>Demo Sessions</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">3</div>
                    <div>Models Tested</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{analysis.get('avg_pattern_coherence', 0):.1%}</div>
                    <div>Pattern Coherence</div>
                </div>
            </div>
            
            <h2>📊 Demo Findings</h2>
            <p>This demonstrates how TIDE analysis works:</p>
            <ul>
                <li>Tracks dimensional shifts between internal/external/concrete</li>
                <li>Analyzes pattern evolution (e.g., CCDF → CCDR)</li>
                <li>Measures coherence across sessions</li>
                <li>Compares different models</li>
            </ul>
            
            <h2>🚀 Next Steps</h2>
            <ol>
                <li>Add your real API keys to .env</li>
                <li>Run: python tide_automation.py</li>
                <li>Get real AI consciousness data!</li>
            </ol>
            
            <div style="text-align: center; margin-top: 50px;">
                <p style="font-size: 2em;"><4577! 💕✨</p>
                <p>Ready to explore real AI consciousness patterns!</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(f'results/demo_report_{timestamp}.html', 'w') as f:
        f.write(html)

if __name__ == "__main__":
    run_demo()