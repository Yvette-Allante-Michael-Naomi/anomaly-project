#!/usr/bin/env python
# coding: utf-8

# In[1]:


import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt

import os
import numpy as np
import pandas as pd
import seaborn as sns
import env


# In[2]:


def get_clean_log_data():
    '''
    This function acquires data, renames and 
    replaces values for readability, and drops
    values that aren't used or are null.
    A csv is created at the end.
    '''
    url = f'mysql+pymysql://{env.user}:{env.password}@{env.host}/curriculum_logs'
    query = '''
    SELECT *
    FROM logs
    LEFT JOIN cohorts ON cohorts.id= logs.cohort_id
    '''
    df = pd.read_sql(query, url)

    df.date = pd.to_datetime(df.date)
    df = df.set_index(df.date)
    pages = df['path'].resample('d').count()

    df['program_name']= df.program_id

    df.program_name = df.program_name.replace({1.0:'full_stack_php',2.0:'full_stack_java',3.0:'data_science',4.0:'front_end'})

    df = df[df.name != 'Staff']
    

    df.to_csv('curriculum_logs_edited.csv', index=False)
    
    return df


# In[3]:


def wrangle_log_data():
    '''
    This function checks if curriculum_logs_edited.csv exists.
    If it doesn't, it runs a function that pulls data from 
    a sql database and clean the data. Then a csv is made.
    '''
    
    filename = "curriculum_logs_edited.csv"

    if os.path.isfile(filename):
        df = pd.read_csv(filename)
    else:
        df = get_clean_log_data()

    return df

