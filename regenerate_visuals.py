#!/usr/bin/env python3
"""Regenerate visualizations and report from existing data"""
import json
from tide_analyzer import TIDEAnalyzer
from tide_visualizer import TIDEVisualizer
from tide_automation import generate_html_report

# Load the existing results
with open('results/data/all_sessions_20250722_151307.json', 'r') as f:
    all_results = json.load(f)

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

# Recreate analysis
analyzer = TIDEAnalyzer(config)
cross_analysis = analyzer.analyze_all_sessions(all_results)

# Regenerate visualizations with full prompts
print("Regenerating visualizations...")
visualizer = TIDEVisualizer(config)
visualizer.create_all_visualizations(all_results, cross_analysis)

# Generate updated report
print("Regenerating report...")
generate_html_report(all_results, cross_analysis, "20250722_151307_updated")

print("Done! Check results/report_20250722_151307_updated.html")
