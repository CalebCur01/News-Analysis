import spacy
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from spacy import displacy
from collections import Counter


def plot_top_entities(counter, entity_type, n, filter_out = []):
    #Filter the counter to only include entities of the specified type
    filtered_counter = {k: v for k, v in counter.items() if k[1] == entity_type and k[0] not in filter_out}

    #Check if filtered_counter is empty
    if not filtered_counter:
        print(f"No entities of type {entity_type} found.")
        return

    #Get the n most common entities of the specified type
    most_common = dict(Counter(filtered_counter).most_common(n))

    #Extract labels and values
    labels, values = zip(*[(k[0], v) for k, v in most_common.items()])
    

    #Create barplot
    plt.figure(figsize=(10, 5))
    sns.barplot(x=list(values), y=list(labels))
    plt.title(f'Top {n} most common entities of type {entity_type}')
    plt.xlabel('Count')
    plt.ylabel(entity_type)
    plt.show()

def plot_entities(counter):
    #Extract types and counts
    types = [entity_type for entity, entity_type in counter.keys()]
    type_counts = Counter(types)

    #unpack and get then zip labels and counts
    labels, values = zip(*type_counts.items())

    #Create barplot
    plt.figure(figsize=(10, 5))
    sns.barplot(x=list(values), y=list(labels))
    plt.title('Counts of each type of entity')
    plt.xlabel('Count')
    plt.ylabel('Entity Type')
    plt.show()

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

#Create data frame
df = pd.read_sql_query("SELECT * FROM news_articles WHERE id < 5",conn)

# Extract entities and labels
df['entities'] = df['content'].apply(lambda content: [(ent.text, ent.label_) for ent in nlp(content.title()).ents])


#Flatten list of lists and count occurrences
counter = Counter([x for sublist in df['entities'].tolist() for x in sublist])


