# ♟️ Chess.com Analytics Dashboard

A comprehensive web-based analytics dashboard for analyzing chess.com game data. Enter any chess.com username and get instant insights including performance statistics, rating progression, opening analysis, optimal playing times, and personalized improvement suggestions.

![Chess Analytics Dashboard](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🌟 Features

- **📊 Comprehensive Statistics**: Win/loss/draw ratios, rating progression, and performance metrics
- **🎯 Opening Analysis**: Identify your strongest and weakest openings with statistical significance
- **⏰ Temporal Insights**: Discover your best performing times of day and days of the week
- **🎨 Color Performance**: Compare your performance playing White vs Black pieces
- **⏱️ Time Class Analysis**: Performance breakdown across Bullet, Blitz, Rapid, and Daily games
- **📈 Rating Tracking**: Visualize your rating progression over time
- **💡 AI-Powered Suggestions**: Get personalized recommendations to improve your game
- **💾 Data Export**: Download your analyzed data in CSV format

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/sanjaykshetri/chess_dot_com_data_analysis.git
cd chess_dot_com_data_analysis
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the Dashboard

Start the Streamlit application:

```bash
streamlit run app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

## 📖 How to Use

1. **Enter Username**: Type your chess.com username in the sidebar
2. **Select Options**: Choose how many months of data to analyze and your timezone
3. **Analyze**: Click the "🔍 Analyze My Games" button
4. **Explore**: Browse through various analytics sections and insights
5. **Download**: Export your data and analysis results as CSV files

## 🏗️ Project Structure

```
chess_dot_com_data_analysis/
│
├── app.py                          # Main Streamlit dashboard application
├── chess_data_fetcher.py          # Module for fetching data from Chess.com API
├── chess_data_analyzer.py         # Module for analyzing chess game data
├── requirements.txt               # Python dependencies
├── README.md                      # This file
│
├── fetch_chess_data.py            # Legacy CLI script for data fetching
├── chess_analysis.ipynb           # Jupyter notebook for analysis
├── chess_importer.ipynb           # Jupyter notebook for data import
│
└── [data files]                   # CSV and PGN files (generated)
```

## 🔧 Key Modules

### `chess_data_fetcher.py`
Handles all interactions with the Chess.com API:
- User validation
- Game data fetching
- Data preprocessing and structuring
- PGN parsing for opening names and termination reasons

### `chess_data_analyzer.py`
Performs comprehensive analysis on chess game data:
- Statistical calculations
- Performance metrics by various dimensions
- Opening repertoire analysis
- Time-based pattern identification
- Improvement suggestion generation

### `app.py`
Streamlit web application providing:
- Interactive user interface
- Real-time data fetching and analysis
- Rich visualizations using Plotly
- Data export functionality

## 📊 Analysis Components

### Overview Statistics
- Total games played
- Win/draw/loss counts and percentages
- Current rating and rating change
- Playing frequency and time investment

### Performance Analysis
- **By Color**: White vs Black performance comparison
- **By Time Control**: Bullet, Blitz, Rapid, Daily analysis
- **By Time of Day**: Hourly performance patterns
- **By Day of Week**: Weekly performance trends

### Opening Analysis
- Statistical analysis of opening performance
- Identification of top 5 strengths and weaknesses
- Minimum game threshold filtering (20+ games)
- ECO code and opening name tracking

### Rating Progression
- Visual tracking of rating over time
- Game-by-game rating changes
- Trend analysis

### Improvement Suggestions
AI-powered recommendations based on:
- Color-specific weaknesses
- Time control performance gaps
- Opening repertoire weaknesses
- Optimal playing time identification
- Recent performance trends

## 🛠️ Technical Details

### Chess.com API
The dashboard uses the public Chess.com API:
- **Endpoint**: `https://api.chess.com/pub`
- **Rate Limiting**: Respectful delays (150ms between requests)
- **Data Format**: JSON responses converted to pandas DataFrames

### Data Processing
1. Fetch monthly archives for specified timeframe
2. Extract game data including PGN, ratings, and results
3. Parse PGN for opening information and termination
4. Calculate derived features (scores, time-based attributes)
5. Aggregate and analyze across multiple dimensions

### Visualization
- **Plotly**: Interactive charts and graphs
- **Streamlit**: Native components for metrics and data display
- **Custom CSS**: Enhanced UI styling

## 📝 Example Analysis Output

```
Total Games: 10,501
Win Rate: 47.2%
Current Rating: 1347
Rating Change: +377
Days Playing: 2,099
Average Games/Day: 5.0

Best Opening: Italian Game (C55) - 61.2% score
Weakest Opening: Bird's Opening (A03) - 25.8% score
Best Time to Play: 14:00-17:00
Best Day: Saturday (52.3% score)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Sanjay Kshetri**

- GitHub: [@sanjaykshetri](https://github.com/sanjaykshetri)
- Chess.com: [sanjaykshetri123](https://www.chess.com/member/sanjaykshetri123)

## 🙏 Acknowledgments

- Chess.com for providing the public API
- Streamlit for the excellent web framework
- The chess community for inspiration

## 📧 Contact

For questions, suggestions, or feedback, please open an issue on GitHub or reach out through the repository.

---

**Built with ♟️ by a chess enthusiast for chess enthusiasts**
