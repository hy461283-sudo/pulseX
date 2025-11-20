# Twitter Real-time Analysis Dashboard Guide

## 🚀 Quick Start

### Running the Dashboard

```bash
cd RealTime-TwitterDataAnalysis/app
source ../venv/bin/activate
streamlit run dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 📊 Features

### 1. **Search & Filter**
- **Keyword Search**: Enter any keyword or hashtag (e.g., #google, #apple, AI) in the sidebar
- **Time Period Selection**: Choose from 4 clear options:
  - 7 Days
  - 14 Days
  - 21 Days
  - 28 Days

### 2. **Automatic Real-time Twitter API Integration**
- **Automatic Fetching**: When you type a keyword and press Enter, the dashboard will:
  - Automatically hit the Twitter API
  - Fetch real-time tweets for that keyword
  - Analyze sentiment in real-time
  - Display comprehensive insights
- **No manual toggle needed** - it works automatically when API is configured!

**Note**: To use Twitter API:
1. Get credentials from https://developer.twitter.com
2. Update `app/twitter_config.py` with your:
   - API Key
   - API Secret Key
   - Access Token
   - Access Token Secret

### 3. **Analytics Provided**

#### Metrics:
- 📝 Total Tweets
- 😊 Average Sentiment Score
- 🔄 Total Retweets
- ❤️ Total Favorites

#### Visualizations:
- **Sentiment Distribution**: Pie chart showing Positive/Neutral/Negative breakdown
- **Sentiment Score Distribution**: Histogram of sentiment scores
- **Tweet Volume Over Time**: Line chart showing tweet activity
- **Average Sentiment Over Time**: Trend of sentiment changes
- **Most Engaging Tweets**: Top 5 tweets by engagement

#### Insights:
- Dominant sentiment and percentage
- Tweet volume for searched keyword
- Sentiment score range
- Analysis time period
- Sentiment breakdown (Positive, Neutral, Negative counts)

## 🎯 How to Use

### For Cached Data (Default):
1. Run the dashboard
2. Enter a keyword in the search bar (e.g., #google)
3. Select your desired time period (7, 14, 21, or 28 days)
4. View the analysis

### For Real-time Twitter Data:
1. Configure Twitter API credentials in `twitter_config.py`
2. Run the dashboard
3. Enter a keyword in the search bar
4. Select time period (7, 14, 21, or 28 days)
5. **The dashboard will automatically fetch live tweets and analyze them!**
6. View real-time sentiment analysis and insights

## 📈 Data Explanation

### Sentiment Score:
- **Range**: -1.0 (most negative) to +1.0 (most positive)
- **Positive**: Score >= 0.05
- **Neutral**: Score between -0.05 and 0.05
- **Negative**: Score <= -0.05

### Engagement:
- Calculated as: Retweets + Favorites
- Higher engagement indicates more popular tweets

### Trend Analysis:
- Shows how tweet volume and sentiment change over time
- Helps identify patterns and trending topics

## 🔧 Troubleshooting

### No data showing?
```bash
cd app
python generate_sample_data.py
```

### Twitter API not working?
- Check your credentials in `twitter_config.py`
- Ensure you have proper API access level
- Verify your API rate limits

### Dashboard not loading?
```bash
# Restart the dashboard
streamlit run dashboard.py --server.port 8501
```

## 💡 Tips

1. **Start with cached data** to understand the dashboard before using Twitter API
2. **Use specific keywords** for better results (e.g., #iPhone instead of just phone)
3. **Compare time periods** to see how sentiment changes over time
4. **Check engagement metrics** to find the most impactful tweets

## 📝 Sample Data

The project includes a sample data generator that creates 1000 tweets spanning 30 days with:
- Random distribution of #google and #apple hashtags
- Varied sentiment (positive, neutral, negative)
- Realistic engagement metrics
- Proper timestamp distribution

Regenerate sample data anytime:
```bash
python generate_sample_data.py
```
