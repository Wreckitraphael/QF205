
# coding: utf-8

# In[28]:


import csv
with open('Z74.SI.csv') as singtel,open('D05.SI.csv') as dbs:
    portfolio={
        'singtel':list(csv.DictReader(singtel)),
        'dbs':list(csv.DictReader(dbs))
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
        

    
    
                
    
        
                    

