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
from itertools import chain


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

    df = pd.read_sql_query("SELECT content FROM news_articles WHERE id >=0",conn)
    

    # Tags to ignore
    ignore = ['ADV','PRON','CCONJ','PUNCT','PART','DET','ADP','SPACE', 'NUM', 'SYM']
    #Tokenize each article content 
    tokens = []
    for summary in tqdm(df['content'], total=len(df)):
       split_summary = ' '.join(wn.split(summary)) #split segmented words
       processed_summary = nlp(split_summary)
       proj_tok = [token.lemma_.lower() for token in processed_summary if token.pos_ not in ignore
                   and not token.is_stop
                   and token.is_alpha
                   and len(token.lemma_) > 2]
       tokens.append(proj_tok)

    print("Done tokenizing all articles\n")

    # Flatten the list of lists of tokens into a single list
    all_tokens = list(chain.from_iterable(tokens))
    
    # Count the frequency of each token
    token_freq = Counter(all_tokens)

    # Sort by frequency
    sorted_token_freq = sorted(token_freq.items(), key=lambda x: x[1], reverse=True)

    # Get the top 50 most common tokens
    top_tokens = sorted_token_freq[:50]

    # Convert the result to a pandas DataFrame
    df_top_tokens = pd.DataFrame(top_tokens, columns=['Token', 'Frequency'])

    # Plot the result
    plt.figure(figsize=(10,20))
    sns.barplot(y='Token', x='Frequency', data=df_top_tokens)
    plt.title('Top 50 Most Common Tokens')
    plt.show()





    

    
