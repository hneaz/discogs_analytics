#!/usr/bin/env python
# coding: utf-8

# # Discogs Analysis
# 
# 
# [Discogs Developer](https://www.discogs.com/developers/#page:home,header:home-quickstart)
# 
# [Download Discogs Data](https://data.discogs.com/)
# 
# [Discogs Database Search](https://www.discogs.com/developers/#page:database,header:database-search)
# 
# [Discogs Oauth](https://github.com/jesseward/discogs-oauth-example)
# 
# Need data on location of purchase
# 
# ### Key Questions to answer:
# 
# * What is the profile of my record collection?
# 
# * What are the most expensive records and CDs I own?
# 
# * Which band/artist do I own the most and what is the cost of that?
# 
# * Which record label do I support the most and which did I spent the most?
# 
# * Which subgenre costs the most and which one is worth the most?
# 
# * Is there a difference between autographed and non-authographed records?
# 
# * What is the breakdown of the format and the cost, min price, median price, and max price?

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
import ydata-profiling
#import cufflinks as cf
import plotly.offline
#cf.go_offline()
#cf.set_config_file(offline=False, world_readable=True)
from pylab import rcParams
sns.set(rc={'figure.figsize':(16,12)})
plt.style.use('ggplot')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_row', None)


# In[3]:


discogs_df = pd.read_csv('../data/discogs_data.csv')
discogs_df.head(10)


# Some of the labels are separated by commas.

# In[4]:


discogs_df = pd.concat([discogs_df, discogs_df['Label'].str.split(', ', expand=True)], axis=1)
discogs_df.head(20)


# Rename columns

# In[5]:


discogs_df.rename(columns={0:'Label1',1:'Label2',2:'Label3',3:'Label4'}, inplace=True)
discogs_df.head()


# Export for inspection

# In[6]:


discogs_df.to_csv('../output/discogs_clean_data.csv',index=False)


# ## Label Sorting
# 
# Label must be sorted. There is an issue like this where Svart Records is placed before 20 Buck Spin

# In[7]:


twentybuck = discogs_df[discogs_df['Label'].str.contains("20 Buck Spin")]
twentybuck


# In[8]:


discogs_df['Label'][discogs_df['Artist'] == 'Oranssi Pazuzu']


# In[9]:


list = ['Svart Records', '20 Buck Spin']
list


# Sort like this

# In[10]:


list.sort()
list


# Drop column

# In[11]:


# Drop columns
discogs_df = discogs_df.drop(columns=['Rating','Collection Media Condition', 
                                      'Collection Notes','Collection Sleeve Condition'])


# In[12]:


discogs_df['Collection Autographed'] = discogs_df['Collection Autographed'].fillna('No')


# ## Create new columns:
# 
# * Artist - Label  
# * pct_profit_min  
# * pct_profit_median  
# * pct_profit_max  

# In[13]:


discogs_df['Record'] = discogs_df['Artist'] + ' - ' + discogs_df['Title']
discogs_df[['Artist','Label','Record']].head()


# Run Pandas Profiler

# In[ ]:


profile = discogs_df.profile_report(title='Discogs Data Profiling Report',correlations={"cramers": False})


# In[ ]:


profile


# Here are some interesting information about my record collection: 
# 
# 1) I purchased around 408 albums in vinyl, CD, and tape format.  
# 2) I have 188 unique artists in my collection. I also have 10 artists that collaborated with others.  
# 3) My top five bands are:
# 
# |        Artist2              |   Count   |  Percentage  |
# |:---------------------------:|:---------:|:------------:|
# |  Opeth	                  |    19	  |      4.7%	 |
# |  Cult Of Luna	              |    16	  |      3.9%	 |
# |  Isis (6)	                  |    12	  |      2.9%	 |
# |  Panopticon (6)	          |    11	  |      2.7%	 |
# |  Between The Buried And Me  |    10	  |      2.5%	 |
# 
# 4) I own 388 distinct albums.   
# 5) In my collection, 84.3% are vinyl and 15.4\% are CD. I have 2 Tapes.
# 
# 6) My top 5 genres are:     
# 
# |  Genre       |  Count  |  Percentage  |
# |:------------:|:-------:|:------------:|
# |  Metal	   |   358	 |     87.7%    |	 
# |  Rock	       |   31	 |     7.6%	    | 
# |  Electronic  |   12	 |     2.9%	    | 
# |  Pop	       |   3	 |     0.7%	    | 
# |  Hip Hop	   |   2	 |     0.5%	    |
# 
# 7) My top 5 subgenres are:  
# 
# |       Genre          |  Count  |  Percentage  |
# |:--------------------:|:-------:|:------------:|
# |  Black Metal	       |    83	 |     20.3%    | 
# |  Progressive Metal   |    62	 |     15.2%    | 
# |  Post Metal	       |    61	 |     15.0%    | 
# |  Djent	           |    26	 |     6.4%	    |
# |  Sludge Metal	       |    26	 |     6.4%	    |
# 
# 
# 7) I typically pay \\$15 (50 or 12.3\%) for a record. The next is \\$20 (49 or 12.0\%).     
# 8) The most frequent album sold at the `_Max_` price is \\$29.99 (12 or 2.9\%). Next is \\$39.99 (9 or 2.2\%).
# 
# 9) My top five record labels are:  
# 
# |        Label         |  Count  |  Percentage  |
# |:--------------------:|:-------:|:------------:|
# |  Relapse Records	   |    23	 |      5.6%	| 
# |  Century Media	   |    17	 |      4.2%	| 
# |  Prosthetic Records  |    13	 |      3.2%	| 
# |  Hydra Head Records  |    12	 |      2.9%	| 
# |  20 Buck Spin	       |    10	 |      2.5%	|
# 
# 10) Most albums I buy were released in the last several years: 
# 
# |  Year  |  Count  |  Percentage  |
# |:------:|:-------:|:------------:|
# |  2014	 |   61	   |     15.0%    |	 
# |  2013	 |   55	   |     13.5%    |	 
# |  2016	 |   52	   |     12.7%    |	 
# |  2015	 |   48	   |     11.8%    |
# |  2017	 |   40	   |     9.8%     |

