# vader_sentiment_analysis.py
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import json

def analyze_sentiment(json_data):
    analyzer = SentimentIntensityAnalyzer()
    records = []

    for entry in json_data:
        author = entry.get("author", "")
        text = entry.get("text", "").strip()
        if not text:
            continue

        vs = analyzer.polarity_scores(text)
        compound = vs["compound"]
        if compound >= 0.05:
            sentiment = "positive"
        elif compound <= -0.05:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        records.append({
            "author": author,
            "text": text,
            "sentiment": sentiment,
            "score_negative": vs["neg"],
            "score_neutral": vs["neu"],
            "score_positive": vs["pos"],
            "score_compound": compound
        })

    return pd.DataFrame(records)

# 修改 Streamlit 中的 Tab5 调用 vader_sentiment_analysis
# 原代码应为：from sentiment_analysis import analyze_sentiment
# 修改为：from vader_sentiment_analysis import analyze_sentiment

# 示例代码：
# from vader_sentiment_analysis import analyze_sentiment
# df = analyze_sentiment(comment_data)
# st.dataframe(df)
