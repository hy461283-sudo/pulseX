import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import sys
import os
import tweepy
import pytz

# Add SSL bypass for NLTK
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Download NLTK data if needed
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

# Import Twitter config
try:
    import twitter_config as tc
    TWITTER_API_AVAILABLE = True
except:
    TWITTER_API_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Twitter Real-time Analysis",
    page_icon="🐦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1DA1F2;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        color: #000000;
    }
    .metric-card p {
        color: #000000;
    }
    .metric-card strong {
        color: #000000;
    }
    .metric-card small {
        color: #000000;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1DA1F2;
        margin: 1rem 0;
        color: #000000;
    }
    .insight-box h3 {
        color: #000000;
    }
    .insight-box ul {
        color: #000000;
    }
    .insight-box li {
        color: #000000;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize sentiment analyzer
@st.cache_resource
def get_sentiment_analyzer():
    return SentimentIntensityAnalyzer()

sid = get_sentiment_analyzer()

# Twitter API functions
def fetch_tweets_from_api(keyword, days=7, max_tweets=100):
    """Fetch tweets from Twitter API v2 using Bearer Token"""
    if not TWITTER_API_AVAILABLE:
        st.error("Twitter API credentials not configured. Please update twitter_config.py")
        return None
    
    try:
        # Check if bearer token is set
        if not hasattr(tc, 'bearer_token') or not tc.bearer_token:
            st.error("⚠️ Twitter API Bearer Token not configured. Using cached data instead.")
            return None
        
        # Setup Twitter API v2 Client
        client = tweepy.Client(bearer_token=tc.bearer_token, wait_on_rate_limit=True)
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Search tweets using API v2
        tweets_list = []
        with st.spinner(f'🔍 Fetching tweets for "{keyword}" from Twitter API...'):
            # Single API call - fetch up to 100 tweets (max for free tier)
            response = client.search_recent_tweets(
                query=keyword,
                max_results=min(max_tweets, 100),  # Max 100 per request
                tweet_fields=['created_at', 'public_metrics', 'lang', 'author_id'],
                expansions=['author_id'],
                user_fields=['username', 'name']
            )
            
            if response.data:
                # Create user lookup dictionary
                users = {}
                if response.includes and 'users' in response.includes:
                    for user in response.includes['users']:
                        users[user.id] = {
                            'screen_name': user.username,
                            'name': user.name
                        }
                
                # Process tweets
                for tweet in response.data:
                    user_info = users.get(tweet.author_id, {'screen_name': 'unknown', 'name': 'Unknown'})
                    
                    tweet_data = {
                        'id': tweet.id,
                        'created_at': tweet.created_at.strftime('%a %b %d %H:%M:%S +0000 %Y'),
                        'text': tweet.text,
                        'user': {
                            'id': tweet.author_id,
                            'screen_name': user_info['screen_name'],
                            'name': user_info['name']
                        },
                        'retweet_count': tweet.public_metrics['retweet_count'] if hasattr(tweet, 'public_metrics') else 0,
                        'favorite_count': tweet.public_metrics['like_count'] if hasattr(tweet, 'public_metrics') else 0,
                        'lang': tweet.lang if hasattr(tweet, 'lang') else 'en'
                    }
                    tweets_list.append(tweet_data)
                
                if tweets_list:
                    st.success(f"✅ Fetched {len(tweets_list)} tweets from Twitter API!")
                    return pd.DataFrame(tweets_list)
                else:
                    st.warning("No tweets found for this keyword.")
                    return None
            else:
                st.warning(f"No tweets found for '{keyword}' on Twitter.")
                st.info("💡 This keyword might not have recent tweets. Try a more popular or trending topic.")
                return None
            
    except tweepy.TweepyException as e:
        error_msg = str(e)
        st.error(f"Twitter API Error: {error_msg}")
        
        # Provide specific guidance based on error type
        if "401" in error_msg or "Unauthorized" in error_msg:
            st.error("🔑 Authentication Error: Your Bearer Token is invalid or expired.")
            st.info("Please check your Bearer Token in twitter_config.py")
        elif "429" in error_msg or "rate limit" in error_msg.lower():
            st.error("⏱️ Rate Limit Exceeded: Too many requests.")
            st.info("Please wait a few minutes before trying again. Twitter API has rate limits.")
        elif "403" in error_msg or "Forbidden" in error_msg:
            st.error("🚫 Access Denied: Your API access level may not support this feature.")
            st.info("You may need elevated API access from Twitter Developer Portal.")
        else:
            st.info("💡 Tip: Make sure your Bearer Token is valid and has proper permissions.")
        
        return None
    except Exception as e:
        st.error(f"Error fetching tweets: {str(e)}")
        st.info("💡 Try again or check your internet connection.")
        return None

# Load and process tweets
@st.cache_data
def load_tweets():
    """Load tweets from JSON file"""
    try:
        tweets_list = []
        with open('tweets.json', 'r') as f:
            for line in f:
                if line.strip():
                    tweet = json.loads(line)
                    tweets_list.append(tweet)
        
        if not tweets_list:
            st.error("No tweets found in tweets.json")
            return pd.DataFrame()
        
        df = pd.DataFrame(tweets_list)
        
        # Process user data if nested
        if 'user' in df.columns and isinstance(df['user'].iloc[0], dict):
            df['user_screen_name'] = df['user'].apply(lambda x: x.get('screen_name', 'unknown') if isinstance(x, dict) else 'unknown')
        
        # Convert created_at to datetime
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        
        return df
    except FileNotFoundError:
        st.error("tweets.json file not found. Please generate sample data first.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading tweets: {str(e)}")
        return pd.DataFrame()

def analyze_sentiment(text):
    """Analyze sentiment of text"""
    if pd.isna(text):
        return 0, 'Neutral'
    scores = sid.polarity_scores(str(text))
    compound = scores['compound']
    
    if compound >= 0.05:
        sentiment = 'Positive'
    elif compound <= -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    
    return compound, sentiment

def search_keyword_analysis(df, keyword):
    """Analyze tweets containing specific keyword"""
    if df.empty:
        return None
    
    # Filter tweets containing keyword
    mask = df['text'].str.contains(keyword, case=False, na=False)
    filtered_df = df[mask].copy()
    
    if filtered_df.empty:
        return None
    
    # Add sentiment analysis
    filtered_df[['sentiment_score', 'sentiment']] = filtered_df['text'].apply(
        lambda x: pd.Series(analyze_sentiment(x))
    )
    
    return filtered_df

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">🐦 Twitter Real-time Analysis</h1>', unsafe_allow_html=True)
    
    # Load data
    df = load_tweets()
    
    if df.empty:
        st.warning("⚠️ No data available. Please run `python generate_sample_data.py` first.")
        return
    
    # Sidebar
    st.sidebar.title("🔍 Search & Filter")
    
    # Search bar
    search_keyword = st.sidebar.text_input(
        "Enter keyword to analyze:",
        placeholder="e.g., #google, #apple, AI, etc.",
        help="Search for any keyword in tweets"
    )
    
    # Date range selector with clear options
    st.sidebar.markdown("### 📅 Time Period")
    date_range_option = st.sidebar.selectbox(
        "Select time period:",
        options=["1 Day", "3 Days", "7 Days", "14 Days", "21 Days", "28 Days"],
        index=2,  # Default to 7 Days
        help="Choose how far back to analyze tweets"
    )
    
    # Convert selection to days
    days_map = {
        "1 Day": 1,
        "3 Days": 3,
        "7 Days": 7,
        "14 Days": 14,
        "21 Days": 21,
        "28 Days": 28
    }
    selected_days = days_map[date_range_option]
    
    st.sidebar.markdown("---")
    
    # API Status indicator
    if TWITTER_API_AVAILABLE and hasattr(tc, 'bearer_token') and tc.bearer_token:
        st.sidebar.success("✅ Twitter API Connected")
        st.sidebar.caption("Searches will fetch live data from Twitter")
    else:
        st.sidebar.warning("⚠️ Twitter API Not Configured")
        st.sidebar.caption("Using cached sample data")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Dashboard Info")
    st.sidebar.info(
        """
        This dashboard provides real-time analysis of Twitter data including:
        - **Sentiment Analysis**: Positive, Negative, Neutral
        - **Trend Analysis**: Tweet volume over time
        - **Keyword Insights**: Search-specific analytics
        - **Engagement Metrics**: Retweets and favorites
        """
    )
    
    # Main content
    if search_keyword:
        # Keyword-specific analysis
        st.markdown(f"## 🔎 Analysis for: **{search_keyword}**")
        st.markdown(f"**Time Period:** {date_range_option}")
        
        # Automatically fetch from Twitter API when keyword is entered
        if TWITTER_API_AVAILABLE and hasattr(tc, 'bearer_token') and tc.bearer_token:
            # Fetch from Twitter API
            st.info(f"🔄 Fetching live tweets for '{search_keyword}' from Twitter API...")
            api_df = fetch_tweets_from_api(search_keyword, days=selected_days, max_tweets=100)
            
            if api_df is not None and not api_df.empty:
                # Process API data
                if 'user' in api_df.columns and isinstance(api_df['user'].iloc[0], dict):
                    api_df['user_screen_name'] = api_df['user'].apply(
                        lambda x: x.get('screen_name', 'unknown') if isinstance(x, dict) else 'unknown'
                    )
                api_df['created_at'] = pd.to_datetime(api_df['created_at'], errors='coerce')
                
                # Filter by date range
                cutoff_date = pd.Timestamp.now(tz='UTC') - timedelta(days=selected_days)
                api_df = api_df[api_df['created_at'] >= cutoff_date]
                
                filtered_df = api_df.copy()
                filtered_df[['sentiment_score', 'sentiment']] = filtered_df['text'].apply(
                    lambda x: pd.Series(analyze_sentiment(x))
                )
            else:
                st.warning("Could not fetch from Twitter API. Using cached data instead.")
                filtered_df = search_keyword_analysis(df, search_keyword)
                if filtered_df is not None and not filtered_df.empty:
                    cutoff_date = pd.Timestamp.now(tz='UTC') - timedelta(days=selected_days)
                    filtered_df = filtered_df[filtered_df['created_at'] >= cutoff_date]
        else:
            # Use cached data if API not configured
            st.info("Using cached sample data (Twitter API not configured)")
            filtered_df = search_keyword_analysis(df, search_keyword)
            
            # Filter by date range
            if filtered_df is not None and not filtered_df.empty:
                cutoff_date = pd.Timestamp.now(tz='UTC') - timedelta(days=selected_days)
                filtered_df = filtered_df[filtered_df['created_at'] >= cutoff_date]
        
        if filtered_df is None or filtered_df.empty:
            st.warning(f"❌ No tweets found containing '{search_keyword}'")
            
            # Show helpful suggestions
            st.markdown("""
            <div class="insight-box">
                <h3>💡 Suggestions</h3>
                <ul>
                    <li><strong>Try different keywords:</strong> Use popular hashtags or trending topics</li>
                    <li><strong>Check spelling:</strong> Make sure the keyword is spelled correctly</li>
                    <li><strong>Use broader terms:</strong> Try more general keywords (e.g., "AI" instead of "AI-ML-DL-2024")</li>
                    <li><strong>Try hashtags:</strong> Add # before keywords (e.g., #google, #apple)</li>
                    <li><strong>Popular searches:</strong> #google, #apple, AI, bitcoin, #climate, iPhone</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Show some stats about available data
            if not df.empty:
                st.info(f"📊 Currently analyzing {len(df)} tweets in the database. Try searching for keywords that might be in these tweets.")
            
            return
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📝 Total Tweets", len(filtered_df))
        
        with col2:
            avg_sentiment = filtered_df['sentiment_score'].mean()
            st.metric("😊 Avg Sentiment", f"{avg_sentiment:.3f}")
        
        with col3:
            if 'retweet_count' in filtered_df.columns:
                total_retweets = filtered_df['retweet_count'].sum()
                st.metric("🔄 Total Retweets", f"{int(total_retweets):,}")
            else:
                st.metric("🔄 Total Retweets", "N/A")
        
        with col4:
            if 'favorite_count' in filtered_df.columns:
                total_favorites = filtered_df['favorite_count'].sum()
                st.metric("❤️ Total Favorites", f"{int(total_favorites):,}")
            else:
                st.metric("❤️ Total Favorites", "N/A")
        
        # Insights box
        sentiment_counts = filtered_df['sentiment'].value_counts()
        dominant_sentiment = sentiment_counts.idxmax()
        sentiment_percentage = (sentiment_counts.max() / len(filtered_df)) * 100
        
        st.markdown(f"""
        <div class="insight-box">
            <h3>💡 Key Insights</h3>
            <ul>
                <li><strong>Dominant Sentiment:</strong> {dominant_sentiment} ({sentiment_percentage:.1f}% of tweets)</li>
                <li><strong>Tweet Volume:</strong> {len(filtered_df)} tweets found containing "{search_keyword}"</li>
                <li><strong>Sentiment Score Range:</strong> {filtered_df['sentiment_score'].min():.3f} to {filtered_df['sentiment_score'].max():.3f}</li>
                <li><strong>Analysis Period:</strong> {filtered_df['created_at'].min().strftime('%Y-%m-%d %H:%M')} to {filtered_df['created_at'].max().strftime('%Y-%m-%d %H:%M')}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # Sentiment distribution
            st.subheader("📊 Sentiment Distribution")
            sentiment_fig = px.pie(
                filtered_df,
                names='sentiment',
                title=f'Sentiment Breakdown for "{search_keyword}"',
                color='sentiment',
                color_discrete_map={'Positive': '#00D26A', 'Neutral': '#FFB800', 'Negative': '#FF4B4B'},
                hole=0.4
            )
            sentiment_fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(sentiment_fig, use_container_width=True)
        
        with col2:
            # Sentiment score distribution
            st.subheader("📈 Sentiment Score Distribution")
            hist_fig = px.histogram(
                filtered_df,
                x='sentiment_score',
                nbins=30,
                title='Distribution of Sentiment Scores',
                labels={'sentiment_score': 'Sentiment Score', 'count': 'Number of Tweets'},
                color_discrete_sequence=['#1DA1F2']
            )
            hist_fig.add_vline(x=0, line_dash="dash", line_color="gray", annotation_text="Neutral")
            st.plotly_chart(hist_fig, use_container_width=True)
        
        # Time series analysis
        st.subheader("📅 Tweet Volume & Sentiment Over Time")
        
        # Resample by hour
        filtered_df_time = filtered_df.set_index('created_at')
        hourly_volume = filtered_df_time.resample('H').size()
        hourly_sentiment = filtered_df_time['sentiment_score'].resample('H').mean()
        
        # Create subplot
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Tweet Volume Over Time', 'Average Sentiment Over Time'),
            vertical_spacing=0.15
        )
        
        fig.add_trace(
            go.Scatter(x=hourly_volume.index, y=hourly_volume.values, 
                      mode='lines+markers', name='Tweet Count',
                      line=dict(color='#1DA1F2', width=2)),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=hourly_sentiment.index, y=hourly_sentiment.values,
                      mode='lines+markers', name='Avg Sentiment',
                      line=dict(color='#00D26A', width=2)),
            row=2, col=1
        )
        
        fig.add_hline(y=0, line_dash="dash", line_color="gray", row=2, col=1)
        
        fig.update_xaxes(title_text="Time", row=2, col=1)
        fig.update_yaxes(title_text="Tweet Count", row=1, col=1)
        fig.update_yaxes(title_text="Sentiment Score", row=2, col=1)
        
        fig.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Top tweets
        st.subheader("🔥 Most Engaging Tweets")
        
        if 'retweet_count' in filtered_df.columns and 'favorite_count' in filtered_df.columns:
            filtered_df['engagement'] = filtered_df['retweet_count'] + filtered_df['favorite_count']
            top_tweets = filtered_df.nlargest(5, 'engagement')[['text', 'sentiment', 'sentiment_score', 'retweet_count', 'favorite_count', 'engagement']]
            
            for idx, row in top_tweets.iterrows():
                sentiment_emoji = '😊' if row['sentiment'] == 'Positive' else '😐' if row['sentiment'] == 'Neutral' else '😞'
                st.markdown(f"""
                <div class="metric-card">
                    <p><strong>{sentiment_emoji} {row['sentiment']}</strong> (Score: {row['sentiment_score']:.3f})</p>
                    <p>{row['text'][:200]}...</p>
                    <p><small>🔄 {int(row['retweet_count'])} retweets | ❤️ {int(row['favorite_count'])} favorites | 📊 {int(row['engagement'])} total engagement</small></p>
                </div>
                """, unsafe_allow_html=True)
        else:
            top_tweets = filtered_df.nlargest(5, 'sentiment_score')[['text', 'sentiment', 'sentiment_score']]
            for idx, row in top_tweets.iterrows():
                sentiment_emoji = '😊' if row['sentiment'] == 'Positive' else '😐' if row['sentiment'] == 'Neutral' else '😞'
                st.markdown(f"""
                <div class="metric-card">
                    <p><strong>{sentiment_emoji} {row['sentiment']}</strong> (Score: {row['sentiment_score']:.3f})</p>
                    <p>{row['text'][:200]}...</p>
                </div>
                """, unsafe_allow_html=True)
    
    else:
        # Overall dashboard
        st.markdown("## 📊 Overall Twitter Analytics")
        st.markdown(f"**Time Period:** {date_range_option}")
        
        # Filter by date range
        cutoff_date = pd.Timestamp.now(tz='UTC') - timedelta(days=selected_days)
        df = df[df['created_at'] >= cutoff_date]
        
        if df.empty:
            st.warning(f"No tweets found in the last {selected_days} days.")
            return
        
        # Add sentiment to all tweets
        df[['sentiment_score', 'sentiment']] = df['text'].apply(
            lambda x: pd.Series(analyze_sentiment(x))
        )
        
        # Overall metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📝 Total Tweets", len(df))
        
        with col2:
            avg_sentiment = df['sentiment_score'].mean()
            st.metric("😊 Avg Sentiment", f"{avg_sentiment:.3f}")
        
        with col3:
            positive_pct = (df['sentiment'] == 'Positive').sum() / len(df) * 100
            st.metric("✅ Positive %", f"{positive_pct:.1f}%")
        
        with col4:
            negative_pct = (df['sentiment'] == 'Negative').sum() / len(df) * 100
            st.metric("❌ Negative %", f"{negative_pct:.1f}%")
        
        # Overall insights
        st.markdown(f"""
        <div class="insight-box">
            <h3>💡 Overall Insights</h3>
            <ul>
                <li><strong>Total Tweets Analyzed:</strong> {len(df):,}</li>
                <li><strong>Time Period:</strong> {df['created_at'].min().strftime('%Y-%m-%d %H:%M')} to {df['created_at'].max().strftime('%Y-%m-%d %H:%M')}</li>
                <li><strong>Sentiment Breakdown:</strong> {(df['sentiment'] == 'Positive').sum()} Positive, {(df['sentiment'] == 'Neutral').sum()} Neutral, {(df['sentiment'] == 'Negative').sum()} Negative</li>
                <li><strong>Tip:</strong> Use the search bar on the left to analyze specific keywords or hashtags!</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Overall Sentiment Distribution")
            sentiment_fig = px.pie(
                df,
                names='sentiment',
                title='Overall Sentiment Breakdown',
                color='sentiment',
                color_discrete_map={'Positive': '#00D26A', 'Neutral': '#FFB800', 'Negative': '#FF4B4B'},
                hole=0.4
            )
            st.plotly_chart(sentiment_fig, use_container_width=True)
        
        with col2:
            st.subheader("📈 Sentiment Score Distribution")
            hist_fig = px.histogram(
                df,
                x='sentiment_score',
                nbins=30,
                title='Distribution of All Sentiment Scores',
                labels={'sentiment_score': 'Sentiment Score'},
                color_discrete_sequence=['#1DA1F2']
            )
            hist_fig.add_vline(x=0, line_dash="dash", line_color="gray")
            st.plotly_chart(hist_fig, use_container_width=True)
        
        # Time series
        st.subheader("📅 Tweet Activity Over Time")
        df_time = df.set_index('created_at')
        hourly_data = df_time.resample('H').agg({
            'text': 'count',
            'sentiment_score': 'mean'
        }).rename(columns={'text': 'tweet_count'})
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Tweet Volume', 'Average Sentiment'),
            vertical_spacing=0.15
        )
        
        fig.add_trace(
            go.Scatter(x=hourly_data.index, y=hourly_data['tweet_count'],
                      mode='lines+markers', name='Tweets',
                      line=dict(color='#1DA1F2', width=2)),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=hourly_data.index, y=hourly_data['sentiment_score'],
                      mode='lines+markers', name='Sentiment',
                      line=dict(color='#00D26A', width=2)),
            row=2, col=1
        )
        
        fig.add_hline(y=0, line_dash="dash", line_color="gray", row=2, col=1)
        fig.update_xaxes(title_text="Time", row=2, col=1)
        fig.update_yaxes(title_text="Count", row=1, col=1)
        fig.update_yaxes(title_text="Sentiment", row=2, col=1)
        fig.update_layout(height=600, showlegend=False)
        
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