# Get summary statistics

# In[ ]:


discogs_df.describe()


# Run correlation

# In[ ]:


corrMatrix = discogs_df.corr()
sns.heatmap(corrMatrix, annot=True)


# ## Plot boxplot of the collection cost, minimum sold, median sold, and max sold.

# In[ ]:


sns.boxplot(x="variable", y="value", data=pd.melt(discogs_df[['Collection_Cost','_Min_','_Median_','_Max_']]))


# Remove outlier

# In[ ]:


sns.boxplot(x="variable", y="value", data=pd.melt(discogs_df[['Collection_Cost','_Min_','_Median_','_Max_']][discogs_df.Collection_Cost < discogs_df['Collection_Cost'].max()]))


# In[ ]:


sns.boxplot(x="variable", y="value", data=pd.melt(discogs_df[['Collection_Cost','_Min_','_Median_']][discogs_df.Collection_Cost < discogs_df['Collection_Cost'].max()]))


# In[ ]:


discogs_df[['Collection_Cost','_Min_','_Median_','_Max_']].sum().reset_index()


# In[ ]:


print('I spent $', discogs_df['Collection_Cost'].sum(),' on music that is recorded on Discogs. \n \nMy collection is worth $',discogs_df['_Median_'].sum())


# In[ ]:


discogs_df[['Collection_Cost','_Min_','_Median_','_Max_']].mean().reset_index()


# In[ ]:


print('I spent on averege $', discogs_df['Collection_Cost'].mean().round(2),' on per album that is recorded on Discogs. \n \nMy average collection is worth $',discogs_df['_Median_'].mean().round(2))


# ## What is the most expensive record I bought?

# In[ ]:


max_cost = discogs_df[discogs_df['Collection_Cost']==discogs_df['Collection_Cost'].max()]
max_cost


# In[ ]:


max_cost[['Artist','Title','Format','Collection_Cost','_Median_','Genre','Subgenre']]


# In[ ]:


print('This record has 7 full length albums and 3 EPs plus a DVD and a lyric book')


# The most expensive record I own is the Meshuggah - 25 Years Of Musical Deviance, Boxset.

# ## What is the least expensive record I own?

# In[ ]:


min_cost = discogs_df[discogs_df['Collection_Cost']==discogs_df['Collection_Cost'].min()]
min_cost


# In[ ]:


min_cost[['Artist','Title','Format','Collection_Cost','_Median_','Genre','Subgenre']]


# In[ ]:


print('I got this record for free from a friend')


# ## What is the least expensive record I bought?

# In[ ]:


purchased_df = discogs_df[discogs_df.Collection_Cost > 0]
min_purchase = purchased_df[purchased_df['Collection_Cost']==purchased_df['Collection_Cost'].min()]
min_purchase[['Artist','Title','Format','Collection_Cost','_Median_','Genre','Subgenre']]


# I bought Wyclef Jean 2xLP at the basement of Dusty Groove for 50 cents.

# ## What are the top 10 records I spent the most?

# In[ ]:


discogs_df[['CollectionFolder','Record','Genre','Subgenre',
            'Collection_Autographed','Collection_Cost',
            '_Min_','_Median_','_Max_']].sort_values('Collection_Cost',ascending = False).head(10)


# In[ ]:


