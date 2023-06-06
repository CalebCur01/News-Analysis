import spacy
import sqlite3
import pandas as pd
from textblob import TextBlob
from matplotlib import pyplot as plt

if __name__ == '__main__':
    # Load model
    nlp = spacy.load("en_core_web_sm")

    # Load database
    filepath = 'D:/database/foxnewsDB.db'
    try:
        conn = sqlite3.connect(filepath)
        print("Database successfully opened")
    except Error as e:
        print(e)

    cursor = conn.cursor()

    df = pd.read_sql_query("SELECT content FROM news_articles", conn)

    # Perform sentiment analysis on the articles
    df['sentiment'] = df['content'].apply(lambda content: TextBlob(content).sentiment.polarity)

    #Histogram of sentiment values
    #df['sentiment'].hist()
    df.hist(column = 'sentiment')
    plt.show()

    # Save the dataframe with sentiment analysis
    #df.to_csv('sentiment_analysis.csv', index=False)
