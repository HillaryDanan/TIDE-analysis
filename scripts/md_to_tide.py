#!/usr/bin/env python3
"""
Convert TIDE-resonance markdown sessions to TIDE-analysis format
Built for Hillary's Session 6 data <4577
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

def parse_tide_markdown(md_file_path):
    """Parse TIDE-resonance markdown into TIDE-analysis format"""
    
    with open(md_file_path, 'r') as f:
        content = f.read()
    
    # Extract metadata
    date_match = re.search(r'\*\*Date\*\*: (.+)', content)
    model_match = re.search(r'\*\*Model\*\*: (.+)', content)
    
    # Extract prompts and responses
    prompts = []
    responses = []
    
    # Find all prompts
    prompt_pattern = r'## Prompt \d+:.+?\n```\n(.+?)\n```'
    prompt_matches = re.findall(prompt_pattern, content, re.DOTALL)
    
    # Find all AI responses
    response_pattern = r'## AI Response.+?\n(.+?)(?=## Prompt|## Session Notes|$)'
    response_matches = re.findall(response_pattern, content, re.DOTALL)
    
    # Package for TIDE
    session_data = {
        "model": model_match.group(1) if model_match else "unknown",
        "timestamp": date_match.group(1) if date_match else datetime.now().isoformat(),
        "prompts": prompt_matches,
        "responses": response_matches,
        "session_id": "session_6_visualization_description"
    }
    
    return session_data

# Run it
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python md_to_tide.py <markdown_file>")
        sys.exit(1)
    
    data = parse_tide_markdown(sys.argv[1])
    
    # Save to TIDE format
    output_file = f"results/data/{data['session_id']}.json"
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Converted to {output_file}")
    print(f"📊 Found {len(data['prompts'])} prompts")