discogs_df[['CollectionFolder','Record','Genre','Subgenre',
            'Collection_Autographed','Collection_Cost',
            '_Min_','_Median_','_Max_']].sort_values('Collection_Cost',ascending = False).groupby('CollectionFolder').head(10)


# ## What are the top 10 bands with the most expensive records purchased?

# In[ ]:


record_sum   = discogs_df.groupby(['Artist2']).agg({
                       'Title': 'count',
                       'Label': 'nunique',
                       'Collection_Cost': 'sum',
                       '_Min_': 'sum',
                       '_Median_': 'sum',
                       '_Max_': 'sum'
                        }).reset_index().sort_values(by='_Median_',ascending=False)


# ## Plot top 10 bands that I purchased the most by cost

# In[ ]:


chart = sns.catplot(x="Artist2", y="Collection_Cost", kind="bar", 
                    data=record_sum.sort_values('Collection_Cost',ascending=False).head(10),
                    height=6, aspect=1.5)
chart.set_xticklabels(rotation=45, horizontalalignment='right')
plt.title('Top 10 Most Spent Records by Bands')

record_sum.sort_values('Collection_Cost',ascending=False).head(10)


# ## What the most records purchased by the Top 10 bands?

# In[ ]:


chart = sns.catplot(x="Artist2", y="Title", kind="bar", 
                    data=record_sum.sort_values('Title',ascending=False).head(10),
                    height=6, aspect=1.5)
chart.set_xticklabels(rotation=45, horizontalalignment='right')
plt.title('Top 10 Most Frequently Bought Records by Bands')

record_sum.sort_values('Title',ascending=False).head(10)


# ## What are the top 10 most valuable record by min?

# In[ ]:


chart = sns.catplot(x="Record", y="_Min_", kind="bar", 
                    data=discogs_df.sort_values('_Max_',ascending=False).head(10),
                    height=6, aspect=1.5)
chart.set_xticklabels(rotation=45, horizontalalignment='right')
plt.title('Top 10 Most Valuable Records by Min')

discogs_df[['Record','Collection_Cost',
            '_Min_','_Median_','_Max_']].sort_values('_Min_',ascending=False).head(10)


# ## What are the top 10 most valuable record by median?

# In[ ]:


chart = sns.catplot(x="Record", y="_Median_", kind="bar", 
                    data=discogs_df.sort_values('_Median_',ascending=False).head(10),
                    height=6, aspect=1.5)
chart.set_xticklabels(rotation=45, horizontalalignment='right')
plt.title('Top 10 Most Valuable Records by Median')

discogs_df[['Record','Title','Subgenre','Collection_Cost',
            '_Min_','_Median_','_Max_']].sort_values('_Median_',ascending=False).head(10)


# ## What are the top 10 most valuable record by max?

# In[ ]:


chart = sns.catplot(x="Record", y="_Max_", kind="bar", 
                    data=discogs_df.sort_values('_Max_',ascending=False).head(10),
                    height=6, aspect=1.5)
chart.set_xticklabels(rotation=45, horizontalalignment='right')
plt.title('Top 10 Most Valuable Records by Max')

discogs_df[['Record','Collection_Cost',
            '_Min_','_Median_','_Max_']].sort_values('_Max_',ascending=False).head(10)


# The Meshuggah boxset was sold for 514.17 and I bought it for 232.

# ## What are the Top 10 albums sold by average?

# In[ ]:


record_mean   = discogs_df.groupby(['Artist2']).agg({
                       'Title': 'count',
                       'Label': 'nunique',
                       'Collection_Cost': 'mean',
                       '_Min_': 'mean',
                       '_Median_': 'mean',
                       '_Max_': 'mean'
                        }).reset_index().sort_values(by='_Median_',ascending=False)


# In[ ]:


chart = sns.catplot(x="Artist2", y="_Median_", kind="bar", 
                    data=record_mean.sort_values('_Median_',ascending=False).head(10),
                    height=6, aspect=1.5)
plt.title('Top 10 Average Sold by Median')
chart.set_xticklabels(rotation=45, horizontalalignment='right')
record_mean.sort_values('_Median_',ascending=False).head(10)


# ## What are the Top 10 albums sold by max?

# In[ ]:


chart = sns.catplot(x="Artist2", y="_Max_", kind="bar", 
                    data=record_mean.sort_values('_Max_',ascending=False).head(10),
                    height=6, aspect=1.5)
plt.title('Top 10 Average Sold by Max')
chart.set_xticklabels(rotation=45, horizontalalignment='right')
record_mean.sort_values('_Max_',ascending=False).head(10)


# ### Opeth Analysis

# In[ ]:


discogs_df[['Artist2','Title','Collection_Cost','_Min_','_Median_','_Max_']][discogs_df.Artist2 == 'Opeth'].sort_values('_Max_',ascending=False)


# # Label Analysis

# In[ ]:


label_sum   = discogs_df.groupby(['Label']).agg({
                       'Artist2': 'nunique',
                       'Title': 'count',
                       'Collection_Cost': 'sum',
                       '_Min_': 'sum',
                       '_Median_': 'sum',
                       '_Max_': 'sum'
                        }).reset_index().sort_values(by='_Median_',ascending=False)
label_sum.head()


# ## Which record labels did I spend the most?

# In[ ]:


chart = sns.catplot(x="Label", y="Collection_Cost", kind="bar", 
                    data=label_sum.sort_values('Collection_Cost',ascending=False).head(10),
                    height=6, aspect=1.5)
chart.set_xticklabels(rotation=45, horizontalalignment='right')
label_sum.sort_values('Collection_Cost',ascending=False).head(10)


# In[ ]:


discogs_df.columns


# In[ ]:


discogs_df.Date_Added = pd.to_datetime(discogs_df.Date_Added).dt.strftime('%m/%Y')
discogs_df.Date_Added.head()


# # Time Series

# ### Group data by `Released` and `Date_Added` then get sum by `Collection_Cost`, `_Min_`, `_Median_`, and `_Max_`.

# In[ ]:


time_df  = discogs_df.groupby(['Released','Date_Added']).agg({
                               'Collection_Cost': 'sum',
                               'Artist': 'nunique',
                               'Artist2': 'nunique',
                               'Title': 'count',
                               '_Min_': 'sum',
                               '_Median_': 'sum',
                               '_Max_': 'sum'
                                }).reset_index().sort_values(by='Date_Added',ascending=True)
time_df.head()


# Plot `Date_Added` over `Collection_Cost`

# In[ ]:


plt.plot(time_df['Date_Added'], time_df['Collection_Cost'])
plt.gcf().autofmt_xdate()
plt.show()


# Plot `Date_Added` over `Title`

# In[ ]:


plt.plot(time_df['Date_Added'], time_df['Title'])
plt.gcf().autofmt_xdate()
plt.show()


# Plot `Date_Added` over `Artist2`

# There were some days that I logged many records at once on discogs.

# In[ ]:


plt.plot(time_df['Date_Added'], time_df['Artist2'])
plt.gcf().autofmt_xdate()
plt.show()


# ### Group data by `Released`

# In[ ]:


year_df  = discogs_df.groupby(['Released']).agg({
                               'Artist2': 'count',
                               'Title': 'count',
                               'CollectionFolder':'count',
                               'Genre':'count', 
                               'Subgenre':'count',
                               'Collection_Cost': 'sum',
                               '_Min_': 'sum',
                               '_Median_': 'sum',
                               '_Max_': 'sum'
                                }).reset_index().sort_values(by='Released',ascending=True)
year_df.head()


# In[ ]:


year_df['Released'].describe()


# In[ ]:


plt.plot(year_df['Released'], year_df['Artist2'])
plt.gcf().autofmt_xdate()
plt.show()


# In[ ]:


plt.plot(year_df['Released'], year_df['Title'])
plt.gcf().autofmt_xdate()
plt.show()


# In[ ]:


chart = sns.catplot(x="Released", y="Title", kind="bar", 
                    data=year_df.sort_values('Released',ascending=True),
                    height=6, aspect=1.5)
chart.set_xticklabels(rotation=45, horizontalalignment='right')


# In[ ]:


chart = sns.catplot(x="Released", y="_Min_", kind="bar", 
                    data=year_df.sort_values('Released',ascending=True),
                    height=6, aspect=1.5)
chart.set_xticklabels(rotation=45, horizontalalignment='right')


# In[ ]:


chart = sns.catplot(x="Released", y="_Median_", kind="bar", 
                    data=year_df.sort_values('Released',ascending=True),
                    height=6, aspect=1.5)
chart.set_xticklabels(rotation=45, horizontalalignment='right')


# In[ ]:


chart = sns.catplot(x="Released", y="_Max_", kind="bar", 
                    data=year_df.sort_values('Released',ascending=True),
                    height=6, aspect=1.5)
chart.set_xticklabels(rotation=45, horizontalalignment='right')


# In[ ]:


chart = sns.catplot(x="Released", y="Collection_Cost", kind="bar", 
                    data=year_df.sort_values('Released',ascending=True),
                    height=6, aspect=1.5)
chart.set_xticklabels(rotation=45, horizontalalignment='right')


# In[ ]:


# https://seaborn.pydata.org/generated/seaborn.FacetGrid.html
# bins = np.arange(0, 65, 5)
# g = sns.FacetGrid(discogs_df, col="Format",  row="Collection_Autographed")
# g = g.map(plt.hist, "Collection_Cost", bins=bins, color="r")


