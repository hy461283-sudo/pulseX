#!/bin/bash

# Script to push code to Xpluse repository
# Replace YOUR_USERNAME with your actual GitHub username

echo "🚀 Pushing to Xpluse repository..."

# Remove old origin if exists
git remote remove origin 2>/dev/null || true

# Add new remote (replace YOUR_USERNAME)
echo "📝 Please replace YOUR_USERNAME with your GitHub username in the command below:"
echo ""
echo "git remote add origin https://github.com/YOUR_USERNAME/Xpluse.git"
echo ""
read -p "Enter your GitHub username: " username

git remote add origin https://github.com/$username/Xpluse.git

# Create a new branch for our changes
git checkout -b main 2>/dev/null || git checkout main

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: Twitter Real-time Analysis Dashboard

Features:
- Twitter API v2 integration with Bearer Token
- Automatic tweet fetching (100 tweets per search)
- Real-time sentiment analysis using VADER
- Interactive dashboard with Streamlit
- Multiple visualizations (pie charts, histograms, time series)
- Date range filters (1, 3, 7, 14, 21, 28 days)
- Engagement metrics (retweets, favorites)
- Top engaging tweets display
- Sample data generator for testing

Tech Stack:
- Python 3.13
- Streamlit
- Tweepy (Twitter API v2)
- NLTK (VADER sentiment analysis)
- Plotly (interactive charts)
- Pandas & NumPy
"

# Push to GitHub
echo ""
echo "🔐 You may be prompted for GitHub credentials..."
git push -u origin main

echo ""
echo "✅ Done! Your code is now at: https://github.com/$username/Xpluse"
