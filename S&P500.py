#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import necessary libraries
import pandas as pd
import yfinance as yf
import streamlit as st
from pandas.tseries.offsets import DateOffset


# In[2]:


# Fetch the list of S&P 500 tickers from Wikipedia
tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0].Symbol


# In[4]:


tickers = tickers.to_list()


# @st.cache_data: This decorator is used to cache the return value of the decorated function getData() in this case, based on its inputs. It allows the function to store its output and retrieve it from the cache instead of recomputing the result every time it is called with the same inputs.
# 
# By using @st.cache_data, Streamlit will automatically handle the caching and retrieval of the function's output. When the function is called with the same inputs again, Streamlit will return the cached result instead of executing the function code.

# In[6]:


@st.cache_data

def getData():
    df = yf.download(tickers, start='2020-01-01')
    df = df['Close']
    return df


# In[7]:


df = getData()


# ## Design the dashboard
# 

# In[8]:


st.title('Index Component Perfomance of the S&P 500')


# In[9]:


# Getting user input
n = st.number_input("Please provide the perfomance horizon in months:", min_value=1,
                    max_value=24)   


# In[11]:


def get_return(df, n):
    previous_prices = df[:df.index[-1] - DateOffset(months=n)].tail(1).squeeze()
    recent_prices = df.loc[df.index[-1]]
    ret_df = recent_prices/previous_prices - 1
    return previous_prices.name, ret_df


# In[12]:


date, ret_df = get_return(df, n)


# In[13]:


winners, losers = ret_df.nlargest(10), ret_df.nsmallest(10)


# In[16]:


winners.name, losers.name = 'winners', 'losers'


# In[17]:


st.table(winners)
st.table(losers)


# In[19]:


# Creating a select box widget to pick a winner and loser to visualize
winnerpick = st.selectbox('Pick a winner to visualize:', winners.index)
st.line_chart(df[winnerpick][date:])

loserpick = st.selectbox('Pick a loser to visualize:', losers.index)
st.line_chart(df[loserpick][date:])


# In[ ]:




