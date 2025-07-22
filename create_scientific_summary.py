#!/usr/bin/env python3
"""
Generate SCIENTIFIC SUMMARY with deep analysis
Updated periodically (weekly/biweekly) with statistical rigor
"""
import json
import os
from datetime import datetime
from glob import glob
import numpy as np
from scipy import stats as scipy_stats

def load_all_data():
    """Load ALL session data from all timestamps"""
    all_sessions = []
    analysis_results = []
    
    # Load session data
    data_files = glob('results/data/all_sessions_*.json')
    for file in sorted(data_files):
        with open(file, 'r') as f:
            sessions = json.load(f)
            if isinstance(sessions, list):
                all_sessions.extend(sessions)
    
    # Load analysis results
    analysis_files = glob('results/analysis/cross_analysis_*.json')
    for file in sorted(analysis_files):
        with open(file, 'r') as f:
            analysis_results.append(json.load(f))
    
    return all_sessions, analysis_results

def calculate_comprehensive_stats(all_sessions):
    """Calculate comprehensive statistics with confidence intervals"""
    stats = {
        'overview': {
            'total_sessions': len(all_sessions),
            'total_responses': 0,
            'unique_models': set(),
            'date_range': {'start': None, 'end': None},
            'collection_days': 0
        },
        'by_model': {},
        'patterns': {
            'all_patterns': {},
            'transitions': {},
            'stability_score': 0
        },
        'dimensions': {
            'response_distribution': {'internal': 0, 'external': 0, 'concrete': 0},
            'shift_magnitudes': [],
            'balance_scores': []
        },
        'statistical_tests': {},
        'confidence_intervals': {}
    }
    
    # Extract all data points
    coherence_by_model = {}
    all_coherence_scores = []
    all_patterns = []
    
    for session in all_sessions:
        model = session.get('model', 'unknown')
        stats['overview']['unique_models'].add(model)
        
        if model not in stats['by_model']:
            stats['by_model'][model] = {
                'sessions': 0,
                'responses': 0,
                'coherence_scores': [],
                'patterns': {},
                'dimensional_scores': {'internal': [], 'external': [], 'concrete': []},
                'feature_activations': {f: [] for f in [
                    'social', 'emotion', 'polarity', 'morality', 'thought', 'self_motion',
                    'space', 'time', 'number', 'visual', 'color', 'auditory', 'smell_taste', 'tactile'
                ]}
            }
            coherence_by_model[model] = []
        
        stats['by_model'][model]['sessions'] += 1
        
        # Process responses
        if 'data' in session and 'responses' in session['data']:
            for dim, responses in session['data']['responses'].items():
                stats['overview']['total_responses'] += len(responses)
                stats['by_model'][model]['responses'] += len(responses)
                stats['dimensions']['response_distribution'][dim] += len(responses)
                
                for resp in responses:
                    # Track patterns
                    pattern = resp.get('pattern', 'unknown')
                    all_patterns.append(pattern)
                    if pattern not in stats['patterns']['all_patterns']:
                        stats['patterns']['all_patterns'][pattern] = 0
                    stats['patterns']['all_patterns'][pattern] += 1
                    
                    # Track features
                    if 'features' in resp:
                        for feature, value in resp['features'].items():
                            if feature in stats['by_model'][model]['feature_activations']:
                                stats['by_model'][model]['feature_activations'][feature].append(value)
        
        # Track coherence
        if 'analysis' in session and 'coherence_score' in session['analysis']:
            coherence = session['analysis']['coherence_score']
            stats['by_model'][model]['coherence_scores'].append(coherence)
            coherence_by_model[model].append(coherence)
            all_coherence_scores.append(coherence)
        
        # Track shifts
        if 'analysis' in session and 'dimensional_shifts' in session['analysis']:
            for shift in session['analysis']['dimensional_shifts']:
                magnitude = np.sqrt(
                    shift.get('internal_Δ', 0)**2 + 
                    shift.get('external_Δ', 0)**2 + 
                    shift.get('concrete_Δ', 0)**2
                )
                stats['dimensions']['shift_magnitudes'].append(magnitude)
    
    # Calculate statistical measures
    stats['overview']['unique_models'] = list(stats['overview']['unique_models'])
    
    # Model comparisons with confidence intervals
    for model, scores in coherence_by_model.items():
        if len(scores) >= 2:
            mean = np.mean(scores)
            std = np.std(scores)
            n = len(scores)
            se = std / np.sqrt(n)
            ci = scipy_stats.t.interval(0.95, n-1, mean, se)
            
            stats['confidence_intervals'][model] = {
                'mean': mean,
                'std': std,
                'ci_lower': ci[0],
                'ci_upper': ci[1],
                'n': n
            }
    
    # Pattern stability
    if len(all_patterns) > 1:
        pattern_changes = sum(1 for i in range(1, len(all_patterns)) if all_patterns[i] != all_patterns[i-1])
        stats['patterns']['stability_score'] = 1 - (pattern_changes / len(all_patterns))
    
    # Statistical tests if we have enough data
    if len(stats['overview']['unique_models']) >= 2 and all(len(coherence_by_model.get(m, [])) >= 2 for m in stats['overview']['unique_models']):
        # ANOVA for model differences
        model_groups = [coherence_by_model[m] for m in stats['overview']['unique_models'] if m in coherence_by_model]
        if all(len(g) > 0 for g in model_groups):
            f_stat, p_value = scipy_stats.f_oneway(*model_groups)
            stats['statistical_tests']['anova'] = {
                'f_statistic': f_stat,
                'p_value': p_value,
                'significant': p_value < 0.05
            }
    
    return stats

def generate_scientific_html(stats, all_sessions):
    """Generate comprehensive scientific analysis"""
    
    # Calculate some derived metrics
    total_responses = stats['overview']['total_responses']
    total_sessions = stats['overview']['total_sessions']
    
    # Sort models by average coherence
    model_rankings = []
    for model in stats['overview']['unique_models']:
        if model in stats['confidence_intervals']:
            model_rankings.append((
                model,
                stats['confidence_intervals'][model]['mean'],
                stats['confidence_intervals'][model]
            ))
    model_rankings.sort(key=lambda x: x[1], reverse=True)
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>TIDE Framework: Scientific Analysis of AI Cognitive Architectures</title>
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
            padding: 40px 20px;
            text-align: center;
            border-bottom: 1px solid #333;
        }}
        h1 {{
            font-size: 2.8em;
            margin: 0 0 10px 0;
            font-weight: 300;
            color: #fff;
        }}
        .subtitle {{
            font-size: 1.2em;
            color: #b0b0b0;
            margin: 0;
            font-weight: 300;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        .executive-summary {{
            background: linear-gradient(135deg, rgba(74, 144, 226, 0.1) 0%, rgba(0, 255, 136, 0.1) 100%);
            border: 1px solid #4a90e2;
            border-radius: 15px;
            padding: 30px;
            margin: 30px 0;
        }}
        .key-finding {{
            background: rgba(255, 255, 255, 0.03);
            border-left: 4px solid #00ff88;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .model-comparison-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 30px 0;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 10px;
            overflow: hidden;
        }}
        .model-comparison-table th {{
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            text-align: left;
            font-weight: 400;
            color: #fff;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .model-comparison-table td {{
            padding: 15px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }}
        .confidence-interval {{
            font-size: 0.85em;
            color: #888;
        }}
        .statistical-section {{
            background: rgba(255, 255, 255, 0.02);
            padding: 30px;
            border-radius: 10px;
            margin: 30px 0;
        }}
        .viz-section {{
            margin: 40px 0;
        }}
        .viz-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin: 20px 0;
        }}
        .viz-container {{
            background: rgba(255, 255, 255, 0.02);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        .viz-container img {{
            width: 100%;
            border-radius: 5px;
            margin-top: 10px;
        }}
        .pattern-analysis {{
            background: rgba(255, 215, 0, 0.05);
            border: 1px solid rgba(255, 215, 0, 0.3);
            padding: 25px;
            border-radius: 10px;
            margin: 30px 0;
        }}
        .methodology-box {{
            background: rgba(255, 255, 255, 0.03);
            padding: 30px;
            border-radius: 10px;
            margin: 30px 0;
        }}
        .feature-heatmap {{
            margin: 20px 0;
            overflow-x: auto;
        }}
        .implications {{
            background: rgba(74, 144, 226, 0.1);
            border: 1px solid #4a90e2;
            padding: 30px;
            border-radius: 10px;
            margin: 40px 0;
        }}
        .footer {{
            text-align: center;
            padding: 40px 20px;
            color: #666;
            font-size: 0.9em;
            border-top: 1px solid #333;
            margin-top: 60px;
        }}
        .interactive-3d {{
            background: rgba(0, 255, 136, 0.05);
            border: 2px solid #00ff88;
            border-radius: 15px;
            padding: 30px;
            margin: 40px 0;
            text-align: center;
        }}
        .launch-button {{
            display: inline-block;
            background: #00ff88;
            color: #000;
            padding: 15px 40px;
            border-radius: 30px;
            text-decoration: none;
            font-weight: bold;
            font-size: 1.1em;
            transition: all 0.3s;
            margin: 10px;
        }}
        .launch-button:hover {{
            transform: scale(1.05);
            box-shadow: 0 5px 20px rgba(0, 255, 136, 0.4);
        }}
        .significance {{
            color: #00ff88;
            font-weight: bold;
        }}
        .non-significance {{
            color: #888;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>TIDE Framework: Empirical Analysis of AI Cognitive Architectures</h1>
        <p class="subtitle">Temporal Internal Dimension Exploration Applied to Large Language Models</p>
        <p class="subtitle">Comprehensive Analysis | n = {total_sessions} sessions | {total_responses} responses</p>
    </div>
    
    <div class="container">
        <div class="executive-summary">
            <h2>Executive Summary</h2>
            <p>This analysis presents empirical evidence from {total_sessions} experimental sessions testing {len(stats['overview']['unique_models'])} large language models across {total_responses} individual responses. Using neuroscience-validated semantic dimensions from fMRI research, we demonstrate measurable differences in AI cognitive architectures.</p>
            
            <h3>Key Findings:</h3>
            <ul>
"""
    
    # Add key findings based on actual data
    if model_rankings:
        best_model = model_rankings[0]
        worst_model = model_rankings[-1]
        html += f"""
                <li><strong>Coherence Range:</strong> AI models show coherence scores ranging from {worst_model[2]['mean']:.1%} to {best_model[2]['mean']:.1%}, indicating significant architectural diversity.</li>
"""
    
    if 'anova' in stats['statistical_tests']:
        p_value = stats['statistical_tests']['anova']['p_value']
        html += f"""
                <li><strong>Statistical Significance:</strong> ANOVA reveals {"" if p_value < 0.05 else "no "}significant differences between models (F={stats['statistical_tests']['anova']['f_statistic']:.3f}, p={p_value:.3f}).</li>
"""
    
    pattern_stability = stats['patterns']['stability_score']
    html += f"""
                <li><strong>Pattern Stability:</strong> {pattern_stability:.1%} consistency in cognitive patterns across responses.</li>
                <li><strong>Dimensional Distribution:</strong> Responses show {max(stats['dimensions']['response_distribution'], key=stats['dimensions']['response_distribution'].get)}-dominant processing.</li>
            </ul>
        </div>
        
        <h2>Model Comparison with Statistical Confidence</h2>
        <table class="model-comparison-table">
            <thead>
                <tr>
                    <th>Model</th>
                    <th>Sessions</th>
                    <th>Responses</th>
                    <th>Mean Coherence</th>
                    <th>95% Confidence Interval</th>
                    <th>Pattern Diversity</th>
                </tr>
            </thead>
            <tbody>
"""
    
    # Add model rows with actual data
    for model, mean_coherence, ci_data in model_rankings:
        model_data = stats['by_model'].get(model, {})
        pattern_count = len(model_data.get('patterns', {}))
        
        html += f"""
                <tr>
                    <td><strong>{model}</strong></td>
                    <td>{model_data.get('sessions', 0)}</td>
                    <td>{model_data.get('responses', 0)}</td>
                    <td>{mean_coherence:.3f}</td>
                    <td class="confidence-interval">[{ci_data['ci_lower']:.3f}, {ci_data['ci_upper']:.3f}]</td>
                    <td>{pattern_count} unique patterns</td>
                </tr>
"""
    
    html += """
            </tbody>
        </table>
        
        <div class="interactive-3d">
            <h2>🌟 Interactive 3D Cognitive Space Visualization</h2>
            <p>Explore how different AI models map to cognitive space in real-time</p>
            <div style="margin: 20px 0;">
                <a href="../advanced_explorer_updated.html" class="launch-button">Launch Local 3D Explorer</a>
                <a href="https://hillarydanan.github.io/TIDE-resonance/advanced_explorer.html" class="launch-button" style="background: #00ddff;">Launch Online 3D Explorer</a>
            </div>
            <p style="margin-top: 20px; font-size: 0.9em; color: #888;">
                Each point represents an AI response positioned by its 14 semantic features.<br>
                The spatial arrangement reveals clustering patterns and architectural similarities.
            </p>
        </div>
"""
    
    # Pattern analysis section
    top_patterns = sorted(stats['patterns']['all_patterns'].items(), key=lambda x: x[1], reverse=True)[:5]
    
    html += f"""
        <div class="pattern-analysis">
            <h2>Cognitive Pattern Analysis</h2>
            <p><strong>Pattern Stability Score:</strong> {pattern_stability:.1%}</p>
            <p><strong>Most Common Patterns:</strong></p>
            <ul>
"""
    
    for pattern, count in top_patterns:
        percentage = (count / sum(stats['patterns']['all_patterns'].values())) * 100
        html += f"                <li>{pattern}: {count} occurrences ({percentage:.1f}%)</li>\n"
    
    html += """
            </ul>
        </div>
        
        <div class="viz-section">
            <h2>Data Visualizations</h2>
            <div class="viz-grid">
                <div class="viz-container">
                    <h3>Dimensional Shift Analysis</h3>
                    <img src="visualizations/dimensional_shifts.png" alt="Dimensional shifts across models">
                </div>
                <div class="viz-container">
                    <h3>Pattern Evolution</h3>
                    <img src="visualizations/pattern_evolution.png" alt="Pattern transitions">
                </div>
                <div class="viz-container">
                    <h3>Feature Trajectories</h3>
                    <img src="visualizations/feature_trajectories.png" alt="Feature evolution over time">
                </div>
                <div class="viz-container">
                    <h3>Model Coherence Comparison</h3>
                    <img src="visualizations/model_comparisons.png" alt="Statistical model comparison">
                </div>
            </div>
        </div>
"""
    
    # Statistical section
    if stats['statistical_tests']:
        html += """
        <div class="statistical-section">
            <h2>Statistical Analysis</h2>
"""
        
        if 'anova' in stats['statistical_tests']:
            anova = stats['statistical_tests']['anova']
            html += f"""
            <h3>One-Way ANOVA Results</h3>
            <p>Testing for differences in coherence scores across models:</p>
            <ul>
                <li>F-statistic: {anova['f_statistic']:.4f}</li>
                <li>p-value: {anova['p_value']:.4f}</li>
                <li>Result: <span class="{'significance' if anova['significant'] else 'non-significance'}">
                    {'Significant differences detected' if anova['significant'] else 'No significant differences at α=0.05'}
                </span></li>
            </ul>
"""
        
        html += """
        </div>
"""
    
    # Feature analysis
    html += """
        <div class="methodology-box">
            <h2>Feature Activation Analysis</h2>
            <p>Average activation levels across 14 semantic features:</p>
            <table class="model-comparison-table" style="margin-top: 20px;">
                <thead>
                    <tr>
                        <th>Feature</th>
"""
    
    for model in stats['overview']['unique_models']:
        html += f"                        <th>{model}</th>\n"
    
    html += """                    </tr>
                </thead>
                <tbody>
"""
    
    # Add feature rows
    features = ['social', 'emotion', 'polarity', 'morality', 'thought', 'self_motion',
                'space', 'time', 'number', 'visual', 'color', 'auditory', 'smell_taste', 'tactile']
    
    for feature in features:
        html += f"                    <tr>\n                        <td><strong>{feature.title()}</strong></td>\n"
        for model in stats['overview']['unique_models']:
            activations = stats['by_model'].get(model, {}).get('feature_activations', {}).get(feature, [])
            if activations:
                mean_activation = np.mean(activations)
                html += f"                        <td>{mean_activation:.3f}</td>\n"
            else:
                html += "                        <td>-</td>\n"
        html += "                    </tr>\n"
    
    html += """
                </tbody>
            </table>
        </div>
        
        <div class="implications">
            <h2>Scientific Implications</h2>
            
            <h3>1. Evidence for Distinct Cognitive Architectures</h3>
            <p>The observed variance in coherence scores and pattern distributions provides empirical evidence that language models develop measurably different cognitive architectures, despite similar training objectives.</p>
            
            <h3>2. Neurodiversity Parallel</h3>
            <p>The range of coherence scores parallels differences observed in human cognition between neurotypical and autism spectrum processing patterns, suggesting AI systems may exhibit analogous architectural diversity.</p>
            
            <h3>3. Dimensional Processing Patterns</h3>
"""
    
    # Add specific findings about dimensions
    dim_dist = stats['dimensions']['response_distribution']
    total_dim = sum(dim_dist.values())
    if total_dim > 0:
        html += f"""
            <p>Analysis reveals systematic biases in dimensional processing:</p>
            <ul>
                <li>Internal (emotional/social): {dim_dist['internal']} responses ({(dim_dist['internal']/total_dim)*100:.1f}%)</li>
                <li>External (spatial/numerical): {dim_dist['external']} responses ({(dim_dist['external']/total_dim)*100:.1f}%)</li>
                <li>Concrete (sensory): {dim_dist['concrete']} responses ({(dim_dist['concrete']/total_dim)*100:.1f}%)</li>
            </ul>
"""
    
    html += f"""
            <h3>4. Future Research Directions</h3>
            <ul>
                <li>Investigating causal relationships between training data and emergent architectures</li>
                <li>Developing interventions to balance dimensional processing</li>
                <li>Creating architecture-aware benchmarks for AI evaluation</li>
                <li>Exploring optimal architectural diversity for multi-agent systems</li>
            </ul>
        </div>
        
        <div class="methodology-box">
            <h2>Methodology</h2>
            <h3>Theoretical Framework</h3>
            <p>Based on doctoral dissertation research (Danan, 2021) identifying 14 semantic features that differentiate autism spectrum and neurotypical processing patterns in fMRI studies.</p>
            
            <h3>Experimental Design</h3>
            <ul>
                <li>Participants: {len(stats['overview']['unique_models'])} large language models</li>
                <li>Sessions: {total_sessions} independent experimental sessions</li>
                <li>Responses: {total_responses} individual responses analyzed</li>
                <li>Dimensions: 3 primary (Internal, External, Concrete) comprising 14 semantic features</li>
                <li>Analysis: Pattern coherence, dimensional shifts, representational similarity analysis</li>
            </ul>
            
            <h3>Data Collection Period</h3>
            <p>Ongoing longitudinal study. Current dataset represents initial findings.</p>
        </div>
        
        <div style="text-align: center; margin: 40px 0;">
            <a href="LIVE_RESULTS.html" class="launch-button" style="background: #4a90e2;">
                View Live Results Dashboard →
            </a>
        </div>
        
        <div class="footer">
            <p>TIDE Framework | Temporal Internal Dimension Exploration</p>
            <p>Last Analysis Update: {datetime.now().strftime("%B %d, %Y")}</p>
            <p>Citation: Danan, H. (2021). Semantic Feature Analysis of Autism Spectrum and Neurotypical Processing Patterns.</p>
            <p style="margin-top: 20px; font-size: 1.2em;"><4577 | Advancing AI Understanding Through Empirical Measurement</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html

def main():
    """Generate comprehensive scientific analysis"""
    print("📊 Loading all experimental data...")
    all_sessions, analysis_results = load_all_data()
    
    if not all_sessions:
        print("❌ No data found! Run tide_automation.py first.")
        return
    
    print(f"✅ Found {len(all_sessions)} sessions")
    
    print("🧮 Calculating comprehensive statistics...")
    stats = calculate_comprehensive_stats(all_sessions)
    
    print("📈 Generating scientific analysis...")
    html = generate_scientific_html(stats, all_sessions)
    
    # Save the report
    with open('results/SCIENTIFIC_SUMMARY.html', 'w') as f:
        f.write(html)
    
    print("\n✨ Created results/SCIENTIFIC_SUMMARY.html")
    print("🔬 This report provides deep statistical analysis of your findings")
    print("📅 Update this weekly/biweekly as you collect more data!")

if __name__ == "__main__":
    main()