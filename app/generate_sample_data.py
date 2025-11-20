import json
import random
from datetime import datetime, timedelta

# Generate sample tweet data
tweets = []
keywords = ['#google', '#apple']
sentiments = ['positive', 'negative', 'neutral']

# Generate data for the last 30 days
base_time = datetime.now() - timedelta(days=30)

for i in range(1000):
    keyword = random.choice(keywords)
    sentiment_words = {
        'positive': ['great', 'awesome', 'love', 'excellent', 'amazing', 'fantastic', 'wonderful', 'brilliant'],
        'negative': ['bad', 'terrible', 'hate', 'awful', 'disappointing', 'poor', 'worst', 'horrible'],
        'neutral': ['okay', 'fine', 'normal', 'average', 'standard', 'decent', 'acceptable']
    }
    
    sentiment = random.choice(sentiments)
    word = random.choice(sentiment_words[sentiment])
    
    tweet_text = f'This is a sample tweet about {keyword}. It is {word}! {keyword}'
    
    # Distribute tweets across 30 days with random intervals
    random_minutes = random.randint(0, 30 * 24 * 60)  # Random time within 30 days
    tweet_time = base_time + timedelta(minutes=random_minutes)
    
    tweet = {
        'id': 1000000000000000000 + i,
        'created_at': tweet_time.strftime('%a %b %d %H:%M:%S +0000 %Y'),
        'text': tweet_text,
        'user': {
            'id': random.randint(100000, 999999),
            'screen_name': f'user{random.randint(1, 100)}',
            'name': f'Test User {random.randint(1, 100)}'
        },
        'retweet_count': random.randint(0, 100),
        'favorite_count': random.randint(0, 200),
        'lang': 'en'
    }
    
    # Add optional fields that the code checks for
    if random.random() > 0.7:  # 30% chance of extended tweet
        tweet['extended_tweet'] = {
            'full_text': tweet_text + ' This is extended content for longer tweets.'
        }
    
    if random.random() > 0.8:  # 20% chance of retweet
        tweet['retweeted_status'] = {
            'text': f'RT: {tweet_text}',
            'user': {
                'screen_name': f'rtuser{random.randint(1, 50)}'
            }
        }
    
    if random.random() > 0.9:  # 10% chance of quoted status
        tweet['quoted_status'] = {
            'text': f'Quoted: {tweet_text}'
        }
    
    tweets.append(tweet)

# Write to tweets.json
with open('tweets.json', 'w') as f:
    for tweet in tweets:
        f.write(json.dumps(tweet) + '\n')

print(f"Generated {len(tweets)} sample tweets in tweets.json")
