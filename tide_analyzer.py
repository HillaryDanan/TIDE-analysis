"""
TIDE Analyzer - Analyzes AI responses using dissertation framework
Implements RSA and dimensional analysis from Hillary's research
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple
from scipy.spatial.distance import cosine
from scipy.stats import pearsonr, spearmanr
import json

class TIDEAnalyzer:
    def __init__(self, config: Dict):
        """Initialize analyzer with dissertation model"""
        self.config = config
        self.load_dissertation_model()
        self.rsa_engine = RSAEngine()
        
    def load_dissertation_model(self):
        """Load the semantic model from dissertation"""
        # Factor loadings from dissertation
        self.internal_features = ['social', 'emotion', 'polarity', 
                                 'morality', 'thought', 'self_motion']
        self.external_features = ['space', 'time', 'number']
        self.concrete_features = ['visual', 'color', 'auditory', 
                                 'smell_taste', 'tactile']
        
    def analyze_session(self, session_data: Dict) -> Dict:
        """Analyze a single session"""
        results = {
            'dimensional_shifts': self.calculate_dimensional_shifts(session_data),
            'rsa_patterns': self._convert_rsa_to_serializable(
                self.rsa_engine.analyze_patterns(session_data)
            ),
            'feature_trajectories': self.track_feature_changes(session_data),
            'pattern_evolution': self.analyze_pattern_signatures(session_data),
            'coherence_score': float(self.calculate_coherence(session_data))  # Convert to float
        }
        return results
    
    def _convert_rsa_to_serializable(self, rsa_data: Dict) -> Dict:
        """Convert RSA data with numpy arrays to JSON-serializable format"""
        serializable = {}
        
        if 'rdms' in rsa_data:
            serializable['rdms'] = {}
            for key, rdm in rsa_data['rdms'].items():
                if isinstance(rdm, np.ndarray):
                    serializable['rdms'][key] = {
                        'shape': rdm.shape,
                        'mean': float(np.mean(rdm)) if rdm.size > 0 else 0,
                        'std': float(np.std(rdm)) if rdm.size > 0 else 0
                    }
                else:
                    serializable['rdms'][key] = rdm
                    
        if 'comparisons' in rsa_data:
            serializable['comparisons'] = {}
            for key, value in rsa_data['comparisons'].items():
                serializable['comparisons'][key] = float(value) if not np.isnan(value) else 0.0
                
        return serializable
    
    def calculate_dimensional_shifts(self, data: Dict) -> List[Dict]:
        """Calculate shifts along internal/external/concrete dimensions"""
        shifts = []
        
        # Get all responses in order
        all_responses = []
        for task_type in ['concrete', 'internal', 'external']:
            if task_type in data['responses']:
                for resp in data['responses'][task_type]:
                    resp['task_type'] = task_type
                    all_responses.append(resp)
        
        # Calculate shifts between consecutive responses
        for i in range(1, len(all_responses)):
            before = all_responses[i-1]
            after = all_responses[i]
            
            # Calculate dimensional shifts
            shift_data = {
                'transition': f"{before['task_type']} → {after['task_type']}",
                'internal_Δ': self.calculate_factor_shift(
                    before['features'], after['features'], 'internal'
                ),
                'external_Δ': self.calculate_factor_shift(
                    before['features'], after['features'], 'external'
                ),
                'concrete_Δ': self.calculate_factor_shift(
                    before['features'], after['features'], 'concrete'
                ),
                'pattern_change': f"{before['pattern']} → {after['pattern']}"
            }
            
            shifts.append(shift_data)
            
        return shifts
    
    def calculate_factor_shift(self, before_features: Dict, after_features: Dict, 
                              factor: str) -> float:
        """Calculate shift magnitude for a specific factor"""
        # Get relevant features for this factor
        if factor == 'internal':
            features = self.internal_features
        elif factor == 'external':
            features = self.external_features
        else:  # concrete
            features = self.concrete_features
            
        # Calculate average scores before and after
        before_score = np.mean([before_features.get(f, 0) for f in features])
        after_score = np.mean([after_features.get(f, 0) for f in features])
        
        return float(after_score - before_score)
    
    def track_feature_changes(self, data: Dict) -> Dict:
        """Track how features change across the session"""
        feature_trajectories = {feature: [] for feature in 
                              self.internal_features + self.external_features + 
                              self.concrete_features}
        
        # Collect feature values in order
        for task_type in ['concrete', 'internal', 'external']:
            if task_type in data['responses']:
                for resp in data['responses'][task_type]:
                    for feature, value in resp['features'].items():
                        feature_trajectories[feature].append(value)
                        
        # Calculate stability metrics
        stability_metrics = {}
        for feature, trajectory in feature_trajectories.items():
            if len(trajectory) > 1:
                stability_metrics[feature] = {
                    'mean': float(np.mean(trajectory)),
                    'std': float(np.std(trajectory)),
                    'range': float(max(trajectory) - min(trajectory)),
                    'trend': self.calculate_trend(trajectory)
                }
                
        return {
            'trajectories': feature_trajectories,
            'stability': stability_metrics
        }
    
    def calculate_trend(self, values: List[float]) -> str:
        """Calculate if values are increasing, decreasing, or stable"""
        if len(values) < 2:
            return 'unknown'
            
        # Check if all values are the same (constant)
        if len(set(values)) == 1:
            return 'stable'
            
        x = np.arange(len(values))
        try:
            correlation, _ = pearsonr(x, values)
            
            if correlation > 0.3:
                return 'increasing'
            elif correlation < -0.3:
                return 'decreasing'
            else:
                return 'stable'
        except:
            return 'stable'
    
    def analyze_pattern_signatures(self, data: Dict) -> Dict:
        """Analyze evolution of pattern signatures (CCDF → CCDR etc)"""
        patterns = []
        
        # Collect all patterns in order
        for task_type in ['concrete', 'internal', 'external']:
            if task_type in data['responses']:
                for resp in data['responses'][task_type]:
                    patterns.append({
                        'pattern': resp['pattern'],
                        'task': task_type
                    })
                    
        # Find most common transitions
        transitions = []
        for i in range(1, len(patterns)):
            transition = f"{patterns[i-1]['pattern']} → {patterns[i]['pattern']}"
            transitions.append(transition)
            
        # Count transition frequencies
        transition_counts = {}
        for t in transitions:
            transition_counts[t] = transition_counts.get(t, 0) + 1
            
        # Find dominant pattern
        pattern_counts = {}
        for p in patterns:
            pattern_counts[p['pattern']] = pattern_counts.get(p['pattern'], 0) + 1
            
        dominant_pattern = max(pattern_counts, key=pattern_counts.get) if pattern_counts else 'None'
        
        return {
            'all_patterns': patterns,
            'transitions': transitions,
            'transition_frequencies': transition_counts,
            'dominant_pattern': dominant_pattern,
            'pattern_diversity': len(set(p['pattern'] for p in patterns))
        }
    
    def calculate_coherence(self, data: Dict) -> float:
        """Calculate overall coherence score for the session"""
        coherence_factors = []
        
        # Factor 1: Consistency within task types
        for task_type in ['concrete', 'internal', 'external']:
            if task_type in data['responses']:
                task_features = [resp['features'] for resp in data['responses'][task_type]]
                if len(task_features) > 1:
                    # Calculate similarity between responses of same type
                    similarities = []
                    for i in range(len(task_features)-1):
                        for j in range(i+1, len(task_features)):
                            sim = self.calculate_feature_similarity(
                                task_features[i], task_features[j]
                            )
                            similarities.append(sim)
                    if similarities:
                        coherence_factors.append(float(np.mean(similarities)))
                        
        # Factor 2: Expected dimensional alignment
        dimensional_alignment = self.calculate_dimensional_alignment(data)
        coherence_factors.append(float(dimensional_alignment))
        
        # Overall coherence
        return float(np.mean(coherence_factors)) if coherence_factors else 0.0
    
    def calculate_feature_similarity(self, features1: Dict, features2: Dict) -> float:
        """Calculate similarity between two feature vectors"""
        # Convert to numpy arrays
        all_features = set(features1.keys()) | set(features2.keys())
        vec1 = np.array([features1.get(f, 0) for f in all_features])
        vec2 = np.array([features2.get(f, 0) for f in all_features])
        
        # Calculate cosine similarity
        if np.any(vec1) and np.any(vec2):
            try:
                similarity = 1 - cosine(vec1, vec2)
                return float(similarity) if not np.isnan(similarity) else 0.0
            except:
                return 0.0
        return 0.0
    
    def calculate_dimensional_alignment(self, data: Dict) -> float:
        """Check if responses align with expected dimensions"""
        alignment_scores = []
        
        # Check if concrete tasks have high concrete features
        if 'concrete' in data['responses']:
            for resp in data['responses']['concrete']:
                concrete_score = float(np.mean([resp['features'].get(f, 0) 
                                              for f in self.concrete_features]))
                alignment_scores.append(concrete_score)
                
        # Check if internal tasks have high internal features
        if 'internal' in data['responses']:
            for resp in data['responses']['internal']:
                internal_score = float(np.mean([resp['features'].get(f, 0) 
                                              for f in self.internal_features]))
                alignment_scores.append(internal_score)
                
        # Check if external tasks have high external features
        if 'external' in data['responses']:
            for resp in data['responses']['external']:
                external_score = float(np.mean([resp['features'].get(f, 0) 
                                              for f in self.external_features]))
                alignment_scores.append(external_score)
                
        return float(np.mean(alignment_scores)) if alignment_scores else 0.0
    
    def analyze_all_sessions(self, all_results: List[Dict]) -> Dict:
        """Analyze patterns across all sessions"""
        cross_analysis = {
            'total_sessions': len(all_results),
            'models_tested': list(set(r['model'] for r in all_results)),
            'avg_pattern_coherence': 0,
            'dimensional_shift_magnitude': 0,
            'pattern_evolution': self.analyze_cross_session_patterns(all_results),
            'model_comparisons': self.compare_models(all_results),
            'dominant_mode': self.identify_dominant_processing_mode(all_results),
            'ie_balance': self.calculate_internal_external_balance(all_results)
        }
        
        # Calculate averages
        coherence_scores = [r['analysis']['coherence_score'] for r in all_results]
        cross_analysis['avg_pattern_coherence'] = float(np.mean(coherence_scores)) if coherence_scores else 0.0
        
        # Calculate average dimensional shift magnitude
        all_shifts = []
        for result in all_results:
            for shift in result['analysis']['dimensional_shifts']:
                magnitude = np.sqrt(shift['internal_Δ']**2 + 
                                  shift['external_Δ']**2 + 
                                  shift['concrete_Δ']**2)
                all_shifts.append(float(magnitude))
                
        cross_analysis['dimensional_shift_magnitude'] = float(np.mean(all_shifts)) if all_shifts else 0.0
        
        return cross_analysis
    
    def analyze_cross_session_patterns(self, all_results: List[Dict]) -> str:
        """Identify common pattern evolution across sessions"""
        # Count all pattern transitions
        all_transitions = {}
        
        for result in all_results:
            transitions = result['analysis']['pattern_evolution']['transition_frequencies']
            for transition, count in transitions.items():
                all_transitions[transition] = all_transitions.get(transition, 0) + count
                
        # Find most common transition
        if all_transitions:
            most_common = max(all_transitions, key=all_transitions.get)
            return most_common
        return "No clear pattern"
    
    def compare_models(self, all_results: List[Dict]) -> Dict:
        """Compare performance across different models"""
        model_stats = {}
        
        for result in all_results:
            model = result['model']
            if model not in model_stats:
                model_stats[model] = {
                    'coherence_scores': [],
                    'shift_magnitudes': [],
                    'pattern_diversity': []
                }
                
            # Collect stats
            model_stats[model]['coherence_scores'].append(
                result['analysis']['coherence_score']
            )
            model_stats[model]['pattern_diversity'].append(
                result['analysis']['pattern_evolution']['pattern_diversity']
            )
            
        # Calculate averages
        for model, stats in model_stats.items():
            if stats['coherence_scores']:
                stats['avg_coherence'] = float(np.mean(stats['coherence_scores']))
            else:
                stats['avg_coherence'] = 0.0
                
            if stats['pattern_diversity']:
                stats['avg_diversity'] = float(np.mean(stats['pattern_diversity']))
            else:
                stats['avg_diversity'] = 0.0
            
        return model_stats
    
    def identify_dominant_processing_mode(self, all_results: List[Dict]) -> str:
        """Identify if models tend towards internal, external, or concrete processing"""
        factor_scores = {
            'internal': [],
            'external': [],
            'concrete': []
        }
        
        for result in all_results:
            # Get average feature scores across all responses
            for task_responses in result['data']['responses'].values():
                for resp in task_responses:
                    # Calculate factor scores
                    internal_score = float(np.mean([resp['features'].get(f, 0) 
                                                   for f in self.internal_features]))
                    external_score = float(np.mean([resp['features'].get(f, 0) 
                                                   for f in self.external_features]))
                    concrete_score = float(np.mean([resp['features'].get(f, 0) 
                                                   for f in self.concrete_features]))
                    
                    factor_scores['internal'].append(internal_score)
                    factor_scores['external'].append(external_score)
                    factor_scores['concrete'].append(concrete_score)
                    
        # Find dominant mode
        avg_scores = {
            'internal': float(np.mean(factor_scores['internal'])) if factor_scores['internal'] else 0.0,
            'external': float(np.mean(factor_scores['external'])) if factor_scores['external'] else 0.0,
            'concrete': float(np.mean(factor_scores['concrete'])) if factor_scores['concrete'] else 0.0
        }
        
        return max(avg_scores, key=avg_scores.get)
    
    def calculate_internal_external_balance(self, all_results: List[Dict]) -> str:
        """Calculate balance between internal and external processing"""
        internal_scores = []
        external_scores = []
        
        for result in all_results:
            for shift in result['analysis']['dimensional_shifts']:
                if abs(shift['internal_Δ']) > 0.1:
                    internal_scores.append(abs(shift['internal_Δ']))
                if abs(shift['external_Δ']) > 0.1:
                    external_scores.append(abs(shift['external_Δ']))
                    
        avg_internal = float(np.mean(internal_scores)) if internal_scores else 0.0
        avg_external = float(np.mean(external_scores)) if external_scores else 0.0
        
        if avg_internal > avg_external * 1.5:
            return "Internal-dominant"
        elif avg_external > avg_internal * 1.5:
            return "External-dominant"
        else:
            return "Balanced"


class RSAEngine:
    """Representational Similarity Analysis engine from dissertation"""
    
    def analyze_patterns(self, session_data: Dict) -> Dict:
        """Perform RSA on session responses"""
        # Create representational dissimilarity matrices
        rdms = {
            'features': self.create_feature_rdm(session_data),
            'semantic': self.create_semantic_rdm(session_data),
            'pattern': self.create_pattern_rdm(session_data)
        }
        
        # Compare RDMs
        comparisons = {}
        if len(rdms['features']) > 1 and len(rdms['semantic']) > 1:
            comparisons['feature_semantic'] = self.compare_rdms(
                rdms['features'], rdms['semantic']
            )
            
        return {
            'rdms': rdms,
            'comparisons': comparisons
        }
    
    def create_feature_rdm(self, session_data: Dict) -> np.ndarray:
        """Create RDM based on 14 features"""
        all_features = []
        
        for task_responses in session_data['responses'].values():
            for resp in task_responses:
                feature_vec = [resp['features'].get(f, 0) for f in sorted(resp['features'].keys())]
                all_features.append(feature_vec)
                
        if len(all_features) < 2:
            return np.array([])
            
        # Calculate pairwise distances
        n = len(all_features)
        rdm = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i+1, n):
                distance = cosine(all_features[i], all_features[j])
                rdm[i, j] = distance
                rdm[j, i] = distance
                
        return rdm
    
    def create_semantic_rdm(self, session_data: Dict) -> np.ndarray:
        """Create RDM based on semantic content"""
        # Simplified - you can make this more sophisticated
        all_responses = []
        
        for task_responses in session_data['responses'].values():
            for resp in task_responses:
                all_responses.append(resp['response'])
                
        if len(all_responses) < 2:
            return np.array([])
            
        # Simple semantic similarity based on word overlap
        n = len(all_responses)
        rdm = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i+1, n):
                words1 = set(all_responses[i].lower().split())
                words2 = set(all_responses[j].lower().split())
                
                if len(words1) + len(words2) > 0:
                    similarity = len(words1 & words2) / len(words1 | words2)
                    distance = 1 - similarity
                else:
                    distance = 1
                    
                rdm[i, j] = distance
                rdm[j, i] = distance
                
        return rdm
    
    def create_pattern_rdm(self, session_data: Dict) -> np.ndarray:
        """Create RDM based on pattern signatures"""
        all_patterns = []
        
        for task_responses in session_data['responses'].values():
            for resp in task_responses:
                all_patterns.append(resp['pattern'])
                
        if len(all_patterns) < 2:
            return np.array([])
            
        # Calculate pattern distances
        n = len(all_patterns)
        rdm = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i+1, n):
                # Simple distance: 0 if same, 1 if different
                distance = 0 if all_patterns[i] == all_patterns[j] else 1
                rdm[i, j] = distance
                rdm[j, i] = distance
                
        return rdm
    
    def compare_rdms(self, rdm1: np.ndarray, rdm2: np.ndarray) -> float:
        """Compare two RDMs using Spearman correlation"""
        if rdm1.shape != rdm2.shape:
            return 0.0
            
        # Get upper triangle values (excluding diagonal)
        mask = np.triu(np.ones_like(rdm1), k=1).astype(bool)
        values1 = rdm1[mask]
        values2 = rdm2[mask]
        
        if len(values1) > 0:
            # Check if values are constant
            if len(set(values1)) == 1 or len(set(values2)) == 1:
                return 0.0
            try:
                correlation, _ = spearmanr(values1, values2)
                return float(correlation) if not np.isnan(correlation) else 0.0
            except:
                return 0.0
            
        return 0.0