# In[ ]:


# tips = sns.load_dataset("tips")
# g = sns.FacetGrid(tips, col="time",  row="smoker")
# g = g.map(plt.hist, "total_bill")


# # Genre and Subgenre analysis

# In[ ]:


discogs_df.Genre.value_counts()


# In[ ]:


fig, axes = plt.subplots(2, 2)

ax = sns.boxplot(x="Genre", y="Collection_Cost", data=discogs_df, orient='v', 
    ax=axes[0, 0])
ax = sns.boxplot(x="Genre", y="_Min_", data=discogs_df, orient='v', 
    ax=axes[0, 1])
ax = sns.boxplot(x="Genre", y="_Median_", data=discogs_df, orient='v', 
    ax=axes[1, 0])
ax = sns.boxplot(x="Genre", y="_Max_", data=discogs_df, orient='v', 
    ax=axes[1, 1])


# Remove records less than 2

# In[ ]:


genre_reduced = discogs_df['Genre'].value_counts()[lambda x: x>2].index.tolist()
genre_reduced


# In[ ]:


genre_reduced_df = discogs_df[(discogs_df['Genre'].isin(genre_reduced)) & (discogs_df.Collection_Cost < 200)]
genre_reduced_df.head()


# In[ ]:


genre_reduced_df.Genre.value_counts()


# ## Boxplot Genre by Collection_Cost, Min, Median, and Max

# In[ ]:


fig, axes = plt.subplots(2, 2)

ax = sns.boxplot(x="Genre", y="Collection_Cost", data=genre_reduced_df, orient='v', 
    ax=axes[0, 0])
ax = sns.boxplot(x="Genre", y="_Min_", data=genre_reduced_df, orient='v', 
    ax=axes[0, 1])
ax = sns.boxplot(x="Genre", y="_Median_", data=genre_reduced_df, orient='v', 
    ax=axes[1, 0])
ax = sns.boxplot(x="Genre", y="_Max_", data=genre_reduced_df, orient='v', 
    ax=axes[1, 1])


# In[ ]:


sns.set_style('whitegrid')
sns.pairplot(genre_reduced_df[['Genre','Collection_Cost','_Min_','_Median_','_Max_']],hue='Genre',size=3)
plt.show()


# In[ ]:


sns.FacetGrid(genre_reduced_df,hue="Genre",size=8).map(sns.distplot,
'Collection_Cost').add_legend()
plt.show()


# In[ ]:


sns.FacetGrid(genre_reduced_df,hue="Genre",size=8).map(sns.distplot,
'_Min_').add_legend()
plt.show()


# In[ ]:


sns.FacetGrid(genre_reduced_df,hue="Genre",size=8).map(sns.distplot,
'_Median_').add_legend()
plt.show()


# In[ ]:


sns.FacetGrid(genre_reduced_df,hue="Genre",size=8).map(sns.distplot,
'_Max_').add_legend()
plt.show()


# In[ ]:


sns.pairplot(genre_reduced_df, x_vars=["Collection_Cost"], y_vars=['_Min_','_Median_','_Max_'],
             hue="Genre", height=5, aspect=1.5, kind="reg");


# ## Subgenre Analysis

# In[ ]:


discogs_df.Subgenre.value_counts()


# In[ ]:


subgenre_reduced = discogs_df['Subgenre'].value_counts()[lambda x: x>5].index.tolist()
subgenre_reduced


# In[ ]:


subgenre_reduced_df = discogs_df[(discogs_df['Subgenre'].isin(subgenre_reduced)) & (discogs_df.Collection_Cost < 200)]
subgenre_reduced_df.head()


# ## Boxplot Subgenre by Collection_Cost, Min, Median, and Max

# In[ ]:


fig, axes = plt.subplots(2, 2)

ax = sns.boxplot(x="Subgenre", y="Collection_Cost", data=subgenre_reduced_df, orient='v', 
    ax=axes[0, 0])
ax.set_xticklabels(ax.get_xticklabels(),rotation=45)
ax = sns.boxplot(x="Subgenre", y="_Min_", data=subgenre_reduced_df, orient='v', 
    ax=axes[0, 1])
ax.set_xticklabels(ax.get_xticklabels(),rotation=45)
ax = sns.boxplot(x="Subgenre", y="_Median_", data=subgenre_reduced_df, orient='v', 
    ax=axes[1, 0])
ax.set_xticklabels(ax.get_xticklabels(),rotation=45)
ax = sns.boxplot(x="Subgenre", y="_Max_", data=subgenre_reduced_df, orient='v', 
    ax=axes[1, 1])
ax.set_xticklabels(ax.get_xticklabels(),rotation=45)


# Reduce to Top 5 subgenres

# In[ ]:


subgenre_reduced1 = discogs_df['Subgenre'].value_counts()[lambda x: x>25].index.tolist()
subgenre_reduced_df1 = discogs_df[(discogs_df['Subgenre'].isin(subgenre_reduced1)) & (discogs_df.Collection_Cost < 200)]


# In[ ]:


subgenre_reduced_df1.head()


# ## Boxplot Reduced Subgenre by Collection_Cost, Min, Median, and Max

# In[ ]:


fig, axes = plt.subplots(2, 2)

ax = sns.boxplot(x="Subgenre", y="Collection_Cost", data=subgenre_reduced_df1, orient='v', 
    ax=axes[0, 0])
ax.set_xticklabels(ax.get_xticklabels(),rotation=45)
ax = sns.boxplot(x="Subgenre", y="_Min_", data=subgenre_reduced_df1, orient='v', 
    ax=axes[0, 1])
ax.set_xticklabels(ax.get_xticklabels(),rotation=45)
ax = sns.boxplot(x="Subgenre", y="_Median_", data=subgenre_reduced_df1, orient='v', 
    ax=axes[1, 0])
ax.set_xticklabels(ax.get_xticklabels(),rotation=45)
ax = sns.boxplot(x="Subgenre", y="_Max_", data=subgenre_reduced_df1, orient='v', 
    ax=axes[1, 1])
ax.set_xticklabels(ax.get_xticklabels(),rotation=45)


# ## 3D Plot of Collection_Cost, Median, and Max

# In[ ]:


import plotly.express as px
fig = px.scatter_3d(subgenre_reduced_df1, x='Collection_Cost', y='_Median_', z='_Max_', color='Subgenre')
fig.show()


# ## Plot Collection_Cost vs Median by Subgenre

# In[ ]:


sns.set_style('whitegrid');
sns.FacetGrid(subgenre_reduced_df1,hue='Subgenre',size=10).map(plt.scatter,
'Collection_Cost','_Median_').add_legend();
plt.show();


# ## Plot Collection_Cost, Min, Median, and Max by Subgenre

# In[ ]:


sns.set_style('whitegrid')
sns.pairplot(subgenre_reduced_df1[['Subgenre','Collection_Cost','_Min_','_Median_','_Max_']],hue='Subgenre',size=3)
plt.show()


# In[ ]:


sns.pairplot(subgenre_reduced_df1, x_vars=["Collection_Cost"], y_vars=['_Min_','_Median_','_Max_'],
             hue="Subgenre", height=5, aspect=1.5, kind="reg");


# ## Distribution Plot Collection Cost by Subgenre

# In[ ]:


sns.FacetGrid(subgenre_reduced_df1,hue="Subgenre",size=8).map(sns.distplot,
'Collection_Cost').add_legend()
plt.show()


# ## Distribution plot Min by Subgenre

# In[ ]:


sns.FacetGrid(subgenre_reduced_df1,hue="Subgenre",size=8).map(sns.distplot,
'_Min_').add_legend()
plt.show()


# ## Distribution Plot Median by Subgenre

# In[ ]:


sns.FacetGrid(subgenre_reduced_df1,hue="Subgenre",size=8).map(sns.distplot,
'_Median_').add_legend()
plt.show()


# ## Distribution Plot Max by Subgenre

# In[ ]:


sns.FacetGrid(subgenre_reduced_df1,hue="Subgenre",size=8).map(sns.distplot,
'_Max_').add_legend()
plt.show()


# # Format Analysis

# ### What are my top 10 valuable records by format?

# In[ ]:


format_df = discogs_df[(discogs_df.CollectionFolder != 'Tape') & (discogs_df.Collection_Cost < 200)]


# In[ ]:


format_df1 = discogs_df[(discogs_df.CollectionFolder != 'Tape')]
format_top20_df = format_df1.sort_values("_Median_",ascending = False).groupby('CollectionFolder').head(20)

format_top20_df[['CollectionFolder','Record','Genre','Subgenre',
                 'Collection_Autographed','Collection_Cost','_Median_']]


# In[ ]:


sns.FacetGrid(format_df,hue="CollectionFolder",size=8).map(sns.distplot,'Collection_Cost').add_legend()
plt.show()


# In[ ]:


sns.FacetGrid(format_df,hue="CollectionFolder",size=8).map(sns.distplot,'_Min_').add_legend()
plt.show()


# In[ ]:


sns.FacetGrid(format_df,hue="CollectionFolder",size=8).map(sns.distplot,'_Median_').add_legend()
plt.show()


# In[ ]:


sns.FacetGrid(format_df,hue="CollectionFolder",size=8).map(sns.distplot,'_Max_').add_legend()
plt.show()


# In[ ]:


sns.set_style('whitegrid')
sns.pairplot(format_df[['CollectionFolder','Collection_Cost','_Min_','_Median_','_Max_']],hue='CollectionFolder',size=3)
plt.show()


# In[ ]:


fig, axes = plt.subplots(2, 2)

ax = sns.boxplot(x="CollectionFolder", y="Collection_Cost", data=format_df, orient='v', 
    ax=axes[0, 0])
ax = sns.boxplot(x="CollectionFolder", y="_Min_", data=format_df, orient='v', 
    ax=axes[0, 1])
ax = sns.boxplot(x="CollectionFolder", y="_Median_", data=format_df, orient='v', 
    ax=axes[1, 0])
ax = sns.boxplot(x="CollectionFolder", y="_Max_", data=format_df, orient='v', 
    ax=axes[1, 1])


# # Autographed Analysis

# In[ ]:


auto_df = discogs_df[(discogs_df.Collection_Autographed == 'Yes')]
auto_top20_df = auto_df.sort_values("_Max_",ascending = False).groupby('CollectionFolder').head(10)

auto_top20_df[['CollectionFolder','Record','Genre','Subgenre',
                 'Collection_Autographed','Collection_Cost','_Min_','_Median_','_Max_']]


# In[ ]:


sns.FacetGrid(auto_df,hue="CollectionFolder",size=8).map(sns.distplot,'Collection_Cost').add_legend()
plt.show()


# In[ ]:


discogs_df1 = discogs_df[discogs_df.Collection_Cost < 200]

sns.set_style('whitegrid')
sns.pairplot(discogs_df1[['Collection_Autographed','Collection_Cost','_Min_','_Median_','_Max_']],hue='Collection_Autographed',size=3)
plt.show()


# In[ ]:


fig, axes = plt.subplots(2, 2)

ax = sns.boxplot(x="Collection_Autographed", y="Collection_Cost", data=discogs_df1, orient='v', 
    ax=axes[0, 0])
ax = sns.boxplot(x="Collection_Autographed", y="_Min_", data=discogs_df1, orient='v', 
    ax=axes[0, 1])
ax = sns.boxplot(x="Collection_Autographed", y="_Median_", data=discogs_df1, orient='v', 
    ax=axes[1, 0])
ax = sns.boxplot(x="Collection_Autographed", y="_Max_", data=discogs_df1, orient='v', 
    ax=axes[1, 1])


# In[ ]:


import plotly.express as px
fig = px.scatter(subgenre_reduced_df1, x="Collection_Cost", y="_Median_", color='Collection_Autographed', 
                 facet_col="Subgenre",hover_name="Subgenre",hover_data=["Artist2","Title","Record"])
fig.update_xaxes(matches=None)
fig.show()


# In[ ]:


fig = px.scatter(subgenre_reduced_df1[subgenre_reduced_df1.CollectionFolder != 'Tape'], 
                 x="Collection_Cost", y="_Median_", color='Collection_Autographed', 
                 facet_col="Subgenre",facet_row="CollectionFolder",
                 hover_name="Subgenre",hover_data=["Artist2","Title","Record"])
fig.update_xaxes(matches=None)
fig.show()


# In[ ]:


year_sub_df  = subgenre_reduced_df1.groupby(['Released','Subgenre']).agg({
                                         'Artist2': 'count',
                                         'Title': 'count',
                                         'Collection_Cost': 'sum',
                                         '_Min_': 'sum',
                                         '_Median_': 'sum',
                                         '_Max_': 'sum'
                                         }).reset_index().sort_values(by='Released',ascending=True)

# Round
year_sub_df.head()


# In[ ]:


year_sub_cost_df = year_sub_df.pivot("Released", "Subgenre", "Collection_Cost")
year_sub_cost_df.round(0).tail()


# In[ ]:


ax = sns.heatmap(year_sub_cost_df, annot=True, fmt="")


# In[ ]:


year_sub_title_df = year_sub_df.pivot("Released", "Subgenre", "Title")
year_sub_title_df.tail()


# In[ ]:


ax = sns.heatmap(year_sub_title_df, annot=True, fmt="")


# In[ ]:


year_sub_title_df1 = year_sub_df.pivot("Released", "Subgenre", "Title")

ax = sns.heatmap(year_sub_title_df1, annot=True, fmt="f")


# In[ ]:


year_sub_title_df1 = year_sub_df[year_sub_df.Released >= 2010].pivot("Released", "Subgenre", "Title")
ax = sns.heatmap(year_sub_title_df1, annot=True, fmt="")


# In[ ]:


