# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 10:15:14 2020

@author: Anton
"""
import ast
import pandas as pd
import numpy as np
filepath = r"C:\Users\Anton\AppData\Local\Flashbook\borders\Norwegian - An Essential Grammar_borders.pkl"

df = pd.read_pickle(filepath)
df = df.replace({np.nan: None})
for index in range(len(df)):
    line = df.iloc[index]
    
    print(line)
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