# 🚀 Quick Start Guide

## Run the Dashboard in 3 Steps

### 1. Install Dependencies
```bash
cd RealTime-TwitterDataAnalysis
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Generate Sample Data (Optional)
```bash
cd app
python generate_sample_data.py
```

### 3. Launch Dashboard
```bash
streamlit run dashboard.py
```

The dashboard will open at: **http://localhost:8501**

---

## 🔑 How It Works

### Without Twitter API (Using Sample Data)
1. Type any keyword (e.g., `#google`, `#apple`)
2. Select time period (7, 14, 21, or 28 days)
3. View analysis from cached sample data

### With Twitter API (Live Data)
1. **Configure API** - Update `app/twitter_config.py` with your Twitter credentials:
   ```python
   api_key = 'your_actual_api_key'
   api_secret_key = 'your_actual_api_secret'
   access_token = 'your_actual_access_token'
   access_token_secret = 'your_actual_access_token_secret'
   ```

2. **Search** - Type any keyword in the search bar

3. **Automatic Fetch** - Dashboard automatically:
   - Hits Twitter API
   - Fetches up to 200 live tweets
   - Analyzes sentiment
   - Shows real-time insights

---

## 📊 What You'll See

- **Sentiment Analysis**: Positive/Neutral/Negative breakdown
- **Tweet Volume**: How many tweets over time
- **Sentiment Trends**: How sentiment changes over time
- **Top Tweets**: Most engaging tweets
- **Key Insights**: Dominant sentiment, score ranges, time periods

---

## 🎯 Example Searches

Try these keywords:
- `#google` - Google-related tweets
- `#apple` - Apple-related tweets
- `AI` - Artificial Intelligence discussions
- `#bitcoin` - Cryptocurrency tweets
- `#climate` - Climate change discussions

---

## ⚙️ Date Range Options

Choose from:
- **7 Days** - Last week
- **14 Days** - Last 2 weeks
- **21 Days** - Last 3 weeks
- **28 Days** - Last 4 weeks

---

## 🔧 Troubleshooting

**Dashboard won't start?**
```bash
streamlit run dashboard.py --server.port 8501
```

**No data showing?**
```bash
python generate_sample_data.py
```

**Twitter API errors?**
- Check your credentials in `twitter_config.py`
- Verify API access level on Twitter Developer Portal
- Check rate limits

---

## 📚 Full Documentation

See [DASHBOARD_GUIDE.md](DASHBOARD_GUIDE.md) for complete documentation.

---

## 🎉 You're Ready!

Start analyzing Twitter sentiment in real-time! 🐦
