import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd

url = 'http://www.imdb.com/chart/top'
resp = requests.get(url)
html = resp.text


#Getting relevant data using BeautifulSoup
soup = BeautifulSoup(html)
pretty_soup = soup.prettify()

movie_name = [desc.find('a').contents[0] for desc in soup.select('td.titleColumn')]
Credits = [desc.find('a')['title'] for desc in soup.select('td.titleColumn')]
year = [info.string for info in soup.select('td.titleColumn span.secondaryInfo')]
votes = [vote['data-value'] for vote in soup.select('td.posterColumn span[name=nv]')]
ratings = [rating['data-value'] for rating in soup.select('td.posterColumn span[name=ir]')]

#Transforming Data 
years =  [re.search('\((.*?)\)', yr).group(1) for yr in year]
Cast = [people.split(',') for people in Credits]
Director,Actor1,Actor2 = [],[],[]
for i in Cast:
    Director.append(re.search('(.*) \(dir.\)', i[0]).group(1))
    Actor1.append(i[1])
    Actor2.append(i[2])

#Converting the Data into a Pandas DataFrame
Movie_List = pd.DataFrame({
        'Movie Name' : movie_name,
        'Release Date' : years,
        'Director' : Director,
        'Actor 1' : Actor1,
        'Actor 2' : Actor2,
        'Rating' : ratings,
        'No. of Votes' : votes
    },columns = ['Movie Name','Release Date','Director','Actor 1','Actor 2','No. of Votes','Rating'])
Movie_List.index += 1
Movie_List.index.name = 'Rank'
Movie_List['Release Date'] = pd.to_numeric(Movie_List['Release Date'])

#Saving into a CSV File
Movie_List.to_csv('IMDB_Data.csv', encoding='utf-8')
