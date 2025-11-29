# 🚀 Quick Start Guide

## Get Started in 3 Steps!

### Step 1: Start the Dashboard
```bash
./run_dashboard.sh
```

Or manually:
```bash
source venv/bin/activate
streamlit run app.py
```

### Step 2: Open in Browser
Visit: **http://localhost:8501**

### Step 3: Analyze!
1. Enter your chess.com username
2. Select months of data (1-60)
3. Choose your timezone
4. Click "🔍 Analyze My Games"

## 📱 What You'll See

### 📊 Overview
- Total games, wins, losses, draws
- Current rating and improvement
- Time invested in chess

### 🎨 Performance Breakdown
- White vs Black performance
- Bullet vs Blitz vs Rapid stats
- Best hours and days to play

### ♟️ Opening Analysis
- Your 5 strongest openings
- Your 5 weakest openings (areas to study)

### 📈 Rating Progression
- Visual chart of your rating over time

### 💡 AI Suggestions
- Personalized tips to improve
- Data-driven recommendations

### 💾 Export Data
- Download your game history as CSV
- Export opening analysis

## 🎯 Example Usernames to Try

- `sanjaykshetri123` (your original data)
- `magnuscarlsen` (World Champion)
- `hikaru` (GM Hikaru Nakamura)
- Any other chess.com username!

## 🛠️ Troubleshooting

**Port already in use?**
```bash
# Find and kill the process
lsof -i :8501
kill -9 <PID>
```

**Dashboard not loading?**
```bash
# Check the logs
tail -f streamlit.log
```

**Need to reinstall?**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## 📧 Questions?

Check the full README.md for detailed documentation!

---

**Happy Analyzing!** ♟️📊
