#!/usr/bin/env python
# coding: utf-8

# In[2]:


#import libaries
import pandas as pd
import seaborn as sns


# In[3]:


df = pd.read_csv("TWO_CENTURIES_OF_UM_RACES.csv")


# In[4]:


#See the data has been imported
df.head(15)


# In[5]:


df.shape


# In[7]:


df.summary


# In[9]:


df.dtypes


# In[11]:


#clean up data
#Only want USA races, 50k or 50Mi, 2020
df[df['Event distance/length']== '50mi']


# In[12]:


#combine 50k/50mi with isin 

df[df['Event distance/length'].isin(['50km','50mi'])]


# In[13]:


df[(df['Event distance/length'].isin(['50km','50mi'])) & (df['Year of event'] == 2020)]


# In[14]:


df[df['Event name'].str.split('(').str.get(1).str.split(')').str.get(0) == 'USA']


# In[15]:


#combine all filters together 
df[(df['Event distance/length'].isin(['50km','50mi'])) & (df['Year of event'] == 2020)& (df['Event name'].str.split('(').str.get(1).str.split(')').str.get(0) == 'USA')]


# In[16]:


df2 = df[(df['Event distance/length'].isin(['50km','50mi'])) & (df['Year of event'] == 2020)& (df['Event name'].str.split('(').str.get(1).str.split(')').str.get(0) == 'USA')]


# In[17]:


df2.shape


# In[18]:


#remove (USA) from event name
df2['Event name'].str.split('(').str.get(0)


# In[19]:


df2['Event name'] = df2['Event name'].str.split('(').str.get(0)


# In[21]:


df2.head(10)


# In[22]:


#clean up athlete age
df2['athlete_age'] = 2020 - df2['Athlete year of birth']


# In[25]:


#remove h from athlete performance
df2['Athlete performance'] = df2['Athlete performance'].str.split(' ').str.get(0)


# In[26]:


df2.head(10)


# In[28]:


#drop columns: Athlete club,Athlete Country, Athlete year of birth, Athlete age category
df2 = df2.drop(['Athlete club','Athlete country','Athlete year of birth','Athlete age category'], axis = 1)


# In[29]:


df2.head()


# In[30]:


#clean up null values
df2.isna().sum()


# In[31]:


df2 = df2.dropna()


# In[32]:


#check for duplicates
df2[df2.duplicated() == True]


# In[33]:


df2.reset_index(drop = True)


# In[34]:


#fix types
df2.dtypes


# In[35]:


df2['athlete_age'] = df2['athlete_age'].astype(int)
df2['Athlete average speed'] = df2['Athlete average speed'].astype(float)


# In[36]:


df2.dtypes


# In[44]:


#rename columns
df2 = df2.rename(columns = {'Year of event':'year',
                            'Event dates' : 'race_day',
                            'Event name' : 'race_name',
                            'Event distance/length': 'race_length',
                            'Event number of finishers' : 'race_number_of_finishers',
                            'Athlete performance': 'athlete_performace',
                            'Athlete gender' : 'athlete_gender',
                            'Athlete average speed' : 'athlete_average_speed',
                            'Athlete ID': 'athlete_id'
 
                           })


# In[45]:


df2.head()


# In[46]:


#reorder columns

df2 = df2.rename(columns = {'Year of event':'year',
                            'Event dates' : 'race_day',
                            'Event name' : 'race_name',
                            'Event distance/length': 'race_length',
                            'Event number of finishers' : 'race_number_of_finishers',
                            'Athlete performance': 'athlete_performace',
                            'Athlete gender' : 'athlete_gender',
                            'Athlete average speed' : 'athlete_average_speed',
                            'Athlete ID': 'athlete_id'
 
                           })



# In[47]:


df2.head()


# In[ ]:





# In[50]:


df2.head()


# In[ ]:





# In[53]:


df2.dtypes


# In[54]:


df2.head(10)


# In[55]:


df2 = df2.rename(columns = {
                            'athlete_performace' : 'race_number_of_finishers',
                           })


# In[56]:





# In[57]:


df2.dtypes


# In[58]:


df2 = df2.rename(columns = {'Year of event':'year',
                            'Event dates' : 'race_day',
                            'Event name' : 'race_name',
                            'Event distance/length': 'race_length',
                            'Event number of finishers' : 'race_number_of_finishers',
                            'Athlete performance': 'athlete_performace',
                            'Athlete gender' : 'athlete_gender',
                            'Athlete average speed' : 'athlete_average_speed',
                            'Athlete ID': 'athlete_id'
})


# In[59]:


df2.dtypes


# In[60]:


df2=df2.rename(columns = {'race_number_of_finishers':'number_of_finishers',
                          'race_number_of_finishers':'athlete_performance'
                          
    
})


# In[61]:


df2.dtypes


# In[63]:


df2.columns = ['year','race_day','race_name','race_length','race_number_of_finishers','athlete_performance','athlete_gender','athlete_average_speed','athlete_id','athlete_age']


# In[64]:


df2.dtypes


# In[65]:


df2.head()


# In[66]:


df3 = df2[['race_day','race_name','race_length','race_number_of_finishers','athlete_id','athlete_gender','athlete_age','athlete_performance','athlete_average_speed','year']]


# In[67]:


df3.head()


# In[68]:


sns.histplot(df3['race_length'])


# In[69]:


sns.histplot(df3,x = 'race_length', hue = 'athlete_gender')


# In[70]:


sns.displot(df3[df3['race_length']== '50mi']['athlete_average_speed'])


# In[72]:


sns.violinplot(data = df3, x = 'race_length',y = 'athlete_average_speed', hue = 'athlete_gender',split = True, inner = 'quart', linewidth = 1)


# In[74]:


sns.lmplot(data=df3, x = 'athlete_age', y = 'athlete_average_speed', hue = 'athlete_gender')


# In[75]:


#Diffrence in speed for the 50k, 50mi male to female

df3.groupby(['race_length','athlete_gender'])['athlete_average_speed'].mean()


# In[85]:


#what age group are the best in the 50m Race (20 + races min)
df3.query('race_length == "50 mi"').groupby('athlete_age')['athlete_average_speed'].agg(['mean','count']).sort_values('mean',ascending = False).query('count>19') 


# In[86]:


df3['race_month'] = df3['race_day'].str.split('.').str.get(1).astype(int)


# In[87]:


df3.head()


# In[ ]:




