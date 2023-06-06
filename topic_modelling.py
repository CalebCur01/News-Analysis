import spacy
import sqlite3
import pandas as pd
from spacy import displacy
from tqdm import tqdm
from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaMulticore
from gensim.models import CoherenceModel
import pyLDAvis.gensim_models
from matplotlib import pyplot as plt
import warnings

warnings.filterwarnings("ignore")


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

    df = pd.read_sql_query("SELECT content FROM news_articles",conn)

    # Tags to ignore
    ignore = ['ADV','CCONJ','NUM','PRON','SPACE','PUNCT']
    #Tokenize each article content 
    tokens = []
    for article in tqdm(nlp.pipe(df['content']),total=len(df)):
       tok = [token.lemma_.lower() for token in article if token.pos_ not in ignore and not token.is_stop and token.is_alpha]
       tokens.append(tok)

    print("Done tokenizing all articles\n")

    #Add tokens in new column of dataframe
    df['tokens'] = tokens

    #create dictionary
    dictionary = Dictionary(df['tokens'])

    #filter common and rare tokens out
    dictionary.filter_extremes(no_below=15, no_above=0.5)

    #Get our bag of words/sparse vectors for each token
    corpus = [dictionary.doc2bow(doc) for doc in df['tokens']]

    #We set the number of topics and train LDA model
    lda_model = LdaMulticore(corpus=corpus, id2word=dictionary, iterations=100, num_topics=7, workers = 4, passes=100)


    # Visualize topics
    lda_display = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)
    pyLDAvis.display(lda_display)

    # Save the report
    pyLDAvis.save_html(lda_display, 'topics.html')
    
    
    """
    #Train our model with different number of topics and calculate coherence score using c_v and umass
    topics = []
    score = []
        
        for i in tqdm(range(1,20,1),total = 20): #calculate c_v coherence
        lda_model = LdaMulticore(corpus=corpus, id2word=dictionary, iterations=10, num_topics=i, workers = 4, passes=10, random_state=100)
        cm = CoherenceModel(model=lda_model, texts = df['tokens'], corpus=corpus, dictionary=dictionary, coherence='c_v')
        topics.append(i)
        score.append(cm.get_coherence())
    _=plt.plot(topics, score)
    _=plt.xlabel('Number of Topics')
    _=plt.ylabel('Coherence Score')
    plt.savefig("c_V.png")

       for i in tqdm(range(1,20,1),total = 20): #calculate umass coherence 
           print(f"training model {i}...")
           lda_model = LdaMulticore(corpus=corpus, id2word=dictionary, iterations=10, num_topics=i, workers = 4, passes=10, random_state=100)
           cm = CoherenceModel(model=lda_model, corpus=corpus, dictionary=dictionary, coherence='u_mass')
           topics.append(i)
           score.append(cm.get_coherence())
    _=plt.plot(topics, score)
    _=plt.xlabel('Number of Topics')
    _=plt.ylabel('Coherence Score')
    plt.savefig(umass.png)"""