year_genre_df  = discogs_df.groupby(['Released','Genre']).agg({
                                     'Artist2': 'count',
                                     'Title': 'count',
                                     'Collection_Cost': 'sum',
                                     '_Min_': 'sum',
                                     '_Median_': 'sum',
                                     '_Max_': 'sum'
                                    }).reset_index().sort_values(by='Released',ascending=True)
year_genre_df.head()


# In[ ]:


year_genre_title_df1 = year_genre_df.pivot("Released", "Genre", "Title")
ax = sns.heatmap(year_genre_title_df1, annot=True, fmt="")


# In[ ]:


year_genre_title_df1 = year_genre_df[year_genre_df.Released >= 2010].pivot("Released", "Genre", "Title")
ax = sns.heatmap(year_genre_title_df1, annot=True, fmt="")


# ## Create animation for year

# ###  Example

# In[ ]:


df = px.data.gapminder()
df.head()


# In[ ]:


fig = px.bar(df, x="continent", y="pop", color="continent",
  animation_frame="year", animation_group="country",
             range_y=[0,4000000000])
fig.show()


# In[ ]:


fig = px.bar(df, y="continent", x="pop", color="continent",
  animation_frame="year", animation_group="country", orientation = 'h',
             range_x=[0,4000000000])
fig.show()


# ### Subgenre By Year

# In[ ]:


subgenre_reduced_df.head()


# In[ ]:


year_sub_df1  = subgenre_reduced_df.groupby(['Released','Subgenre']).agg({
                                         'Title': 'count',
                                         'Collection_Cost': 'sum',
                                         '_Min_': 'sum',
                                         '_Median_': 'sum',
                                         '_Max_': 'sum'
                                         }).reset_index().sort_values(by='Released',ascending=True)

# Round
year_sub_df1.head()


# In[ ]:


year_sub_df1['Released'].unique()


# In[ ]:


Released = pd.DataFrame({'Released':year_sub_df1['Released'].unique()})
Released


# In[ ]:


year_sub_df1['Subgenre'].unique()


# In[ ]:


Subgenre = pd.DataFrame({'Subgenre':year_sub_df1['Subgenre'].unique()})
Subgenre


# In[ ]:


def cartesian_product_basic(left, right):
    return (
       left.assign(key=1).merge(right.assign(key=1), on='key').drop('key', 1))


# In[ ]:


released_subgenre_df = cartesian_product_basic(Released, Subgenre)
released_subgenre_df.head()


# Left Join released_subgenre_df on year_sub_df1

# In[ ]:


year_sub_df1.head()


# In[ ]:


subgenre_df2 = released_subgenre_df.merge(year_sub_df1, on = ['Released','Subgenre'],how='left').fillna(0).sort_values(by=['Released','Subgenre'],ascending=True)
subgenre_df2.head()


# In[ ]:


subgenre_cum_df2 = subgenre_df2.groupby(['Released','Subgenre']).sum().groupby(['Subgenre']).cumsum().reset_index()
subgenre_cum_df2.head()


# Start animations here

# ## Title vs. Subgenre by Year

# In[ ]:


fig = px.bar(subgenre_cum_df2, x="Title", y="Subgenre", color="Subgenre",
  animation_frame="Released", range_x=[0,90], orientation = 'h')
fig.show()


# ## Collection_Cost vs. Subgenre by Year

# In[ ]:


fig = px.bar(subgenre_cum_df2, x="Collection_Cost", y="Subgenre", color="Subgenre",
  animation_frame="Released", range_x=[0,1600], orientation = 'h')
fig.show()


# ## Median vs. Subgenre by Year

# In[ ]:


fig = px.bar(subgenre_cum_df2, x="_Median_", y="Subgenre", color="Subgenre",
  animation_frame="Released", range_x=[0,2000], orientation = 'h')
fig.show()


# ## Title vs. Collection Cost by Year

# In[ ]:


px.scatter(subgenre_cum_df2,x = 'Title', y = 'Collection_Cost',color='Subgenre',
               size='_Median_',animation_frame='Released', animation_group='Subgenre',range_x = [0,100],
              range_y = [0,2000],text='Subgenre')


# ## Scatterplot - Title vs. Collection Cost by Year

# In[ ]:


px.scatter(subgenre_cum_df2,x = 'Collection_Cost', y = '_Median_',color='Subgenre',
               size='Title',animation_frame='Released', animation_group='Subgenre',range_x = [0,2000],
              range_y = [0,2100],text='Subgenre')


# Export data for Floursh

# In[ ]:


subgenre_cum_df2 = subgenre_cum_df2.sort_values(by=['Released','Collection_Cost'],ascending=[True,False])
subgenre_cum_df2.to_csv('../output/discogs_cum_sum_data.csv',index = False)


# In[ ]:


subgenre_cum_df2.set_index(['Released','Subgenre']).T


# In[ ]:




