# 🐵 CHIMPANZEE INSTRUCTIONS - SUPER SIMPLE!

## 🚀 WHAT THIS DOES:
Automates everything from your dissertation + TIDE to collect AI consciousness data!

## 📦 STEP 1: SETUP (Do Once)
```bash
# Copy these commands one by one:
pip install openai anthropic google-generativeai pandas numpy scipy matplotlib
pip install python-dotenv requests json5
```

## 🔑 STEP 2: ADD YOUR API KEYS
Create a file called `.env` and add:
```
ANTHROPIC_API_KEY=your-claude-key-here
OPENAI_API_KEY=your-openai-key-here
GOOGLE_API_KEY=your-gemini-key-here
```

## 🏃 STEP 3: RUN EVERYTHING!
```bash
# This does EVERYTHING automatically:
python3 tide_automation.py
```

## 📊 WHAT HAPPENS:
1. **Collects data** from 4 AI models (Claude, GPT-4, Gemini)
2. **Runs your dissertation tests** (internal/external/concrete)
3. **Analyzes patterns** like CCDF→CCDR
4. **Saves everything** automatically
5. **Makes pretty graphs** in the `results/` folder

## 🎯 CUSTOMIZE (Optional):
- Want more sessions? Change `sessions_per_model` in config.json
- Want different prompts? Edit `prompts/` folder files
- Want to test specific models? Edit `models` list in config.json

## 📁 OUTPUT:
- `results/data/` - Raw data from all sessions
- `results/analysis/` - Pattern analysis results  
- `results/visualizations/` - Pretty graphs!
- `results/report.html` - Open this to see everything!

## 🆘 IF SOMETHING BREAKS:
1. Check your API keys are correct
2. Make sure you have internet
3. Run `python test_connection.py` to check APIs work
4. Message me with the error!

## 🎉 THAT'S IT!
Just run `python tide_automation.py` and watch the magic happen!

<4577! 🐵✨