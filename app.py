# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 09:18:30 2021

@author: DELL
"""
import advertools as adv
import regex 
import pandas as pd
import numpy as np
import emoji
import collections
from collections import Counter
#from os import path
import PIL
from PIL import Image
import wordcloud
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
#import os 
import plotly
import matplotlib
import plotly.express as px
import matplotlib.pyplot as plt

import streamlit as st
import regex as re
import seaborn as sns
print(PIL.__version__)
st.markdown('<style>body{background-color: White}</style>',unsafe_allow_html=True)
#st.markdown(f'<p style="background-color:#0066cc;color:#33ff33;font-size:24px;border-radius:2%;"></p>', unsafe_allow_html=True)

def startsWithDateAndTime(s):
    pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -'
    result=re.match(pattern, s)
    if result:
        return True
    else:
        return False

def findauthor(s):
    s=s.split(":")
    if(len(s)==2):
        return True
    else:
        return False
def getdatapoint(line):
    splitline=line.split(' - ')
    dateTime=splitline[0]
    date,time=dateTime.split(', ')
    message=' '.join(splitline[1:])
    if findauthor(message):
        splitmessage=message.split(': ')
        author=splitmessage[0]
        message=' '.join(splitmessage[1:])
    else:
        author=None
    return date, time, author, message


data=[]
    
#streamlit hello
st.title('Whatsapp Group Chat Analysis')
original_title = '<p style="font-family:Courier; color:yellow; font-size:15px;"> Analysis on Exported chats to understand texting patterns of users.</p>'
st.markdown(original_title, unsafe_allow_html=True)   
  
    
    
#st.markdown('Analysis on Exported chats to understand texting patterns of users.')
st.set_option('deprecation.showfileUploaderEncoding', False)

st.sidebar.title("Analyze:")
st.sidebar.markdown("This app is use to analyze your WhatsApp Group Chats")

st.sidebar.markdown('[![Priyanshi Agarwal]\
                    (https://img.shields.io/badge/Author-@priyanshiAgarwal-gray.svg?colorA=gray&colorB=dodgerblue)]\
                    (https://www.linkedin.com/in/priyanshi-agarwal-515245176/)')

st.sidebar.markdown('**How to export chat text file? (Not Available on Whatsapp Web)**')
st.sidebar.text('Follow the steps 👇:')
st.sidebar.text('1) Open the individual or group chat.')
st.sidebar.text('2) Tap options > More > Export chat.')
st.sidebar.text('3) Choose export without media.')
st.sidebar.markdown('*You are all set to go 😃*.')
st.sidebar.subheader('**FAQs**')
st.sidebar.markdown('**What happens to my data?**')
st.sidebar.markdown('The data you upload is not saved anywhere on this site or any 3rd party site i.e, not in any storage like DB/FileSystem/Logs.')
uploaded_files = st.file_uploader("Upload Your Whatsapp Chat.(.txt file only!)",type="txt")

if uploaded_files:
 messagebuffer=[]
 parsedData=[]
 date,time,author=None,None,None
 for l in uploaded_files:
#    fp.readline()
       # st.write(l)
     
        line=l.decode("utf-8") 
        
        line=line.strip()
        if startsWithDateAndTime(line):
            if len(messagebuffer) >0:
                parsedData.append([date,time,author,' '.join(messagebuffer)])
            messagebuffer.clear()
            date,time,author,message=getdatapoint(line)
            messagebuffer.append(message)
        else:
            messagebuffer.append(line)
#print(parsedData)
 df=pd.DataFrame(parsedData,columns=['date','time','author','message'])
 df['date']=pd.to_datetime(df["date"])
 df=df.dropna()

 total_message=df.shape[0]
#print(total_message)
 media_messages=df[df['message']=='<Media omitted>'].shape[0]
 def split_count(text):
    li=[text]
    
    n = []
    emoji_list=adv.extract_emoji(li)
    
    n=emoji_list['emoji'][0]
         

    return n
 authorlist = list(df.author.unique())
 authorlist.insert(0,'All')
 st.subheader("**Who's Stats do you want to see?**")
 option = st.selectbox("", authorlist)    

 df["emoji"] = df["message"].apply(split_count)
 emojis=sum(df['emoji'].str.len())
 total_messages=df.shape[0]
 #st.write(option)
 
 URLPATTERN=r'(https?://\S+)'
 df['urlcount']=df.message.apply(lambda x:re.findall(URLPATTERN, x)).str.len()
 links=np.sum(df.urlcount)
 original_title = '<p style="font-family:Courier; color:Red; font-size: 40px;">DATA                           SCIENCE                             COMMUNITY</p>'
 st.markdown(original_title, unsafe_allow_html=True)
 if(option=='All'):
  original_title = '<p style="font-family:Courier; color:White; font-size: 18px;">Group Data</p>'
  st.markdown(original_title, unsafe_allow_html=True)
 #st.header('Data science  community') 
  st.write('messages',total_messages)
  st.write("media:",media_messages)
  st.write("emojis:",emojis)
  st.write("links:",links)
 media_messages_df=df[df['message']=='<Media omitted>']
 message_df=df.drop(media_messages_df.index)
#print(message_df.info())
#print(df.info())
 message_df['letter count']=df.message.apply(lambda s: len(s))
 message_df['word count']=df.message.apply(lambda s: len(s.split(" ")))
 message_df['messagecount']=1
#print(message_df.head())
 l=df.author.unique()
 if(option=='All'):
   for i in range (len(l)):
   
     req_df=message_df[message_df["author"]==l[i]]
   # original_title = '<p style="font-family:Courier; color:White; font-size: 18px;">f"stats of {l[i]} -"</p>'
    #st.markdown(original_title, unsafe_allow_html=True)
     st.write(f'stats of {l[i]} -')
     st.write("messages sent:",req_df.shape[0])
     wor=(np.sum(req_df['word count']))/req_df.shape[0]
     st.write("words per message",wor)
     media=media_messages_df[media_messages_df['author']==l[i]].shape[0]
     st.write("media messages:",media)
     e=sum(req_df['emoji'].str.len())
     st.write("emojis sent",e)
     li=sum(req_df["urlcount"])
     st.write("links:",li)
  
 elif(option!='All'):
    req_df=message_df[message_df["author"]==option]
   # original_title = '<p style="font-family:Courier; color:White; font-size: 18px;">f"stats of {l[i]} -"</p>'
    #st.markdown(original_title, unsafe_allow_html=True)
    st.write(f'stats of {option} -')
    st.write("messages sent:",req_df.shape[0])
    wor=(np.sum(req_df['word count']))/req_df.shape[0]
    st.write("words per message",wor)
    media=media_messages_df[media_messages_df['author']==option].shape[0]
    st.write("media messages:",media)
    e=sum(req_df['emoji'].str.len())
    st.write("emojis sent",e)
    li=sum(req_df["urlcount"])
    st.write("links:",li)
     
      
 stopwords=set(STOPWORDS)    
 def visualize_emoji(data):
	 total_emojis_list = list([a for b in message_df.emoji for a in b])
	 emoji_dict = dict(Counter(total_emojis_list))
	 emoji_dict = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)
	 emoji_df = pd.DataFrame(emoji_dict, columns=['emoji', 'count'])
	 fig = px.pie(emoji_df, values='count', names='emoji')
	 fig.update_traces(textposition='inside', textinfo='percent+label')
	 fig.update_layout(
    	margin=dict(
        	l=5,
        	r=5,
    	)
    )
	 fig.update(layout_showlegend=False)
	 return fig
 if(option!='All'):
     original_title = '<p style="font-family:Courier; color:Pink; font-size: 30px;"> Emoji Distribution Of This Person 😂</p>'
     st.markdown(original_title, unsafe_allow_html=True)
 dummy=message_df[message_df['author']==option]    
 if(option!='All'):
      
	 total_emojis_list = list([a for b in dummy.emoji for a in b ])
	 emoji_dict = dict(Counter(total_emojis_list))
	 emoji_dict = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)
	 emoji_df = pd.DataFrame(emoji_dict, columns=['emoji', 'count'])
	 fig = px.pie(emoji_df, values='count', names='emoji')
	 fig.update_traces(textposition='inside', textinfo='percent+label')
	 fig.update_layout(
    	margin=dict(
        	l=5,
        	r=5,
    	)
   )
	 fig.update(layout_showlegend=False)
	 st.plotly_chart(fig)
	   
 if(option=='All'):
  original_title = '<p style="font-family:Courier; color:Pink; font-size: 30px;"> Emoji Distribution 😂</p>'
  st.markdown(original_title, unsafe_allow_html=True)
 #st.subheader(" emoji distribution 😂")
  st.text("Hover on Chart to see details.")
  st.plotly_chart(visualize_emoji(data),use_container_width=True)
  l=list(l)
  original_title = '<p style="font-family:Courier; color:Pink; font-size: 30px;"> GROUP WORDCLOUD </p>'
  st.markdown(original_title, unsafe_allow_html=True)
# st.header("GROUP WORDCLOUD")
  text=" ".join(r for r in message_df.message) 
  wordcloud=WordCloud(stopwords=stopwords,background_color="white").generate(text)
  fig=plt.figure(figsize=(10,5))
  plt.imshow(wordcloud,interpolation="bilinear")
  fig=plt.axis("off")
  plt.show()
  st.set_option('deprecation.showPyplotGlobalUse', False)
  st.pyplot()
 if(option=='All'): 
  original_title = '<p style="font-family:Courier; color:Pink; font-size: 30px;"> PERSON WISE STATS</p>'
  st.markdown(original_title, unsafe_allow_html=True)
 #st.header("PERSON WISE STATS")
  for i in range(len(l)):
    st.write(l[i])  
    dummy_df=message_df[message_df["author"]==l[i]]
    text=" ".join(r for r in dummy_df.message)
    stopwords=set(STOPWORDS)
    stopwords=["kya","toh","toh","ki","hai","se","koi","haan","hi","me","h","ky","nahi","yr","m","ye","he","are","to","abhi","ka","tho","or","na","haa","han","fir"]

    wordcloud=WordCloud(stopwords=stopwords,background_color="white").generate(text)
    print(l[i])
    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud,interpolation="bilinear")
    plt.axis("off")
    plt.show()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
  plt.figure(figsize=(9,6))
  mostly_active = message_df['author'].value_counts()
 #st.write(mostly_active)
### Top 10 peoples that are mostly active in our Group is : 
  m_a = mostly_active.head(10)
  h=m_a.index
 #st.write(h)
  original_title = '<p style="font-family:Courier; color:Pink; font-size: 30px;"> Mostly Active Members in the group</p>'
  st.markdown(original_title, unsafe_allow_html=True)
  x_pos = np.arange(len(h))
 #st.write(x_pos)
  m_a.plot.bar()
  plt.xlabel('Authors',fontdict={'fontsize': 14,'fontweight': 10})
  plt.ylabel('No. of messages',fontdict={'fontsize': 14,'fontweight': 10})
  plt.title('Mostly active member of Group',fontdict={'fontsize': 20,'fontweight': 8})
  plt.xticks(x_pos, h)
  st.pyplot()  
  original_title = '<p style="font-family:Courier; color:Pink; font-size: 30px;"> Most Busy Hours Of the day</p>'
  st.markdown(original_title, unsafe_allow_html=True)
  plt.figure(figsize=(8,5))
  t = message_df['time'].value_counts().head(20)
  tx = t.plot.bar()
#  tx.yaxis.set_major_locator(MaxNLocator(integer=True))  #Converting y axis data to integer
  plt.xlabel('Time',fontdict={'fontsize': 12,'fontweight': 10})
  plt.ylabel('No. of messages',fontdict={'fontsize': 12,'fontweight': 10})
  plt.title('Analysis of time when Group was highly active.',fontdict={'fontsize': 18,'fontweight': 8})
  plt.show()
  st.pyplot()
  df['Year'] = df['date'].dt.year
  df['Mon'] = df['date'].dt.month
  months = {
     1 : 'Jan',
     2 : 'Feb',
     3 : 'Mar',
     4 : 'Apr',
     5 : 'May',
     6 : 'Jun',
     7 : 'Jul',
     8 : 'Aug',
     9 : 'Sep',
    10 : 'Oct',
    11 : 'Nov',
    12 : 'Dec'
  }
  df['Month'] = df['Mon'].map(months)
  df.drop('Mon',axis=1,inplace=True)
  #st.write(df['Month'].head())
  original_title = '<p style="font-family:Courier; color:Pink; font-size: 30px;"> Mostly Active Year </p>'
  st.markdown(original_title, unsafe_allow_html=True) 
 
  z = df['Year'].value_counts() 
  z1 = z.to_dict() #converts to dictionary
  df['Msg_count_yearly'] = df['Year'].map(z1)
  plt.figure(figsize=(18,9))
  sns.set_style("darkgrid")
  sns.lineplot(data=df,x='Year',y='Msg_count_yearly',markers=True,marker='o')
  plt.xlabel('Month',fontdict={'fontsize': 14,'fontweight': 10})
  plt.ylabel('No. of messages',fontdict={'fontsize': 14,'fontweight': 10})
  plt.title('Analysis of mostly active year using line plot.',fontdict={'fontsize': 20,'fontweight': 8})
  plt.show()
  st.pyplot()
  #message_df['Hours'] = pd.to_datetime(message_df['time'], format='%H:%M:%S').dt.hour
  
  ### Analysing on which time group is mostly active based on hours and day.
 
  weeks = {
  0 : 'Monday',
  1 : 'Tuesday',
  2 : 'Wednesday',
  3 : 'Thrusday',
  4 : 'Friday',
  5 : 'Saturday',
  6 : 'Sunday'
  }
  original_title = '<p style="font-family:Courier; color:Pink; font-size: 30px;"> Date on which Group was highly active</p>'
  st.markdown(original_title, unsafe_allow_html=True) 
  message_df['Day'] = message_df['date'].dt.weekday.map(weeks)
  plt.figure(figsize=(8,5))
  message_df['date'].value_counts().head(15).plot.bar()
  plt.xlabel('date',fontdict={'fontsize': 14,'fontweight': 10})
  plt.ylabel('No. of messages',fontdict={'fontsize': 14,'fontweight': 10})
  plt.title('Analysis of Date on which Group was highly active',fontdict={'fontsize': 18,'fontweight': 8})
  plt.show()
  st.pyplot()
  original_title = '<p style="font-family:Courier; color:Pink; font-size: 30px;"> Mostly Active Day Of The Week </p>'
  st.markdown(original_title, unsafe_allow_html=True) 
  plt.figure(figsize=(8,5))
  active_day = message_df['Day'].value_counts()
### Top 10 peoples that are mostly active in our Group is : 
  a_d = active_day.head(10)
  a_d.plot.bar()
  plt.xlabel('Day',fontdict={'fontsize': 12,'fontweight': 10})
  plt.ylabel('No. of messages',fontdict={'fontsize': 12,'fontweight': 10})
  plt.title('Mostly active day of Week in the Group',fontdict={'fontsize': 18,'fontweight': 8})
  plt.show()
  #df['Day']
  st.pyplot()  
  z = message_df['date'].value_counts() 
  z1 = z.to_dict() #converts to dictionary
  message_df['Msg_count'] = message_df['date'].map(z1)
### Timeseries plot 
  fig = px.line(x=message_df['date'],y=message_df['Msg_count'])
  fig.update_layout(title='Analysis of number of message"s using TimeSeries plot.',
                  xaxis_title='Month',
                  yaxis_title='No. of Messages')
  fig.update_xaxes(nticks=20)
  
  st.plotly_chart(fig)
 if(option!='All'):
    original_title = '<p style="font-family:Courier; color:Pink; font-size: 30px;"> Word Cloud</p>'
    st.markdown(original_title, unsafe_allow_html=True)  
    st.write(option)  
    dummy_df=message_df[message_df["author"]==option]
    text=" ".join(r for r in dummy_df.message)
    stopwords=set(STOPWORDS)
    stopwords=["kya","toh","toh","ki","hai","se","koi","haan","hi","me","h","ky","nahi","yr","m","ye","he","are","to","abhi","ka","tho","or","na","haa","han","fir"]

    wordcloud=WordCloud(stopwords=stopwords,background_color="white").generate(text)
    print(option)
    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud,interpolation="bilinear")
    plt.axis("off")
    plt.show()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
    
 original_title = '<p style="font-family:Courier; color:Red; font-size: 30px;"> THATS ALL ABOUT YOUR WHATSAPP GROUP</p>'
 st.markdown(original_title, unsafe_allow_html=True) 
 original_title = '<p style="font-family:Courier; color:#c93c3b; font-size: 35px;"> THANKS FOR USING THIS APP</p>'
 st.markdown(original_title, unsafe_allow_html=True)   
  
    
    

