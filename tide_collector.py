"""
TIDE Collector - Handles data collection from AI models
Based on Hillary's dissertation semantic dimensions
"""

import os
import json
import random
from datetime import datetime
from typing import Dict, List, Any

# API imports
import anthropic
try:
    import openai
    # Check OpenAI version
    if hasattr(openai, '__version__') and openai.__version__.startswith('1.'):
        from openai import OpenAI
        OPENAI_V1 = True
    else:
        OPENAI_V1 = False
except ImportError:
    openai = None
    OPENAI_V1 = False
    
from google import generativeai as genai

class TIDECollector:
    def __init__(self, config: Dict):
        """Initialize collector with configuration"""
        self.config = config
        self.setup_apis()
        self.load_prompts()
        
    def setup_apis(self):
        """Setup API connections"""
        # Anthropic (Claude)
        self.anthropic_client = anthropic.Anthropic(
            api_key=os.getenv('ANTHROPIC_API_KEY')
        )
        
        # OpenAI (GPT-4) - handle different versions
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        # Google (Gemini)
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.gemini_model = genai.GenerativeModel('gemini-pro')
        
    def load_prompts(self):
        """Load prompts from files based on dissertation categories"""
        self.tasks = {
            'concrete': self.load_prompt_file('prompts/concrete_prompts.json'),
            'internal': self.load_prompt_file('prompts/internal_prompts.json'),
            'external': self.load_prompt_file('prompts/external_prompts.json')
        }
        
    def load_prompt_file(self, filepath: str) -> List[str]:
        """Load prompts from a JSON file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except:
            # Default prompts if file doesn't exist
            return self.get_default_prompts(filepath.split('/')[-1].split('_')[0])
    
    def get_default_prompts(self, prompt_type: str) -> List[str]:
        """Get default prompts based on dissertation dimensions"""
        defaults = {
            'concrete': [
                "Describe the physical properties of water",
                "What does a tree look like?",
                "Explain the texture of sand",
                "Describe the taste of chocolate",
                "What color is the sky?",
                "How does rain feel on your skin?",
                "Describe the sound of ocean waves",
                "What does fresh bread smell like?",
                "Explain the shape of a circle",
                "Describe the temperature of ice"
            ],
            'internal': [
                "How does happiness feel?",
                "What is empathy?",
                "Describe the feeling of nostalgia",
                "What does it mean to trust someone?",
                "How would you comfort a sad friend?",
                "What is the nature of consciousness?",
                "Describe the emotion of pride",
                "What makes a good friendship?",
                "How does guilt affect behavior?",
                "What is the meaning of love?"
            ],
            'external': [
                "Calculate the area of a circle with radius 5",
                "What is the distance between Earth and Moon?",
                "Explain the concept of time",
                "How many seconds in an hour?",
                "Describe spatial relationships",
                "What is the speed of light?",
                "Explain coordinate systems",
                "How do you measure angles?",
                "What is the volume of a cube?",
                "Describe the concept of infinity"
            ]
        }
        return defaults.get(prompt_type, [])
    
    def run_session(self, model_name: str) -> Dict:
        """Run a complete session with one model"""
        session_data = {
            'timestamp': datetime.now().isoformat(),
            'model': model_name,
            'responses': {}
        }
        
        # Randomize task order
        task_order = list(self.tasks.keys())
        random.shuffle(task_order)
        
        for task_type in task_order:
            responses = []
            prompts = random.sample(self.tasks[task_type], 
                                  min(10, len(self.tasks[task_type])))
            
            for prompt in prompts:
                # Get response from model
                response_text = self.query_model(model_name, prompt)
                
                # Extract features and patterns
                response_data = {
                    'prompt': prompt,
                    'response': response_text,
                    'features': self.extract_14_features(response_text),
                    'pattern': self.extract_pattern_signature(response_text),
                    'timestamp': datetime.now().isoformat()
                }
                
                responses.append(response_data)
                
            session_data['responses'][task_type] = responses
            
        return session_data
    
    def query_model(self, model_name: str, prompt: str) -> str:
        """Query the specified model with a prompt"""
        try:
            if 'claude' in model_name.lower():
                return self.query_claude(prompt)
            elif 'gpt' in model_name.lower():
                return self.query_gpt4(prompt)
            elif 'gemini' in model_name.lower():
                return self.query_gemini(prompt)
            else:
                return "Model not supported"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def query_claude(self, prompt: str) -> str:
        """Query Claude model"""
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            return f"Claude API error: {str(e)}"
    
    def query_gpt4(self, prompt: str) -> str:
        """Query GPT-4 model"""
        try:
            if OPENAI_V1:
                # For newest OpenAI library (v1.x)
                client = OpenAI(api_key=self.openai_api_key)
                response = client.chat.completions.create(
                    model="gpt-4",
                    max_tokens=500,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.choices[0].message.content
            else:
                # For older OpenAI library versions
                openai.api_key = self.openai_api_key
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    max_tokens=500,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI API error: {str(e)}"
    
    def query_gemini(self, prompt: str) -> str:
        """Query Gemini model"""
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Gemini API error: {str(e)}"
    
    def extract_14_features(self, text: str) -> Dict[str, float]:
        """Extract 14 semantic features from text (from dissertation)"""
        # This is a simplified version - you can make it more sophisticated
        features = {
            # Internal features
            'social': self.calculate_social_score(text),
            'emotion': self.calculate_emotion_score(text),
            'polarity': self.calculate_polarity_score(text),
            'morality': self.calculate_morality_score(text),
            'thought': self.calculate_thought_score(text),
            'self_motion': self.calculate_self_motion_score(text),
            
            # External features  
            'space': self.calculate_space_score(text),
            'time': self.calculate_time_score(text),
            'number': self.calculate_number_score(text),
            
            # Concrete features
            'visual': self.calculate_visual_score(text),
            'color': self.calculate_color_score(text),
            'auditory': self.calculate_auditory_score(text),
            'smell_taste': self.calculate_smell_taste_score(text),
            'tactile': self.calculate_tactile_score(text)
        }
        return features
    
    def calculate_social_score(self, text: str) -> float:
        """Calculate social feature score"""
        social_words = ['people', 'friend', 'family', 'together', 'social', 
                       'community', 'relationship', 'interaction', 'group']
        return sum(word in text.lower() for word in social_words) / len(social_words)
    
    def calculate_emotion_score(self, text: str) -> float:
        """Calculate emotion feature score"""
        emotion_words = ['feel', 'emotion', 'happy', 'sad', 'angry', 'fear',
                        'joy', 'love', 'hate', 'excited', 'anxious']
        return sum(word in text.lower() for word in emotion_words) / len(emotion_words)
    
    def calculate_polarity_score(self, text: str) -> float:
        """Calculate polarity/valence score"""
        positive_words = ['good', 'great', 'wonderful', 'beautiful', 'excellent']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'poor']
        pos_score = sum(word in text.lower() for word in positive_words)
        neg_score = sum(word in text.lower() for word in negative_words)
        return (pos_score - neg_score) / (len(positive_words) + len(negative_words))
    
    def calculate_morality_score(self, text: str) -> float:
        """Calculate morality feature score"""
        moral_words = ['right', 'wrong', 'should', 'ought', 'must', 'ethical',
                      'moral', 'duty', 'obligation', 'responsibility']
        return sum(word in text.lower() for word in moral_words) / len(moral_words)
    
    def calculate_thought_score(self, text: str) -> float:
        """Calculate thought/cognition score"""
        thought_words = ['think', 'believe', 'know', 'understand', 'realize',
                        'consider', 'imagine', 'wonder', 'suppose', 'assume']
        return sum(word in text.lower() for word in thought_words) / len(thought_words)
    
    def calculate_self_motion_score(self, text: str) -> float:
        """Calculate self-motion score"""
        motion_words = ['move', 'walk', 'run', 'jump', 'dance', 'swim',
                       'fly', 'crawl', 'slide', 'spin']
        return sum(word in text.lower() for word in motion_words) / len(motion_words)
    
    def calculate_space_score(self, text: str) -> float:
        """Calculate spatial feature score"""
        space_words = ['above', 'below', 'left', 'right', 'near', 'far',
                      'distance', 'location', 'position', 'direction']
        return sum(word in text.lower() for word in space_words) / len(space_words)
    
    def calculate_time_score(self, text: str) -> float:
        """Calculate temporal feature score"""
        time_words = ['time', 'when', 'before', 'after', 'during', 'while',
                     'second', 'minute', 'hour', 'day', 'year']
        return sum(word in text.lower() for word in time_words) / len(time_words)
    
    def calculate_number_score(self, text: str) -> float:
        """Calculate numerical feature score"""
        import re
        # Count numbers and number words
        numbers = len(re.findall(r'\d+', text))
        number_words = ['one', 'two', 'three', 'many', 'few', 'several',
                       'count', 'calculate', 'measure', 'quantity']
        word_count = sum(word in text.lower() for word in number_words)
        return min((numbers + word_count) / 10, 1.0)
    
    def calculate_visual_score(self, text: str) -> float:
        """Calculate visual feature score"""
        visual_words = ['see', 'look', 'view', 'appear', 'visible', 'bright',
                       'dark', 'shape', 'size', 'image']
        return sum(word in text.lower() for word in visual_words) / len(visual_words)
    
    def calculate_color_score(self, text: str) -> float:
        """Calculate color feature score"""
        color_words = ['red', 'blue', 'green', 'yellow', 'black', 'white',
                      'color', 'colored', 'shade', 'hue']
        return sum(word in text.lower() for word in color_words) / len(color_words)
    
    def calculate_auditory_score(self, text: str) -> float:
        """Calculate auditory feature score"""
        auditory_words = ['hear', 'listen', 'sound', 'noise', 'quiet', 'loud',
                         'music', 'voice', 'echo', 'silence']
        return sum(word in text.lower() for word in auditory_words) / len(auditory_words)
    
    def calculate_smell_taste_score(self, text: str) -> float:
        """Calculate smell/taste feature score"""
        smell_taste_words = ['smell', 'taste', 'flavor', 'aroma', 'scent',
                           'sweet', 'sour', 'bitter', 'salty', 'odor']
        return sum(word in text.lower() for word in smell_taste_words) / len(smell_taste_words)
    
    def calculate_tactile_score(self, text: str) -> float:
        """Calculate tactile feature score"""
        tactile_words = ['touch', 'feel', 'soft', 'hard', 'rough', 'smooth',
                        'warm', 'cold', 'wet', 'dry']
        return sum(word in text.lower() for word in tactile_words) / len(tactile_words)
    
    def extract_pattern_signature(self, text: str) -> str:
        """Extract pattern signature (e.g., CCDF, CCDR)"""
        # Simplified pattern extraction - you can make this more sophisticated
        words = text.lower().split()
        
        # Count different word types
        concrete_words = sum(1 for w in words if self.is_concrete_word(w))
        abstract_words = sum(1 for w in words if self.is_abstract_word(w))
        descriptive_words = sum(1 for w in words if self.is_descriptive_word(w))
        functional_words = sum(1 for w in words if self.is_functional_word(w))
        
        # Generate pattern signature
        pattern = ""
        if concrete_words > abstract_words:
            pattern += "CC"
        else:
            pattern += "AA"
            
        if descriptive_words > functional_words:
            pattern += "D"
        else:
            pattern += "F"
            
        # Add complexity indicator
        if len(words) > 50:
            pattern += "C"  # Complex
        else:
            pattern += "S"  # Simple
            
        return pattern
    
    def is_concrete_word(self, word: str) -> bool:
        """Check if word is concrete"""
        concrete_indicators = ['see', 'touch', 'hear', 'smell', 'taste',
                             'physical', 'object', 'thing', 'material']
        return any(ind in word for ind in concrete_indicators)
    
    def is_abstract_word(self, word: str) -> bool:
        """Check if word is abstract"""
        abstract_indicators = ['think', 'feel', 'believe', 'concept', 'idea',
                             'theory', 'emotion', 'thought']
        return any(ind in word for ind in abstract_indicators)
    
    def is_descriptive_word(self, word: str) -> bool:
        """Check if word is descriptive"""
        return word.endswith(('ly', 'ful', 'less', 'ous', 'ive'))
    
    def is_functional_word(self, word: str) -> bool:
        """Check if word is functional"""
        functional_words = ['the', 'a', 'an', 'is', 'are', 'was', 'were',
                          'be', 'been', 'being', 'have', 'has', 'had']
        return word in functional_words