import tweepy
import json
import time

# Use bearer token for Twitter API v2
bearer_token = "AAAAAAAAAAAAAAAAAAAAABmY5QEAAAAAsr24Rt8v26u4YhJyvSt7daFVSp8%3D9JbsQab2fbXA7zQvpWTysYRMMmnb5hjwxD6JtrPWc9tlJkd4Af"

class TweetStreamListener(tweepy.StreamingClient):
    def __init__(self, bearer_token, output_file='tweets.json'):
        super().__init__(bearer_token)
        self.output_file = output_file
        self.counter = 0
        self.output = open(self.output_file, 'w')
    
    def on_tweet(self, tweet):
        tweet_data = {
            'id': tweet.id,
            'text': tweet.text,
            'created_at': str(tweet.created_at) if hasattr(tweet, 'created_at') else None,
            'author_id': tweet.author_id
        }
        self.output.write(json.dumps(tweet_data) + '\n')
        self.counter += 1
        
        if self.counter % 50 == 0:
            print(f"No of tweets currently in tweets.json = {self.counter}")
        
        if self.counter >= 20000:
            self.output.close()
            self.output = open(self.output_file, 'w')
            self.counter = 0
    
    def on_error(self, status):
        print(f'Error: {status}')
        return False

# Create streaming client
stream = TweetStreamListener(bearer_token)

# Add rules for filtering tweets
keywords = ['google', 'apple']
for keyword in keywords:
    try:
        stream.add_rules(tweepy.StreamRule(keyword))
    except Exception as e:
        print(f"Rule might already exist: {e}")

print("Starting stream for keywords:", keywords)
stream.filter()
