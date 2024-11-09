import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()

# Configure your API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to analyze sentiment
def analyze_sentiment(article_text):
    prompt = f"Analyze the sentiment of the following text:\n\n{article_text}\n\nThe output should be in the format: Sentiment: [Positive/Negative/Neutral]"
    response = model.generate_content(prompt)
    return response.text

# Read the news articles from JSON file
with open('news_bitcoin2.json', 'r', encoding='utf-8') as file:
    news_articles = json.load(file)

# Iterate through the dictionary and access each article's content
for article in news_articles["news"]:
    article_id = article["_id"]
    article_content = article["content"]
    print(f"ID: {article_id}")
    print(f"Content: {article_content}\n")

# Iterate through the dictionary and analyze sentiment for each article
for article in news_articles["news"]:
    article_id = article["_id"]
    article_content = article["content"]
    sentiment = analyze_sentiment(article_content)
    print(f"{article_id}: {sentiment}")
