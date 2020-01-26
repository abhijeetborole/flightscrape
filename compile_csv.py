import pandas as pd
import glob, os
import os
import itertools
fold=os.getcwd()
folder=os.listdir(fold)
results = pd.DataFrame([])
L = list(itertools.repeat("a", 20))
i=0
for f in folder:
    if f.startswith('flights') and f!='flights.py':
        i+=1
        namedf = pd.read_excel(f,usecols=[1,2,3,4,5,6])
        a=f[7:10]
        b=f[11:14]
        c=f[14:22]
        d=f[23:31]
        namedf['from']=a
        namedf['to']=b
        namedf['date of flight']=c
        namedf['scrape date']=d
        results = results.append(namedf)
        print(i)
results = results.dropna(axis=0, subset=['price'])
results.to_csv("prices_"+d+".txt")        



