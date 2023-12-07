#!/usr/bin/env python
# coding: utf-8

# In[17]:


pip install requests beautifulsoup4 requests-html


# In[18]:


#we need to import the necessary libraries
import pandas as pd
from urllib.parse import urlparse
import numpy as np
import nltk.data
from requests_html import HTMLSession


# In[19]:


def parse_elements(url,element):
    session = HTMLSession()
    r = session.get(url)
    elements = r.html.find(element)
    return elements


# In[48]:


#we need to define key words for topic analysis from the website
def topic_detection(sentence):
    Realestate_words = ('mortgage rate', 'listings', 'home price', 'home ssles', 'property', 'bathrooms', 'interest rates', 'borrowing costs', 'neighbourhood', 'rent', 'selling')
    Finance_words = ('loan', 'stocks', 'bonds', 'credit score', 'forex', 'commodities','dividends','investment','debt', 'savings','budgeting')
    Ecommerce_words = ('shopify', 'amazon','etsy','products','customers','marketing','demand','orders')
    Real_Estate = any(sentence.count(i) > 0 for i in Realestate_words)
    Finance = any(sentence.count(i) > 0 for i in Finance_words)
    Ecommerce = any(sentence.count(i) > 0 for i in Ecommerce_words)
    topics = []
    if Real_Estate == True:
        topics.append("Real Estate")
    if Finance == True:
        topics.append("Finance")
    if Ecommerce == True:
        topics.append("Ecommerce")
    return topics


# In[49]:


url = 'https://globalnews.ca/news/10003716/toronto-home-sales-september-2023/'
paragraphs = parse_elements(url, 'p')
links = parse_elements(url, 'a')


# In[50]:


type(paragraphs[0])


# In[67]:


#some paragraphs from the website
for p in paragraphs:
  print(p.text)


# In[55]:


def sentiment_detection(sentence):
    positive_words = ('happy', 'sunny', 'positive', 'triumphant', 'optimistic', 'wonderful', 'significant', 'achieve','capabilities','progress','prized')
    negative_words = ('sad', 'terrible', 'frightening', 'rainy', 'scary', 'shocked', 'critical','bottlenecked')

    positive = any(sentence.count(i) > 0 for i in positive_words)
    negative = any(sentence.count(i) > 0 for i in negative_words)

    if positive == negative == False:
        return "neutral"
    elif positive != negative:
        return "positive" if positive else "negative"
    else:
        return "mixed"


# In[68]:


#dictionary that has two lists, one for the paragraphs, and one for topics covered by those paragraphs
print(paragraphs)
p_dictionary = {}
p_list = []
topic_list = []
for p in range(0, len(paragraphs)):
    if len(paragraphs[p].text) > 50:
      #print((paragraphs[p].text))
      #print(f"TALKS ABOUT: {topic_detection(paragraphs[p].text)}")
      p_list.append(paragraphs[p].text)
      topic_list.append(topic_detection(paragraphs[p].text))
p_dictionary['Paragraphs'] = p_list
p_dictionary['Topics'] = topic_list


# In[52]:


p_dictionary['Topics']


# In[53]:


#we need to input the dictionary into a dataframe to classify the topics
medium_df = pd.DataFrame(p_dictionary)


# In[54]:


medium_df.head(9)


# In[58]:


medium_df2 = pd.DataFrame({'Paragraph_Elements':paragraphs})


# In[59]:


medium_df2['Paragraph_Text'] = medium_df2['Paragraph_Elements'].apply(lambda x:x.text)


# In[60]:


medium_df2['Topics'] = medium_df2['Paragraph_Text'].apply(topic_detection)


# In[61]:


medium_df2['Character Count'] = medium_df2['Paragraph_Text'].apply(lambda x: len(x))


# In[62]:


medium_df2.head()


# In[63]:


medium_df2 = medium_df2[medium_df2['Character Count'] >= 50]


# In[64]:


medium_df2


# In[ ]:




