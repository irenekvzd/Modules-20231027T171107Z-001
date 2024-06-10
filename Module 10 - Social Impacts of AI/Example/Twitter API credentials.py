import pandas as pd
import numpy as np
import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Twitter API credentials (you need to fill these in with your credentials)
consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_secret'
access_token = 'your_access_token'
access_secret = 'your_access_secret'

# Set up the Twitter API connection
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Function to fetch tweets
def fetch_tweets(query, count=100):
    tweets = []
    for tweet in tweepy.Cursor(api.search_tweets, q=query, lang='en').items(count):
        tweets.append(tweet.text)
    return tweets

# Fetch tweets about the social impacts of AI
query = "social impacts of AI"
tweets = fetch_tweets(query, count=500)

# Create a DataFrame from the tweets
df = pd.DataFrame(tweets, columns=['Tweet'])

# Function to clean tweets
def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

# Clean the tweets
df['Cleaned_Tweet'] = df['Tweet'].apply(clean_tweet)

# Function to analyze sentiment
def analyze_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

# Analyze the sentiment of the cleaned tweets
df['Sentiment'] = df['Cleaned_Tweet'].apply(analyze_sentiment)

# Display the first few rows of the DataFrame
print(df.head())

# Sentiment analysis summary
sentiment_counts = df['Sentiment'].value_counts()
print(sentiment_counts)

# Plotting the sentiment distribution
plt.figure(figsize=(10, 6))
sentiment_counts.plot(kind='bar', color=['green', 'blue', 'red'])
plt.title('Sentiment Analysis of Tweets about Social Impacts of AI')
plt.xlabel('Sentiment')
plt.ylabel('Number of Tweets')
plt.show()

# Generate a word cloud
all_words = ' '.join([text for text in df['Cleaned_Tweet']])
wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(all_words)

plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()

# Additional analysis: common words in positive vs. negative tweets
positive_tweets = df[df['Sentiment'] == 'Positive']['Cleaned_Tweet']
negative_ttweets = df[df['Sentiment'] == 'Negative']['Cleaned_Tweet']

positive_words = ' '.join([text for text in positive_tweets])
negative_words = ' '.join([text for text in negative_tweets])

positive_wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110, collocations=False).generate(positive_words)
negative_wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110, collocations=False).generate(negative_words)

plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.imshow(positive_wordcloud, interpolation="bilinear")
plt.title('Positive Words')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(negative_wordcloud, interpolation="bilinear")
plt.title('Negative Words')
plt.axis('off')

plt.show()
