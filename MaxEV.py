# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 20:35:30 2018

@author: 
"""

import csv
with open('Z74.SI.csv') as Singtel,open('D05.SI.csv') as DBS,open('O39.SI.csv') as OCBC, \
     open('C31.SI.csv') as Capitaland,open('C6L.SI.csv') as SIA,open('BN4.SI.csv') as Keppel,open('T39.SI.csv') as SPH, \
     open('C52.SI.csv') as ComfortDelgro,open('C09.SI.csv') as CityDevelopment,open('U96.SI.csv') as Sembcorp:

    portfolio={
        'Singtel':list(csv.DictReader(Singtel)),
        'DBS':list(csv.DictReader(DBS)),
        'OCBC':list(csv.DictReader(OCBC)),
        'Capitaland':list(csv.DictReader(Capitaland)),
        'SIA':list(csv.DictReader(SIA)),
        'Keppel':list(csv.DictReader(Keppel)),
        'SPH':list(csv.DictReader(SPH)),
        'ComfortDelgro':list(csv.DictReader(ComfortDelgro)),
        'CityDevelopment':list(csv.DictReader(CityDevelopment)),
        'Sembcorp':list(csv.DictReader(Sembcorp))
    }

    price={}
    for k,v in portfolio.items():
        price[k]=[]
        for i in range(len(v)):
            if v[i]['Adj Close'] == 'null':
                price[k].append(0)
            else:
                price[k].append(float(v[i]['Adj Close']))
    
    dailyreturn={}
    for k,v in price.items():
        dailyreturn[k]=[]
        for i in range(len(v)-1):
            if v[i] != 0:
                dailyreturn[k].append(v[i+1]/v[i] -1)
    
    meanreturn={}
    for k,v in dailyreturn.items():
        meanreturn[k]=0
        for i in range(len(v)):
            meanreturn[k] += v[i]
        meanreturn[k]=meanreturn[k]/len(v)
    
ER = list(meanreturn.values())

print(ER)

W = [0 for n in range(len(ER))]

for i in range(0,len(ER)):
    if ER[i] == max(ER):
        W[i] = 1
    else:
        W[i] = 0

print (W)