# News-Analysis

# Graphs and charts
The most common words and most common tokens:
![Most common tokens](https://github.com/CalebCur01/News-Analysis/assets/25915691/5c7bf5e5-482a-446e-b23a-fd5ea7ea945f)
![Most common words](https://github.com/CalebCur01/News-Analysis/assets/25915691/226ef813-3b6d-4d3d-9ab4-d8907766bf3e)

Number of articles published by author:
![Article Count](https://github.com/CalebCur01/News-Analysis/assets/25915691/9cf16e34-e9c6-42fb-9159-0a142de18d22)

Number of articles published by author each day:

Bar:
![Article_by_date-Bar](https://github.com/CalebCur01/News-Analysis/assets/25915691/d11f15b1-637d-44b3-a4e3-335ac9dc29c1)
Line:
![Article_by_date-Line](https://github.com/CalebCur01/News-Analysis/assets/25915691/a7c091bf-976d-4e8e-a009-15d75e8cd182)

Sentiment:
Values range from [-1,1]. Numbers less than 0 indicate negative sentiment, while numbers greater than 0 indicate positive. Based on this, it seems most articles are close to neutral, between 0 and 0.1

![Sentiment_Histogram](https://github.com/CalebCur01/News-Analysis/assets/25915691/3c490739-8baa-47ee-a9d9-e406c41a7545)




# Topic-Modelling
Coherence Scores:
We train LDA model using different number of topics and calculate the umass and c_v coherence scores to determine how many topics we should use. Based on these, we decided on 7 topics.
![Coherence_Score-umass](https://github.com/CalebCur01/News-Analysis/assets/25915691/1875e0a9-e548-4664-ac8f-4d6e7439c139)
![Coherence_Score-C_v](https://github.com/CalebCur01/News-Analysis/assets/25915691/8095e864-5675-48b4-97e5-6a69f03e8681)

To view the result, see: https://calebcur01.github.io/

Looking at the output, topic 1 and topic 7 seem to have substantial overlap. For topic 1, some of the most relevant terms are "police", "county", and "officer". For topic 7, we have "jury", "juror", and "prosectuor". We will say Topic 1 is Crime, and Topic 7 is Criminal Justice. Looking at the most relevant terms for the other topics, we can roughly catagorize them as follows: 

Topic 2: Entertainment

Topic 3: Politics

Topic 4: Personal Finance

Topic 5: Health/Medicine

Topic 6: Economy

