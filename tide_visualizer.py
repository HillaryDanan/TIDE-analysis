"""
TIDE Visualizer - Creates beautiful visualizations of analysis results
Integrates with advanced_explorer.html for 3D visualization
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
from typing import Dict, List, Any
import seaborn as sns
import json
from datetime import datetime

class TIDEVisualizer:
    def __init__(self, config: Dict):
        """Initialize visualizer with configuration"""
        self.config = config
        self.setup_style()
        
    def setup_style(self):
        """Setup matplotlib style for beautiful visualizations"""
        plt.style.use('dark_background')
        self.colors = {
            'internal': '#00ff88',  # Bright green
            'external': '#00ddff',  # Bright cyan
            'concrete': '#ff00dd',  # Bright magenta
            'background': '#1e3c72',
            'accent': '#ffd700'
        }
        
    def create_all_visualizations(self, all_results: List[Dict], 
                                 cross_analysis: Dict):
        """Create all visualization outputs"""
        print("    📊 Creating dimensional shift visualization...")
        self.plot_dimensional_shifts(all_results)
        
        print("    📊 Creating pattern evolution visualization...")
        self.plot_pattern_evolution(all_results)
        
        print("    📊 Creating feature trajectory visualization...")
        self.plot_feature_trajectories(all_results)
        
        print("    📊 Creating model comparison visualization...")
        self.plot_model_comparisons(cross_analysis)
        
        print("    📊 Creating 3D visualization data...")
        self.create_3d_visualization_data(all_results)
        
    def plot_dimensional_shifts(self, all_results: List[Dict]):
        """Plot dimensional shifts across all sessions"""
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
        fig.patch.set_facecolor('#0a0a0a')
        
        # Collect shift data
        internal_shifts = []
        external_shifts = []
        concrete_shifts = []
        
        for result in all_results:
            for shift in result['analysis']['dimensional_shifts']:
                internal_shifts.append(shift['internal_Δ'])
                external_shifts.append(shift['external_Δ'])
                concrete_shifts.append(shift['concrete_Δ'])
                
        # Plot distributions
        ax1.hist(internal_shifts, bins=30, color=self.colors['internal'], 
                alpha=0.7, edgecolor='white')
        ax1.set_title('Internal Dimension Shifts', fontsize=16, color='white')
        ax1.set_xlabel('Shift Magnitude', color='white')
        ax1.set_ylabel('Frequency', color='white')
        
        ax2.hist(external_shifts, bins=30, color=self.colors['external'],
                alpha=0.7, edgecolor='white')
        ax2.set_title('External Dimension Shifts', fontsize=16, color='white')
        ax2.set_xlabel('Shift Magnitude', color='white')
        ax2.set_ylabel('Frequency', color='white')
        
        ax3.hist(concrete_shifts, bins=30, color=self.colors['concrete'],
                alpha=0.7, edgecolor='white')
        ax3.set_title('Concrete Dimension Shifts', fontsize=16, color='white')
        ax3.set_xlabel('Shift Magnitude', color='white')
        ax3.set_ylabel('Frequency', color='white')
        
        plt.tight_layout()
        plt.savefig('results/visualizations/dimensional_shifts.png', 
                   facecolor='#0a0a0a', dpi=150)
        plt.close()
        
    def plot_pattern_evolution(self, all_results: List[Dict]):
        """Plot pattern signature evolution"""
        fig, ax = plt.subplots(figsize=(14, 8))
        fig.patch.set_facecolor('#0a0a0a')
        
        # Collect pattern transitions
        transition_counts = {}
        
        for result in all_results:
            transitions = result['analysis']['pattern_evolution']['transition_frequencies']
            for transition, count in transitions.items():
                transition_counts[transition] = transition_counts.get(transition, 0) + count
                
        # Sort by frequency
        sorted_transitions = sorted(transition_counts.items(), 
                                  key=lambda x: x[1], reverse=True)[:15]
        
        # Plot
        transitions = [t[0] for t in sorted_transitions]
        counts = [t[1] for t in sorted_transitions]
        
        bars = ax.barh(transitions, counts, color=self.colors['accent'])
        
        # Add value labels
        for i, (bar, count) in enumerate(zip(bars, counts)):
            ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                   str(count), va='center', color='white')
                   
        ax.set_xlabel('Frequency', fontsize=14, color='white')
        ax.set_title('Pattern Signature Transitions', fontsize=18, color='white')
        ax.tick_params(colors='white')
        
        plt.tight_layout()
        plt.savefig('results/visualizations/pattern_evolution.png',
                   facecolor='#0a0a0a', dpi=150)
        plt.close()
        
    def plot_feature_trajectories(self, all_results: List[Dict]):
        """Plot how features change over time"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.patch.set_facecolor('#0a0a0a')
        axes = axes.flatten()
        
        # Select representative features
        features_to_plot = [
            ('emotion', 'Internal Feature: Emotion', self.colors['internal']),
            ('space', 'External Feature: Space', self.colors['external']),
            ('visual', 'Concrete Feature: Visual', self.colors['concrete']),
            ('thought', 'Internal Feature: Thought', self.colors['internal'])
        ]
        
        for idx, (feature, title, color) in enumerate(features_to_plot):
            ax = axes[idx]
            
            # Collect feature values across all sessions
            for result_idx, result in enumerate(all_results[:4]):  # First 4 sessions
                trajectory = result['analysis']['feature_trajectories']['trajectories'].get(feature, [])
                
                if trajectory:
                    x = range(len(trajectory))
                    ax.plot(x, trajectory, marker='o', label=f"Session {result_idx+1}",
                           alpha=0.7, linewidth=2)
                    
            ax.set_title(title, fontsize=14, color='white')
            ax.set_xlabel('Response Number', color='white')
            ax.set_ylabel('Feature Score', color='white')
            ax.tick_params(colors='white')
            ax.legend(loc='best')
            ax.grid(True, alpha=0.3)
            
        plt.tight_layout()
        plt.savefig('results/visualizations/feature_trajectories.png',
                   facecolor='#0a0a0a', dpi=150)
        plt.close()
        
    def plot_model_comparisons(self, cross_analysis: Dict):
        """Plot comparison between different models"""
        model_stats = cross_analysis['model_comparisons']
        
        if not model_stats:
            return
            
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.patch.set_facecolor('#0a0a0a')
        
        # Get model names and stats
        models = list(model_stats.keys())
        coherence_scores = [stats['avg_coherence'] for stats in model_stats.values()]
        diversity_scores = [stats['avg_diversity'] for stats in model_stats.values()]
        
        # Plot coherence
        bars1 = ax1.bar(models, coherence_scores, color=self.colors['accent'])
        ax1.set_title('Average Coherence by Model', fontsize=16, color='white')
        ax1.set_ylabel('Coherence Score', color='white')
        ax1.tick_params(colors='white')
        
        # Add value labels
        for bar, score in zip(bars1, coherence_scores):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{score:.2f}', ha='center', va='bottom', color='white')
                    
        # Plot diversity
        bars2 = ax2.bar(models, diversity_scores, color=self.colors['external'])
        ax2.set_title('Pattern Diversity by Model', fontsize=16, color='white')
        ax2.set_ylabel('Diversity Score', color='white')
        ax2.tick_params(colors='white')
        
        # Add value labels
        for bar, score in zip(bars2, diversity_scores):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{score:.1f}', ha='center', va='bottom', color='white')
                    
        plt.tight_layout()
        plt.savefig('results/visualizations/model_comparisons.png',
                   facecolor='#0a0a0a', dpi=150)
        plt.close()
        
    def create_3d_visualization_data(self, all_results: List[Dict]):
        """Create data for 3D visualization in advanced_explorer.html"""
        visualization_data = {
            'sessions': [],
            'metadata': {
                'total_sessions': len(all_results),
                'models': list(set(r['model'] for r in all_results)),
                'timestamp': datetime.now().isoformat()
            }
        }
        
        for result in all_results:
            session_3d = {
                'model': result['model'],
                'session_id': result['session'],
                'points': []
            }
            
            # Convert each response to a 3D point
            point_id = 0
            for task_type, responses in result['data']['responses'].items():
                for resp in responses:
                    # Calculate 3D coordinates based on factor scores
                    internal_score = np.mean([resp['features'].get(f, 0) 
                                            for f in ['social', 'emotion', 'polarity', 
                                                     'morality', 'thought', 'self_motion']])
                    external_score = np.mean([resp['features'].get(f, 0)
                                            for f in ['space', 'time', 'number']])
                    concrete_score = np.mean([resp['features'].get(f, 0)
                                            for f in ['visual', 'color', 'auditory',
                                                     'smell_taste', 'tactile']])
                    
                    point = {
                        'id': point_id,
                        'x': internal_score,
                        'y': external_score,
                        'z': concrete_score,
                        'task_type': task_type,
                        'pattern': resp['pattern'],
                        'color': self.colors[task_type],
                        'prompt': resp['prompt']# Show full prompt
                    }
                    
                    session_3d['points'].append(point)
                    point_id += 1
                    
            visualization_data['sessions'].append(session_3d)
            
        # Save for use in advanced_explorer.html
        with open('results/visualizations/3d_data.json', 'w') as f:
            json.dump(visualization_data, f, indent=2)
            
        print("      ✅ 3D visualization data saved to: results/visualizations/3d_data.json")
