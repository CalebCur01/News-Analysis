import spacy
import sqlite3
import pandas as pd
import wordninja as wn
import matplotlib.pyplot as plt
from spacy import displacy
from tqdm import tqdm
from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaMulticore
from gensim.models import CoherenceModel
import pyLDAvis.gensim_models
import seaborn as sns
from nltk.corpus import stopwords
from collections import Counter


if __name__ == '__main__':
    #load model
    nlp = spacy.load("en_core_web_sm")

    #load database
    filepath = 'D:/database/foxnewsDB.db'
    try:
        conn = sqlite3.connect(filepath)
        print("Database succesfully opened")
    except Error as e:
        print(e)
    cursor = conn.cursor()

    df = pd.read_sql_query("SELECT content FROM news_articles WHERE id >= 0",conn)

    # define a list of stop words, you may use nltk corpus for more
    nlp.Defaults.stop_words.add("s")  # add 's to spacy's stopword list
    stop_words = list(stopwords.words('english')) + list(nlp.Defaults.stop_words)
    
    # concatenate all the content and split to form a list of words
    all_content = ' '.join(df['content'])
    all_content = ' '.join(wn.split(all_content))
    all_words = all_content.split()

    # define a list of words to be excluded
    exclude_words = ["fox","atlanta","'"," "]

    # remove stop words
    non_stop_words = [word for word in all_words 
                  if not word.isnumeric()  # exclude numbers
                  and word.lower() not in stop_words
                  and word.lower() not in exclude_words
                  and len(word) > 2]  # additional exclusion words

    # get the frequency of each word
    word_freq = Counter(non_stop_words)

    # sort by frequency
    sorted_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

    # get the top 50 most common words
    top_words = sorted_freq[:50]

    # convert the result to a pandas DataFrame
    df_top_words = pd.DataFrame(top_words, columns=['Word', 'Frequency'])

    # plot the result
    plt.figure(figsize=(20,10))
    sns.barplot(y='Word', x='Frequency', data=df_top_words)
    plt.title('Top 50 Most Common Non-stop Words')
    plt.show()
