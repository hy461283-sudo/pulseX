# 🐦 Xpluse - Twitter Real-time Analysis Dashboard

A powerful real-time Twitter sentiment analysis dashboard that automatically fetches and analyzes tweets using Twitter API v2.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![Twitter API](https://img.shields.io/badge/Twitter%20API-v2-1DA1F2)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

### 🔄 Automatic Twitter API Integration
- **Real-time data fetching** - Automatically hits Twitter API when you search
- **No manual toggles** - Just type a keyword and get instant results
- **100 tweets per search** - Optimized for speed and efficiency
- **Twitter API v2** - Uses latest Bearer Token authentication

### 📊 Comprehensive Analytics
- **Sentiment Analysis** - VADER-based sentiment scoring
- **Interactive Visualizations** - Pie charts, histograms, time series
- **Engagement Metrics** - Retweets, favorites, and total engagement
- **Trend Analysis** - Tweet volume and sentiment over time
- **Top Tweets** - Most engaging tweets with sentiment scores

### 🎯 User-Friendly Interface
- **Clean Design** - Twitter blue theme with intuitive layout
- **Date Range Filters** - 1, 3, 7, 14, 21, 28 days options
- **Real-time Updates** - Live data processing and visualization
- **Detailed Insights** - Dominant sentiment, score ranges, time periods

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Twitter Developer Account (for API access)
- Bearer Token from Twitter Developer Portal

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/Xpluse.git
cd Xpluse
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Twitter API**
Edit `app/twitter_config.py` and add your Bearer Token:
```python
bearer_token = "YOUR_BEARER_TOKEN_HERE"
```

5. **Generate sample data (optional)**
```bash
cd app
python generate_sample_data.py
```

6. **Run the dashboard**
```bash
streamlit run dashboard.py
```

7. **Open in browser**
Navigate to `http://localhost:8501`

## 📖 Usage

### Search for Keywords
1. Type any keyword in the search bar (e.g., `#google`, `AI`, `bitcoin`)
2. Select time period (1, 3, 7, 14, 21, or 28 days)
3. Dashboard automatically fetches 100 live tweets
4. View comprehensive sentiment analysis in ~5 seconds

### Example Searches
- `#google` - Google-related tweets
- `#apple` - Apple-related tweets
- `AI` - Artificial Intelligence discussions
- `bitcoin` - Cryptocurrency tweets
- `#climate` - Climate change discussions
- `iPhone` - iPhone-related tweets

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib
- **Sentiment Analysis**: NLTK (VADER)
- **Twitter API**: Tweepy (v2)
- **Language**: Python 3.13

## 📊 What You Get

### Metrics
- 📝 Total Tweets
- 😊 Average Sentiment Score
- 🔄 Total Retweets
- ❤️ Total Favorites

### Visualizations
- **Sentiment Distribution** - Pie chart showing Positive/Neutral/Negative breakdown
- **Sentiment Score Distribution** - Histogram of sentiment scores
- **Tweet Volume Over Time** - Line chart showing tweet frequency
- **Sentiment Trend Over Time** - How sentiment changes over time
- **Top 5 Engaging Tweets** - Most popular tweets with metrics

### Insights
- Dominant sentiment and percentage
- Tweet volume for keyword
- Sentiment score range (-1 to +1)
- Analysis time period
- Detailed sentiment breakdown

## ⚡ Performance

- **Average Response Time**: 4-6 seconds
- **API Calls**: 1 call per search
- **Tweets Fetched**: Up to 100 per search
- **Processing**: Real-time sentiment analysis
- **Visualization**: Instant chart generation

## 🔑 Twitter API Setup

1. Go to [Twitter Developer Portal](https://developer.twitter.com)
2. Create a new project and app
3. Generate Bearer Token
4. Copy token to `app/twitter_config.py`
5. Start searching!

### API Limits (Free Tier)
- 500,000 tweets per month
- 100 tweets per request
- Recent search (last 7 days)
- Basic tweet fields

## 📁 Project Structure

```
Xpluse/
├── app/
│   ├── dashboard.py              # Main Streamlit dashboard
│   ├── twitter_config.py         # Twitter API configuration
│   ├── generate_sample_data.py   # Sample data generator
│   ├── sentiment_analysis.py     # Sentiment analysis module
│   ├── tweets_data.py            # Data processing
│   └── tweets.json               # Cached tweets
├── requirements.txt              # Python dependencies
├── QUICK_START.md               # Quick start guide
├── DASHBOARD_GUIDE.md           # Complete documentation
├── FEATURES.md                  # Detailed features
└── README.md                    # This file
```

## 🎓 How It Works

```
User Types Keyword
        ↓
Dashboard Detects Input
        ↓
Automatically Calls Twitter API v2
        ↓
Fetches 100 Live Tweets (2-3s)
        ↓
Analyzes Sentiment with VADER (1-2s)
        ↓
Generates Visualizations (1s)
        ↓
Displays Complete Results (~5s total)
```

## 🐛 Troubleshooting

### Dashboard won't start?
```bash
streamlit run dashboard.py --server.port 8501
```

### No data showing?
```bash
python generate_sample_data.py
```

### Twitter API errors?
- Check Bearer Token in `twitter_config.py`
- Verify token is valid on Twitter Developer Portal
- Check rate limits (free tier: 500,000 tweets/month)

### Rate limit exceeded?
Wait 15 minutes or use alternative Bearer Token

## 📚 Documentation

- **QUICK_START.md** - Fast setup guide
- **DASHBOARD_GUIDE.md** - Complete documentation
- **FEATURES.md** - Detailed feature list
- **SETUP_COMPLETE.md** - Configuration guide

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 🌟 Features Roadmap

- [ ] Multiple Bearer Token rotation
- [ ] Export results to CSV/PDF
- [ ] Word cloud visualization
- [ ] Historical data comparison
- [ ] Custom date range picker
- [ ] Multi-keyword comparison
- [ ] Email alerts for sentiment changes
- [ ] Advanced filtering options

## 💡 Use Cases

- **Marketing**: Track brand sentiment
- **Research**: Public opinion analysis
- **Business**: Competitor monitoring
- **Personal**: Topic exploration
- **Education**: Social media analytics learning

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ using Python, Streamlit, and Twitter API v2**

⭐ Star this repo if you find it useful!
