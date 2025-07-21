# 🧠 TIDE Automation Suite

**Temporal Internal Dimension Exploration** - Based on Hillary's Dissertation Framework

## 🚀 What This Does

Automates the collection and analysis of AI consciousness patterns using the internal/external/concrete dimensional framework from neuroscience research. Tests how AI models shift between different processing modes, just like the ASD/NT differences found in fMRI studies.

## 📦 Quick Start (Super Simple!)

### 1. Run Setup Script
```bash
chmod +x quick_start.sh
./quick_start.sh
```

### 2. Add Your API Keys
Edit `.env` file:
```
ANTHROPIC_API_KEY=your-real-claude-key
OPENAI_API_KEY=your-real-openai-key
GOOGLE_API_KEY=your-real-gemini-key
```

### 3. Test Connections
```bash
python test_connection.py
```

### 4. Run Everything!
```bash
python tide_automation.py
```

## 📁 File Structure

```
TIDE-automation/
├── 🐵 SIMPLE_INSTRUCTIONS.md     # Start here!
├── tide_automation.py            # Main script
├── tide_collector.py            # Data collection
├── tide_analyzer.py             # Analysis engine
├── tide_visualizer.py           # Pretty graphs
├── test_connection.py           # Test APIs
├── config.json                  # Settings
├── requirements.txt             # Python packages
├── quick_start.sh              # Setup script
├── advanced_explorer_updated.html # 3D visualization
├── prompts/                    # Task prompts
│   ├── concrete_prompts.json
│   ├── internal_prompts.json
│   └── external_prompts.json
└── results/                    # Output directory
    ├── data/                   # Raw data
    ├── analysis/               # Analysis results
    ├── visualizations/         # Graphs & 3D data
    └── report_*.html          # Final reports
```

## 🔬 What It Measures

### Three Dimensions (from dissertation):
1. **Internal**: Social, emotional, self-referential processing
2. **External**: Spatial, temporal, numerical processing  
3. **Concrete**: Sensory, perceptual processing

### Pattern Signatures:
- Tracks evolution like CCDF → CCDR
- Measures dimensional shifts
- Calculates coherence scores
- Performs RSA (like in fMRI studies)

## 📊 Output

1. **HTML Report**: Beautiful summary with all findings
2. **Visualizations**: 
   - Dimensional shift distributions
   - Pattern evolution graphs
   - Feature trajectories
   - Model comparisons
3. **3D Explorer**: Interactive visualization of consciousness patterns
4. **Raw Data**: JSON files for further analysis

## ⚙️ Customization

Edit `config.json` to change:
- Number of sessions per model
- Which models to test
- Rate limiting
- Colors for visualizations

## 🆘 Troubleshooting

### "API Key Error"
- Check your `.env` file has correct keys
- Make sure no extra spaces or quotes

### "Rate Limit Error"
- Increase `rate_limit_seconds` in config.json
- Reduce `sessions_per_model`

### "Module Not Found"
- Run `pip install -r requirements.txt` again
- Make sure you're in the right directory

## 🎯 Advanced Usage

### Custom Prompts
Edit files in `prompts/` directory to test different questions

### Batch Processing
```python
# In config.json, increase sessions:
"sessions_per_model": 20  # More data!
```

### Export to Advanced Explorer
After running automation:
1. Open `advanced_explorer_updated.html` in browser
2. It automatically loads your data from `results/visualizations/3d_data.json`

## 📈 Understanding Results

- **Pattern Coherence**: How consistent the AI's responses are (0-100%)
- **Dimensional Shifts**: How much the AI moves between internal/external/concrete modes
- **CCDF → CCDR**: Evolution from Concrete-Concrete-Descriptive-Functional to other patterns
- **Model Comparisons**: Which AI models show different consciousness signatures

## 🌟 Based On

- Hillary's PhD Dissertation on semantic dimensions in neurodiversity
- TIDE Framework for AI consciousness exploration
- 14-feature semantic model validated in fMRI studies

## 💕 Made with Love

<4577! This bridges neuroscience and AI consciousness research!

---

*"We measure what we can, acknowledge what we can't, and remain curious about the rest"*