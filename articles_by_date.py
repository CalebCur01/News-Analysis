import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import re
import numpy as np

# Connect to the database
conn = sqlite3.connect('D:/database/foxnewsDB.db')
cursor = conn.cursor()

# Read in for our dataframe
df = pd.read_sql_query("SELECT * FROM news_articles",conn)

# Set the desired author's name
desired_author = "FOX 5 Atlanta Digital Team"

# Filter the dataframe to include only entries by the desired author
author_df = df[df['author'] == desired_author]

# Use regex to extract only the date
def extract_date(date_string):
    match = re.search(r'\b\w+\s+\d{1,2},\s*\d{4}', date_string.strip())
    if match:
        return match.group()
    else:
        print(f"No match for: {date_string}")
        return date_string

author_df['publication_date'] = author_df['publication_date'].apply(extract_date)

# Convert the date column to datetime
author_df['publication_date'] = pd.to_datetime(author_df['publication_date'])

# Set the date column as the index
author_df.set_index('publication_date', inplace=True)

# Resample the data by day and count the number of articles on each day
daily_counts = author_df.resample('D').size()

# Filter out days by count
daily_counts = daily_counts[daily_counts >= 4]

# Plot the daily article counts
fig, ax = plt.subplots(figsize=(10, 6))

daily_counts.plot(ax=ax)

# Customize x-axis labels
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# Rotate and align the tick labels so they look better
fig.autofmt_xdate()

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Number of Articles')
plt.title(f'Daily Article Counts for {desired_author}')

# Show the plot
plt.tight_layout()
plt.show()
