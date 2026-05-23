import requests
from textblob import TextBlob
import pandas as pd
import streamlit as st

st.title("Reddit Sentiment Analyzer")


#headers = {"User-Agent": "sentiment-analyzer/0.1"}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",}

subreddit = st.text_input("Enter subreddit name")
button = st.button("Analyze")
url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=25&raw_json=1"
if subreddit and button:
    response = requests.get(url, headers=headers, timeout=10)
    st.write(response.status_code)
    try:                       
        posts = response.json()["data"]["children"]
        results = []
        tweets = []

        for post in posts:
            tweet = post["data"]["title"]
            tweets.append(tweet)
            check_sentiment = TextBlob(tweet).sentiment.polarity
            if check_sentiment > 0:
                results.append({"Tweet": tweet, "Sentiments": "Positive"})
            elif check_sentiment < 0:
                results.append({"Tweet": tweet, "Sentiments": "Negative"})
            else:
                results.append({"Tweet": tweet, "Sentiments": "No Sentiments"})

        #print(response.json())
        pd.set_option("display.max_colwidth", None)
        df = pd.DataFrame(results)

        #print(df)
        st.dataframe(df)
        #print(df["Sentiments"].value_counts())
        st.bar_chart(df["Sentiments"].value_counts())
    except Exception as e:
        st.error(f"Something went wrong :{e}")
else:
    st.info("Enter a subreddit name above to get started!")