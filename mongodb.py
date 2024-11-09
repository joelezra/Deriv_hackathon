import pymongo
import os
import google.generativeai as genai
from dotenv import load_dotenv
import requests
from heatmap import RiskDashboard

load_dotenv()

# Set up MongoDB connection
client = pymongo.MongoClient(
    "mongodb+srv://admin:d2A5sO5NrM5c1AVQ@cluster0.koj4j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["hackathon"]
news_data = db["news_data"]

# Configure your API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to analyze sentiment
# def analyze_sentiment(article_text):
#     prompt = f"""Analyze the sentiment of the following text:\n\n{article_text}\n\n
#     The output should strictly only be in the format: Sentiment: [Positive/Negative/Neutral]"""
#     response = model.generate_content(prompt)
#     return response.text

    # Fetch technical indicators from the API
try:
    response_ema = requests.get('http://tayar.pro:8000/symbol/btc')
    if response_ema.status_code == 200:
        data_ema = response_ema.json()
        ema_25 = data_ema['crypto'][0]['1_hr_EMA_25']
        ema_75 = data_ema['crypto'][0]['1_hr_EMA_75'] 
        ema_150 = data_ema['crypto'][0]['1_hr_EMA_150']
        # print(ema_25, ema_75, ema_150)
        
except Exception as e:
    print(f"Error fetching technical indicators: {e}")

try:
    response_transactions = requests.get('http://tayar.pro:8000/transactions')
    if response_transactions.status_code == 200:
        data_transactions = response_transactions.json()
        transaction_type = data_transactions['transactions'][0]['transaction_type']
        # Calculate total units for BTC across all transactions
        total_btc_units = sum(
            data_transactions['transactions'][i]['units'] 
            for i in range(len(data_transactions['transactions'])) 
            if data_transactions['transactions'][i]['symbol'] == 'BTC'
        )
        print(f"Total BTC units: {total_btc_units}")
        # print(transaction_type)
        
except Exception as e:
    print(f"Error fetching technical indicators: {e}")

try:
    response_sentiment = requests.get('http://167.99.116.224:8000/news')
    if response_sentiment.status_code == 200:
        data_sentiment = response_sentiment.json()
        sentiment = int(data_sentiment['news'][0]['sentiment'])
        print(sentiment)
        print(type(sentiment))
        
except Exception as e:
    print(f"Error fetching technical indicators: {e}")

response_sentiment = requests.get('http://167.99.116.224:8000/news')
if response_sentiment.status_code == 200:
    data_sentiment = response_sentiment.json()
    sentiment = int(data_sentiment['news'][0]['sentiment'])
    print(sentiment)
    print(type(sentiment))


# Trading logic based on transaction type
if transaction_type == 'Buy':
    # Check if EMAs indicate upward trend
    if ema_25 > ema_75 and ema_75 > ema_150:
        ema = 0
    elif ema_25 < ema_75 and ema_75 < ema_150:
        ema = -1
    else:
        ema = 0

elif transaction_type == 'Sell':
    # Check if EMAs indicate downward trend
    if ema_25 > ema_75 and ema_75 > ema_150:
        ema = 1
    elif ema_25 < ema_75 and ema_75 < ema_150:
        ema = 0
    else:
        ema = 0

# if transaction_type == 'Buy' and int(sentiment) > 0:
#     sentiment = 0
# elif transaction_type == 'Buy' and int(sentiment) < 0:
#     sentiment = sentiment
# elif transaction_type == 'Sell' and int(sentiment) > 0:
#     sentiment = sentiment
# elif transaction_type == 'Sell' and int(sentiment) < 0:
#     sentiment = 0

# Calculate weighted score based on available components
# Current components: sentiment (0.2) and EMA (0.2)
# Future components: client profitability (0.3) and portfolio VAR (0.3)

# Initialize placeholder values for missing components
client_profitability = 0  # Placeholder for future implementation

# Create an instance of the RiskDashboard class
risk_dashboard = RiskDashboard()

# Call the calculate_var method
risk = risk_dashboard.calculate_var(confidence_level=0.95)
portfolio_var = risk * total_btc_units    # Value at Risk for BTC
print(portfolio_var)

# Define client profitability profiles
client_profiles = {
    'good': {  # High performing client
        'win_rate': 0.75,  # 75% profitable trades
        'avg_return': 0.25, # 25% average return
        'risk_adherence': 0.95, # Follows risk limits
        'profitability': 1.0  # Maximum score
    },
    'mid': {  # Average performing client
        'win_rate': 0.50,  # 50% profitable trades
        'avg_return': 0.10, # 10% average return
        'risk_adherence': 0.75, # Mostly follows risk limits
        'profitability': 0.5  # Medium score
    },
    'bad': {  # Poor performing client
        'win_rate': 0.25,  # 25% profitable trades
        'avg_return': -0.15, # -15% average return
        'risk_adherence': 0.30, # Often exceeds risk limits
        'profitability': 0.0  # Minimum score
    }
}

# Define a function to get client profitability based on profile
def get_client_profitability(profile):
    return client_profiles[profile]['profitability']

client_profitability = get_client_profitability('good')  # or 'mid', 'bad'

# Calculate weighted score with component breakdown
score_components = {
    'sentiment_score': sentiment * 0.2,
    'ema_score': ema * 0.2,
    'client_profitability_score': client_profitability * 0.3,
    'portfolio_var_score': portfolio_var * 0.3
}

weighted_score = sum(score_components.values())

# Create detailed context string for LLM
score_context = f"""
Weighted Market Analysis Score: {weighted_score}

Component Breakdown:
- Sentiment Analysis (20% weight): {score_components['sentiment_score']} (derived from news sentiment)
- Technical Analysis (20% weight): {score_components['ema_score']} (based on EMA crossovers)
- Client Profitability (30% weight): {score_components['client_profitability_score']} (placeholder for future implementation)
- Portfolio VAR (30% weight): {score_components['portfolio_var_score']} (placeholder for future implementation)

Note: A score closer to 1 indicates need for hedging, while a score closer to 0 indicates no action needed.
"""

print(f"Current weighted score (partial): {weighted_score}")
print("\nDetailed context for LLM:", score_context)



# Function to analyze sentiment
def analyze_sentiment(article_text):
    prompt = f"""Analyze the following news article about cryptocurrency to determine its sentiment on a continuous scale from -1 to 1. Here’s how the scale works:

    -1 represents a very bearish sentiment, indicating extremely negative or pessimistic views about the cryptocurrency’s performance or outlook.
    0 represents a neutral sentiment, reflecting a balanced view with no clear bullish or bearish leanings.
    1 represents a very bullish sentiment, indicating highly positive or optimistic views about the cryptocurrency’s performance or outlook.
    To arrive at a score, follow these steps:

    Identify and weigh positive or negative language in the article, especially around market performance, investor sentiment, regulatory updates, or recent technological developments.
    Consider whether the article emphasizes risks or challenges (bearish indicators) or focuses on growth, innovation, or favorable market conditions (bullish indicators).
    Evaluate the article’s overall tone and messaging:
    If the tone is heavily negative, lean toward a score closer to -1.
    If the sentiment appears balanced, assign a score near 0.
    If the article is largely positive, lean toward a score closer to 1.
    Use decimal points (e.g., -0.5, 0.6, 0.8) to express varying degrees of sentiment more precisely. Only provide a single number as output, reflecting the sentiment score.
    {article_text}
    """
    response = model.generate_content(prompt)
    return response.text


# Limit to first 10 rows
# for n in news_data.find({"sentiment": {"$exists": False}}).limit(175):
#     # print(n)
#     link = n["link"]
#     content = n["content"]
#     sentiment = analyze_sentiment(content)
#     clean_sentiment = sentiment.split(": ")[1].replace("**", "")
#     print(clean_sentiment)

# for n in news_data.find().limit(50):
#     link = n["link"]
#     content = n["content"]
#     sentiment = analyze_sentiment(content)
#     clean_sentiment = sentiment.split(" ")[0]
#     print(clean_sentiment)

#     """
#     Get the Sentiment Here
#     """

    # news_data.update_one({"link": link}, {"$set": {"sentiment": clean_sentiment}})

