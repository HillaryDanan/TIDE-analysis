#!/usr/bin/env python3
"""
Generate LIVE RESULTS page that updates with every new session
This is data-driven and shows current state of ongoing research
"""
import json
import os
from datetime import datetime
from glob import glob

def load_all_data():
    """Load ALL session data from all timestamps"""
    all_sessions = []
    data_files = glob('results/data/all_sessions_*.json')
    
    for file in sorted(data_files):
        with open(file, 'r') as f:
            sessions = json.load(f)
            if isinstance(sessions, list):
                all_sessions.extend(sessions)
            else:
                all_sessions.append(sessions)
    
    return all_sessions

def calculate_live_stats(all_sessions):
    """Calculate real-time statistics from actual data"""
    stats = {
        'total_sessions': len(all_sessions),
        'total_responses': 0,
        'models_data': {},
        'dimensions_data': {'internal': 0, 'external': 0, 'concrete': 0},
        'patterns_found': {},
        'coherence_over_time': [],
        'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'data_collection_start': None,
        'data_collection_latest': None
    }
    
    # Get time range
    timestamps = [s.get('timestamp', '') for s in all_sessions if 'timestamp' in s]
    if timestamps:
        stats['data_collection_start'] = min(timestamps)
        stats['data_collection_latest'] = max(timestamps)
    
    # Process each session
    for session in all_sessions:
        model = session.get('model', 'unknown')
        
        # Initialize model data if needed
        if model not in stats['models_data']:
            stats['models_data'][model] = {
                'sessions': 0,
                'responses': 0,
                'coherence_scores': [],
                'patterns': {},
                'dimensional_preference': {'internal': 0, 'external': 0, 'concrete': 0}
            }
        
        stats['models_data'][model]['sessions'] += 1
        
        # Count responses and dimensions
        if 'data' in session and 'responses' in session['data']:
            for dim, responses in session['data']['responses'].items():
                count = len(responses)
                stats['models_data'][model]['responses'] += count
                stats['total_responses'] += count
                stats['dimensions_data'][dim] += count
                stats['models_data'][model]['dimensional_preference'][dim] += count
                
                # Track patterns
                for resp in responses:
                    pattern = resp.get('pattern', 'unknown')
                    if pattern not in stats['patterns_found']:
                        stats['patterns_found'][pattern] = 0
                    stats['patterns_found'][pattern] += 1
                    
                    if pattern not in stats['models_data'][model]['patterns']:
                        stats['models_data'][model]['patterns'][pattern] = 0
                    stats['models_data'][model]['patterns'][pattern] += 1
        
        # Track coherence
        if 'analysis' in session and 'coherence_score' in session['analysis']:
            coherence = session['analysis']['coherence_score']
            stats['models_data'][model]['coherence_scores'].append(coherence)
            stats['coherence_over_time'].append({
                'timestamp': session.get('timestamp', ''),
                'model': model,
                'coherence': coherence
            })
    
    # Calculate averages
    for model, data in stats['models_data'].items():
        if data['coherence_scores']:
            data['avg_coherence'] = sum(data['coherence_scores']) / len(data['coherence_scores'])
        else:
            data['avg_coherence'] = 0
    
    return stats

