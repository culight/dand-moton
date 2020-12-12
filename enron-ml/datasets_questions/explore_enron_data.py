#!/usr/bin/python

"""
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000

"""

import pickle
import pandas as pd

enron_data = pickle.load(open("../final_project/final_project_dataset.pkl", "rb"))
enron_df = pd.DataFrame(enron_data)

poi_list = [i for i in list(enron_df.columns) if enron_df[i]['poi'] == 1]
len(poi_list)
poi_list

def count_poi_names():
    i = 0
    with open('../final_project/poi_names.txt', 'r') as f:
        contents = f.readlines()
        for line in contents:
            if line[0] == '(':
                i+=1
    print(i)
count_poi_names()

enron_df['SKILLING JEFFREY K']['total_payments']
enron_df['LAY KENNETH L']['total_payments']
enron_df['FASTOW ANDREW S']['total_payments']

enron_df
enron_df.describe()
import numpy as np

nan_list = [i for i in list(enron_df.columns) if enron_df[i]['poi'] == 1]

import re
EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

no_salary = [i for i in list(enron_df.columns) if enron_df[i]['salary'] == 'NaN']
len(no_salary)
no_email = [i for i in list(enron_df.columns) if re.match(EMAIL_REGEX, enron_df[i]['email_address'])]
len(no_email)

no_total_payments = [i for i in list(enron_df.columns) if enron_df[i]['total_payments'] == 'NaN']
len(no_total_payments)/len(enron_df.columns)
len(no_total_payments)

[enron_df[i] for i in list(enron_df[poi_list])]
poi_no_total_payments = [enron_df[i] for i in list(enron_df[poi_list]) if enron_df[i]['total_payments'] == 'NaN']
len(poi_no_total_payments)

len(enron_df.columns)
