# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 10:15:14 2020

@author: Anton
"""
import ast
import pandas as pd
import numpy as np
filepath = r"C:\Users\Anton\AppData\Local\Flashbook\Borders\Java for Dummies (2018)_borders.pkl"

df = pd.read_pickle(filepath)
df = df.replace({np.nan: None})
for index in range(len(df)):
    line = df.iloc[index]
    
    print(line)
    print()
    """
    
    #all these try except statements happen because when a file is correctly pickled literal_eval will throw an error, this is just for an old file
    try:
        line['question'] = ast.literal_eval(line['question'])
    except ValueError:
        question = line['question']
    if line['answer']:
        try:
            line['answer'] = ast.literal_eval(line['answer'])
            
        except ValueError:
            answer = line['answer']
            print(line)
    else:
        line['answer'] = None
        
    topic = line['topic']
    try:
        line['size'] = ast.literal_eval(line['size'])
    except ValueError:
        size = line['size']
    """
    #df.iloc[index] = line
    
#df.to_pickle(filepath)
#%%
    
pagenumber = 10

#if pagenumber in df['page']:
p = df['page']
pages_used = set(p)
a_list = set(df['page'])

given_value = pagenumber
difference_function = lambda list_value : abs(given_value - list_value)
closest_value = min(a_list, key=difference_function)    
if closest_value > pagenumber:
    closest_index = p.where(p==closest_value).first_valid_index() - 0.5
else:
    closest_index = p.where(p==closest_value).last_valid_index() + 0.5
    
closest_index = -0.5
    



index = closest_index
print("tst  "*20)
print(df['page'])
df2 = df.copy()
line = {'page': 1, 'id': 'Kl8W', 'question': {'text': '123'}, 'size': [(87, 50), (0, 0), (0, 0), (0, 0), (0, 0)], 'relsize': 100}


print(f"type = {type(line)}")
dfline = pd.DataFrame( index=[closest_index])
for key, value in line.items():
    print(key)
    dfline[key] = [value]

#%%
print(f"dfline = {type(line)}")
df3 = df2.append(dfline, ignore_index=False,sort = False)

df3 = df3.sort_index().reset_index(drop=True)

print(pagenumber ,"/",closest_value)
print("test")
replacedata = {}
print(f"df3 = {type(df3)}")
indices = df['page'].where(df['page']==10)
indices = [bool(x) for x in indices]

df.drop