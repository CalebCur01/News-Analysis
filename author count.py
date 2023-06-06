import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import re

# Connect to the database
conn = sqlite3.connect('D:/database/foxnewsDB.db')
cursor = conn.cursor()

#read in for our dataframe
df = pd.read_sql_query("SELECT * FROM news_articles",conn)

#strip whitespace
df['author'] = df['author'].apply(lambda x: ' '.join(x.split()).strip())

"""df['author'].value_counts().plot(kind='bar')
plt.show()"""

# Calculate author counts
author_counts = df['author'].value_counts()

# Set the threshold (minimum count)
n = 14

# Filter out authors with count less than the threshold
filtered_author_counts = author_counts[author_counts >= n]

# Sort the author counts
sorted_author_counts = filtered_author_counts.sort_values()

# Plot the filtered author counts as a bar chart
plt.figure(figsize=(5, 10))  # Adjust the figure size as needed
ax = sorted_author_counts.plot(kind='bar')

# Add labels and title
plt.xlabel('Author')
plt.ylabel('Count')
plt.title('Author Count')

# Rotate x-axis labels (45 degrees)
"""plt.xticks(rotation=45)"""

# Display the count values on top of the bars
for i, count in enumerate(sorted_author_counts):
    ax.text(i, count, str(count), ha='center', va='bottom')

# Show the plot
plt.tight_layout()
plt.show()
