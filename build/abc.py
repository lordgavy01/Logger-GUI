import pandas as pd
import json


log_data=open('Warehouse.log','r')
input()
result={}
i=0
for line in log_data:
    columns=line.split(',')
    data=[]
    for c in columns:
        if len(data)==0:
            c=c[11:]
        if len(data)==1:
            c=c[4:]
        data.append(c)
    # print(data)