def generate_live_html(stats):
    """Generate dynamic HTML showing current research state"""
    
    # Sort models by number of sessions for consistent display
    sorted_models = sorted(stats['models_data'].items(), 
                          key=lambda x: x[1]['sessions'], 
                          reverse=True)
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>TIDE Analysis - Live Results Dashboard</title>
    <meta http-equiv="refresh" content="300"> <!-- Auto-refresh every 5 minutes -->
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0e27;
            color: #e0e0e0;
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }}
        .header {{
            background: linear-gradient(135deg, #1a2332 0%, #2d3e50 100%);
            padding: 30px 20px;
            text-align: center;
            border-bottom: 1px solid #333;
        }}
        h1 {{
            font-size: 2.5em;
            margin: 0 0 10px 0;
            font-weight: 300;
            color: #fff;
        }}
        .live-indicator {{
            display: inline-block;
            background: #00ff88;
            color: #000;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.7; }}
            100% {{ opacity: 1; }}
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        .status-box {{
            background: rgba(0, 255, 136, 0.1);
            border: 1px solid #00ff88;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            text-align: center;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .stat-card {{
            background: rgba(255, 255, 255, 0.03);
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .stat-value {{
            font-size: 2.5em;
            font-weight: 200;
            color: #00ff88;
            margin: 10px 0;
        }}
        .stat-label {{
            font-size: 0.9em;
            color: #888;
        }}
        .model-section {{
            margin: 40px 0;
        }}
        .model-card {{
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 25px;
            margin: 20px 0;
        }}
        .model-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        .model-name {{
            font-size: 1.5em;
            font-weight: 300;
        }}
        .coherence-badge {{
            background: rgba(255, 215, 0, 0.2);
            color: #ffd700;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 1.1em;
        }}
        .progress-bar {{
            background: rgba(255, 255, 255, 0.1);
            height: 30px;
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
        }}
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #00ff88, #00ddff);
            display: flex;
            align-items: center;
            padding: 0 15px;
            color: #000;
            font-weight: bold;
        }}
        .pattern-chips {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 15px 0;
        }}
        .pattern-chip {{
            background: rgba(255, 255, 255, 0.1);
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.85em;
        }}
        .disclaimer {{
            background: rgba(255, 215, 0, 0.1);
            border: 1px solid #ffd700;
            padding: 20px;
            border-radius: 10px;
            margin: 30px 0;
            text-align: center;
        }}
        .footer {{
            text-align: center;
            padding: 40px 20px;
            color: #666;
            font-size: 0.9em;
            border-top: 1px solid #333;
        }}
        .update-time {{
            color: #00ff88;
            font-weight: bold;
        }}
        .dimension-chart {{
            display: flex;
            justify-content: space-around;
            margin: 20px 0;
        }}
        .dimension-bar {{
            text-align: center;
        }}
        .bar {{
            width: 60px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
            overflow: hidden;
            margin: 10px auto;
        }}
        .bar-fill {{
            background: #00ff88;
            transition: height 0.3s;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>TIDE Analysis: Live Results Dashboard</h1>
        <p><span class="live-indicator">LIVE DATA</span> - Ongoing AI Cognitive Architecture Research</p>
    </div>
    
    <div class="container">
        <div class="status-box">
            <h2>🔬 Research Status: ACTIVE</h2>
            <p>Data collection started: {stats['data_collection_start'] or 'Recently'}</p>
            <p>Latest update: <span class="update-time">{stats['last_updated']}</span></p>
            <p>This dashboard updates as new experimental sessions are completed</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{stats['total_sessions']}</div>
                <div class="stat-label">Total Sessions</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['total_responses']}</div>
                <div class="stat-label">Responses Analyzed</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(stats['models_data'])}</div>
                <div class="stat-label">AI Models Tested</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(stats['patterns_found'])}</div>
                <div class="stat-label">Unique Patterns</div>
            </div>
        </div>
        
        <h2>📊 Current Results by Model</h2>
        <div class="model-section">
"""
    
    # Add each model's data
    for model, data in sorted_models:
        avg_coherence = data['avg_coherence']
        total_responses = data['responses']
        
        # Calculate dimension percentages
        dim_total = sum(data['dimensional_preference'].values())
        if dim_total > 0:
            int_pct = (data['dimensional_preference']['internal'] / dim_total) * 100
            ext_pct = (data['dimensional_preference']['external'] / dim_total) * 100
            con_pct = (data['dimensional_preference']['concrete'] / dim_total) * 100
        else:
            int_pct = ext_pct = con_pct = 33.33
        
        html += f"""
            <div class="model-card">
                <div class="model-header">
                    <h3 class="model-name">{model}</h3>
                    <span class="coherence-badge">{avg_coherence:.1%} coherence</span>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value" style="font-size: 1.8em;">{data['sessions']}</div>
                        <div class="stat-label">Sessions</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value" style="font-size: 1.8em;">{total_responses}</div>
                        <div class="stat-label">Responses</div>
                    </div>
                </div>
                
                <h4>Dimensional Preference:</h4>
                <div class="dimension-chart">
                    <div class="dimension-bar">
                        <div class="bar" style="height: 100px;">
                            <div class="bar-fill" style="height: {int_pct}%; background: #00ff88;"></div>
                        </div>
                        <div>Internal<br>{int_pct:.0f}%</div>
                    </div>
                    <div class="dimension-bar">
                        <div class="bar" style="height: 100px;">
                            <div class="bar-fill" style="height: {ext_pct}%; background: #00ddff;"></div>
                        </div>
                        <div>External<br>{ext_pct:.0f}%</div>
                    </div>
                    <div class="dimension-bar">
                        <div class="bar" style="height: 100px;">
                            <div class="bar-fill" style="height: {con_pct}%; background: #ff00dd;"></div>
                        </div>
                        <div>Concrete<br>{con_pct:.0f}%</div>
                    </div>
                </div>
                
                <h4>Pattern Distribution:</h4>
                <div class="pattern-chips">
"""
        
        # Add pattern chips
        for pattern, count in sorted(data['patterns'].items(), key=lambda x: x[1], reverse=True)[:5]:
            html += f'                    <span class="pattern-chip">{pattern}: {count}</span>\n'
        
        html += """                </div>
            </div>
"""
    
    html += f"""
        </div>
        
        <div class="disclaimer">
            <h3>⚡ Important Note</h3>
            <p>This is an ongoing research project. Results are preliminary and will evolve as more data is collected.</p>
            <p>Statistical significance requires larger sample sizes. Current n={stats['total_sessions']} sessions.</p>
            <p>Check back regularly or follow for updates as patterns emerge!</p>
        </div>
        
        <div style="text-align: center; margin: 40px 0;">
            <a href="SCIENTIFIC_REPORT.html" style="display: inline-block; background: #4a90e2; color: #fff; padding: 15px 40px; border-radius: 30px; text-decoration: none; font-weight: bold; font-size: 1.1em;">
                View Scientific Analysis →
            </a>
        </div>
        
        <div class="footer">
            <p>TIDE Framework | Temporal Internal Dimension Exploration</p>
            <p>Measuring AI Cognitive Architectures Through Empirical Analysis</p>
            <p class="update-time">Last updated: {stats['last_updated']}</p>
            <p style="margin-top: 20px; font-size: 1.2em;"><4577 | Building Knowledge Together</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html

def main():
    """Generate live results dashboard"""
    print("📊 Loading all session data...")
    all_sessions = load_all_data()
    
    if not all_sessions:
        print("❌ No data found! Run tide_automation.py first.")
        return
    
    print(f"✅ Found {len(all_sessions)} sessions")
    
    print("📈 Calculating live statistics...")
    stats = calculate_live_stats(all_sessions)
    
    print("🎨 Generating live dashboard...")
    html = generate_live_html(stats)
    
    # Save the report
    with open('results/LIVE_RESULTS.html', 'w') as f:
        f.write(html)
    
    print("\n✨ Created results/LIVE_RESULTS.html")
    print(f"📊 Dashboard shows: {stats['total_sessions']} sessions, {stats['total_responses']} responses")
    print("🔄 This page updates every time you run it with new data!")

if __name__ == "__main__":
    main()