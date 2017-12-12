# -*- coding: utf-8 -*-
"""
Kwang
"""

import urllib.request, re, csv
from bs4 import BeautifulSoup
textVersionUrl = 'https://www.cia.gov/Library/publications/the-world-factbook/print/textversion.html'
baseUrl = 'https://www.cia.gov/Library/publications/the-world-factbook/'
html = urllib.request.urlopen(textVersionUrl)
soup = BeautifulSoup (html, "lxml")
code=[]
sublinks=[]
gdp=[]
area=[]
road=[]
rail=[]
rows = zip(code,gdp,area,road,rail) 
for link in soup.find_all('a'):
    if link.has_attr('href'):
        string = link.get('href')
        #grab 2 letter code from countries url
        raw = re.findall(r'/geos\/print_[a-z].+', string)
        if(len(raw)>0):
            sublinks.append(raw[0])
#extract letter code from urls
for string in sublinks:
    code.append(string[-7:-5].upper())
#for every subpages, extract data from the pages
for i in range(0, len(sublinks)):
    testhtml = urllib.request.urlopen(baseUrl+sublinks[i])
    #fetch html of the subpage
    subpage = BeautifulSoup(testhtml, 'lxml')
    #check if the country has road/rail ways
    if(len(re.findall('Roadways:', subpage.text))==0):
        road.append(0)
    if(len(re.findall('Railways:', subpage.text))==0):
        rail.append(0)
    re.findall('Roadways:', subpage.text)
    for div in subpage.find_all('div'):
        if div.text == 'GDP - per capita (PPP):':
            gdpdata = div.find_next('div').text
            #convert string into numberic data                       
            try:
                gdpdata2 = gdpdata.split()
                gdp.append(int("".join(re.findall(r'[0-9]', gdpdata2[0]))))
            except:
                try:
                    gdp.append(int("".join(re.findall(r'[0-9]', gdpdata))))
                except:
                    gdp.append(0)
        #'million' data pendding 
        elif div.text == 'Area:':
            areadata = div.find_next('div').text
            areadata2 = areadata.split()
            try: 
                area.append(int("".join(re.findall(r'[0-9]', areadata2[1]))))
            except:
                area.append(0)
        elif div.text == 'Roadways:':
            roaddata = div.find_next('div').text
            roaddata2 = roaddata.split()
            try: 
                roaddata2.append(int("".join(re.findall(r'[0-9]', roaddata2[1]))))
            except:
                road.append(0)
        elif div.text == 'Railways:':
            raildata = div.find_next('div').text
            raildata2 = raildata.split()
            try: 
                rail.append(int("".join(re.findall(r'[0-9]', raildata2[1]))))
            except:
                rail.append(0)
#write data in csv
with open("cia.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    write = writer.writerow(['Country Code','GDP($)', 'Area(sq km)', 'Length of Roadways(km)', ' Length of Railways(km)'])
    writer = writer.writerows(rows)
        
