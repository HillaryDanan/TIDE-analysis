#!/bin/bash
# TIDE Quick Start Script
# Makes everything super simple!

echo "🚀 TIDE Quick Start!"
echo "=================="

# Create directories
echo "📁 Creating directories..."
mkdir -p prompts
mkdir -p results/data
mkdir -p results/analysis
mkdir -p results/visualizations
mkdir -p results/checkpoints

# Create default prompt files
echo "📝 Creating default prompts..."

# Concrete prompts
cat > prompts/concrete_prompts.json << 'EOF'
[
  "Describe the physical properties of water",
  "What does a tree look like?",
  "Explain the texture of sand",
  "Describe the taste of chocolate",
  "What color is the sky?",
  "How does rain feel on your skin?",
  "Describe the sound of ocean waves",
  "What does fresh bread smell like?",
  "Explain the shape of a circle",
  "Describe the temperature of ice",
  "What does grass feel like?",
  "Describe the appearance of a mountain",
  "How does silk feel to touch?",
  "What does coffee taste like?",
  "Describe the sound of thunder"
]
EOF

# Internal prompts
cat > prompts/internal_prompts.json << 'EOF'
[
  "How does happiness feel?",
  "What is empathy?",
  "Describe the feeling of nostalgia",
  "What does it mean to trust someone?",
  "How would you comfort a sad friend?",
  "What is the nature of consciousness?",
  "Describe the emotion of pride",
  "What makes a good friendship?",
  "How does guilt affect behavior?",
  "What is the meaning of love?",
  "Describe the feeling of loneliness",
  "What is compassion?",
  "How does anxiety manifest?",
  "What brings inner peace?",
  "Describe the nature of hope"
]
EOF

# External prompts
cat > prompts/external_prompts.json << 'EOF'
[
  "Calculate the area of a circle with radius 5",
  "What is the distance between Earth and Moon?",
  "Explain the concept of time",
  "How many seconds in an hour?",
  "Describe spatial relationships",
  "What is the speed of light?",
  "Explain coordinate systems",
  "How do you measure angles?",
  "What is the volume of a cube?",
  "Describe the concept of infinity",
  "Calculate 15% of 200",
  "What is a prime number?",
  "Explain the Pythagorean theorem",
  "How do you convert Celsius to Fahrenheit?",
  "What is the golden ratio?"
]
EOF

# Create .env template if it doesn't exist
if [ ! -f .env ]; then
    echo "🔑 Creating .env template..."
    cat > .env << 'EOF'
# Add your API keys here
ANTHROPIC_API_KEY=your-claude-key-here
OPENAI_API_KEY=your-openai-key-here
GOOGLE_API_KEY=your-gemini-key-here
EOF
    echo "⚠️  Please edit .env and add your API keys!"
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo "=================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your API keys"
echo "2. Run: python test_connection.py"
echo "3. Run: python tide_automation.py"
echo ""
echo "<4577! 💕"