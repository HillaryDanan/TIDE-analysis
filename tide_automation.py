#!/usr/bin/env python3
"""
TIDE Automation Script - Based on Hillary's Dissertation
Automates data collection and analysis for AI consciousness patterns
"""

import os
import json
import time
import random
from datetime import datetime
from typing import Dict, List, Any
import pandas as pd
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our modules
from tide_collector import TIDECollector
from tide_analyzer import TIDEAnalyzer
from tide_visualizer import TIDEVisualizer

def load_config():
    """Load configuration from config.json"""
    with open('config.json', 'r') as f:
        return json.load(f)

def create_directories():
    """Create necessary directories for results"""
    dirs = [
        'results',
        'results/data',
        'results/analysis', 
        'results/visualizations',
        'results/checkpoints'
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def run_automated_collection_week():
    """Main automation function - collects and analyzes everything!"""
    
    print("🚀 Starting TIDE Automation!")
    print("="*50)
    
    # Setup
    config = load_config()
    create_directories()
    
    # Initialize components
    collector = TIDECollector(config)
    analyzer = TIDEAnalyzer(config)
    visualizer = TIDEVisualizer(config)
    
    # Get models and sessions from config
    models = config['models']
    sessions_per_model = config['sessions_per_model']
    
    print(f"📊 Will collect {sessions_per_model} sessions from {len(models)} models")
    print(f"📊 Total sessions: {sessions_per_model * len(models)}")
    print("="*50)
    
    all_results = []
    
    # Main collection loop
    for model_idx, model in enumerate(models):
        print(f"\n🤖 Testing Model {model_idx+1}/{len(models)}: {model}")
        print("-"*30)
        
        for session_num in range(sessions_per_model):
            print(f"  📝 Session {session_num+1}/{sessions_per_model}...", end='', flush=True)
            
            try:
                # Collect data
                session_data = collector.run_session(model)
                
                # Analyze immediately
                analysis_results = analyzer.analyze_session(session_data)
                
                # Package results
                full_result = {
                    'model': model,
                    'session': session_num,
                    'timestamp': datetime.now().isoformat(),
                    'data': session_data,
                    'analysis': analysis_results
                }
                
                all_results.append(full_result)
                
                # Save checkpoint (don't lose work!)
                checkpoint_path = f"results/checkpoints/checkpoint_{model}_{session_num}.json"
                with open(checkpoint_path, 'w') as f:
                    json.dump(full_result, f, indent=2)
                
                print(" ✅ Complete!")
                
                # Rate limiting (be nice to APIs)
                if session_num < sessions_per_model - 1:
                    wait_time = config.get('rate_limit_seconds', 60)
                    print(f"  ⏳ Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    
            except Exception as e:
                print(f" ❌ Error: {str(e)}")
                continue
    
    print("\n" + "="*50)
    print("🎉 Data Collection Complete!")
    print("="*50)
    
    # Generate final analysis
    print("\n📊 Generating Final Analysis...")
    
    # Save all raw data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_data_path = f"results/data/all_sessions_{timestamp}.json"
    with open(raw_data_path, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"  💾 Saved raw data: {raw_data_path}")
    
    # Perform cross-session analysis
    print("  🧠 Running cross-session analysis...")
    cross_analysis = analyzer.analyze_all_sessions(all_results)
    
    analysis_path = f"results/analysis/cross_analysis_{timestamp}.json"
    with open(analysis_path, 'w') as f:
        json.dump(cross_analysis, f, indent=2)
    print(f"  💾 Saved analysis: {analysis_path}")
    
    # Generate visualizations
    print("  📈 Creating visualizations...")
    visualizer.create_all_visualizations(all_results, cross_analysis)
    
    # Generate HTML report
    print("  📄 Generating report...")
    generate_html_report(all_results, cross_analysis, timestamp)
    
    print("\n" + "="*50)
    print("✨ ALL DONE! ✨")
    print(f"📊 Check out your results in: results/report_{timestamp}.html")
    print("="*50)
    print("\n<4577! 💕")

def generate_html_report(results, analysis, timestamp):
    """Generate a beautiful HTML report"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>TIDE Analysis Report - {timestamp}</title>
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
            .pattern-signature {{
                font-family: monospace;
                font-size: 1.2em;
                background: rgba(0,0,0,0.3);
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
            }}
            img {{
                max-width: 100%;
                border-radius: 10px;
                margin: 10px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧠 TIDE Analysis Report</h1>
            <h2>Based on Hillary's Dissertation Framework</h2>
            
            <div class="stat-grid">
                <div class="stat-card">
                    <div class="stat-number">{len(results)}</div>
                    <div>Total Sessions</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(set(r['model'] for r in results))}</div>
                    <div>Models Tested</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{analysis.get('avg_pattern_coherence', 0):.1%}</div>
                    <div>Avg Pattern Coherence</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{analysis.get('dimensional_shift_magnitude', 0):.2f}</div>
                    <div>Dimensional Shift Magnitude</div>
                </div>
            </div>
            
            <h2>📊 Key Findings</h2>
            <ul>
                <li>Pattern Evolution: {analysis.get('pattern_evolution', 'CCDF → CCDR')}</li>
                <li>Dominant Processing Mode: {analysis.get('dominant_mode', 'Unknown')}</li>
                <li>Internal/External Balance: {analysis.get('ie_balance', 'Unknown')}</li>
            </ul>
            
            <h2>📈 Visualizations</h2>
            <img src="visualizations/dimensional_shifts.png" alt="Dimensional Shifts">
            <img src="visualizations/pattern_evolution.png" alt="Pattern Evolution">
            <img src="visualizations/feature_trajectories.png" alt="Feature Trajectories">
            
            <h2>🔬 Technical Details</h2>
            <p>Generated: {timestamp}</p>
            <p>Framework: TIDE (Temporal Internal Dimension Exploration)</p>
            <p>Based on: Dissertation semantic dimensions (Internal/External/Concrete)</p>
            
            <div style="text-align: center; margin-top: 50px;">
                <p style="font-size: 2em;"><4577! 💕✨</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    report_path = f"results/report_{timestamp}.html"
    with open(report_path, 'w') as f:
        f.write(html)

if __name__ == "__main__":
    run_automated_collection_week()