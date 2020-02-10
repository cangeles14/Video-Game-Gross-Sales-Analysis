#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 12:33:01 2020

@author: christopher
"""
#Libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import random
# Set seaborn for all graphs
sns.set()

df = pd.read_csv('/Data Visualization/vgsalesGlobale.csv')

# Examine and clean the dataframe
df.query('Year >2015 & Global_Sales < 100').index
df.drop(df.query('Year >2015 & Global_Sales < 100').index, inplace=True)

# Take a look at the database
df.head()
        
def Global_Gross_Revenue(df):
    # Trend of gross revenue globally
    df[['Year','Global_Sales']].groupby('Year')['Global_Sales'].agg('sum')
    plt.plot(df[['Year','Global_Sales']].groupby('Year')['Global_Sales'].agg('sum'))
    plt.title('Gross Revenue 1980 - 2015')
    plt.xlabel('Years')
    plt.ylabel('Gross Revenue (in millions)')
    plt.savefig('Gross Revenue', dpi=600)
    
def Gross_Revenue_Region (df):
    # Same graph but with all regions on same graph
    plt.plot(df[['Year','NA_Sales']].groupby('Year')['NA_Sales'].agg('sum'), label = 'NA Sales')
    plt.plot(df[['Year','EU_Sales']].groupby('Year')['EU_Sales'].agg('sum'), label = 'EU Sales')
    plt.plot(df[['Year','JP_Sales']].groupby('Year')['JP_Sales'].agg('sum'), label = 'JP Sales')
    plt.title('Gross Revenue 1980 - 2015')
    plt.xlabel('Years')
    plt.ylabel('Gross Revenue (in millions)')
    plt.legend()
    plt.ylim(0,400)
    plt.savefig('Gross Revenue Comparitive', dpi=600)
    
def Nintendo_Revenue (df):
    # Running sum of Nintendo sales from 1980-2015
    df_Nintendo = df.query('Publisher == "Nintendo"')
    df_Nintendo[['Year','Global_Sales']].groupby('Year').agg('sum')
    # Plot
    plt.plot(df_Nintendo[['Year','Global_Sales']].groupby('Year').agg('sum'))
    plt.title('Sales Revenue for Nintendo from 1980-2015')
    plt.xlabel('Years')
    plt.ylabel('Revenue (in millions)')
    plt.ylim(0,250)
    plt.savefig('Sales Revenue Nintendo', dpi=600)
    
def Top_Platform_Sales (df):
    colors = ['#f27eb2', '#559aba','#d2dfe9', '#1c2340']
    Sales_List = ['NA_Sales','EU_Sales','JP_Sales','Global_Sales']
    for i in Sales_List:
            x = df[[i,'Platform']].groupby('Platform').agg('sum').sort_values(i, ascending=False).head(5)
            x.plot.barh(color=colors)
            plt.savefig(f'{i} for Platform',dpi=600,bbox_inches = "tight")
    
df[['Genre','Global_Sales']].groupby('Genre').agg('sum').sort_values('Global_Sales',ascending=False).head(3)


def Genre_Sale_Trends(df):
    # Create a new df, and find global sale trends for the top 3 genres
    df2 = pd.DataFrame(df.loc[(df.Genre=='Sports') | (df.Genre=='Action') | (df.Genre=='Shooter')])
    df2['Global_Sales'] = df2['Global_Sales'].astype(int)
    colors = ['#f27eb2', '#559aba','#d2dfe9', '#1c2340']
    sns.lineplot(x='Year', y='Global_Sales', data=df2, hue=df2.Genre, linewidth=6, color=colors)
    plt.ylim(-1,15)
    plt.ylabel('Global Sales in millions')
    plt.title('Global Sale Trends for Top Grossing Genres from 1980-2015')
    plt.savefig('Genre Sales Trends 1980 -2015', dpi=600)
    
def Top_5_Grossing_Games(df):
    # Top 5 highest grossing games rank and global sales
    top_10 = pd.DataFrame(df[['Global_Sales', 'Name']].head(5))
    plt.figure(figsize=(11,6))
    sns.barplot(x='Name', y='Global_Sales', data=top_10)
    plt.title('Top Grossing Games from 1980-2015')
    plt.ylabel('Global Sales in Millions')
    plt.savefig('Top Grossing Games from 1980-2015', dpi=600)
    
# Add wordcloud image for video game titles
    def word_cloud_img():
        wordcloud1 = WordCloud(max_font_size=350, collocations=False, \
                               max_words=60, width=1600, height=800, \
                               background_color="white").generate(' '.join(df.Name))
        def grey_color_func(word, font_size, position, orientation, random_state=None,
                            **kwargs):
            return "hsl(335, 100%%, %d%%)" % random.randint(60, 100)
        plt.figure(figsize=(8,4))
        plt.imshow(wordcloud1.recolor(color_func=grey_color_func), interpolation="bilinear")
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.show()
        plt.savefig('Video Game Title Word Cloud', dpi=600)
