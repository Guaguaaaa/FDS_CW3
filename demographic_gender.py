import numpy as np
import re

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression


dtypes = {
    'Year of event': 'int64',
    'Event dates': object,  # there are 00.00.1995, or 05.-07.01.2018
    'Event name': object,
    'Event distance/length': object,
    'Event number of finishers': 'int64',
    'Athlete performance': object,
    'Athlete club': object,
    'Athlete country': object,
    'Athlete year of birth': 'float64',  # contains 1978.0 (always .0)
    'Athlete gender': object,  # Gender: F or M or X
    'Athlete age category': object,
    'Athlete average speed': object,  # has data like '18:00:00' in it.
    'Athlete ID': 'int64'
}

# read file
df = pd.read_csv("TWO_CENTURIES_OF_UM_RACES.csv", dtype=dtypes)


def duration_to_hours(duration_str):
    var = 0
    values = ""
    if "d" in duration_str:
        temp = duration_str.split()
        var += int(temp[0][:-1]) * 24
        values = duration_str.split()[1]
    else:
        values = duration_str.split()[0]

    splitbypoint = values.split(":")
    var += int(splitbypoint[0]) + int(splitbypoint[1]) / 60 + int(splitbypoint[2]) / 3600

    return var


var_50km = df[df['Event distance/length'] == '50km']
var_100km = df[df['Event distance/length'] == '100km']
var_50mi = df[df['Event distance/length'] == '50mi']
var_100mi = df[df['Event distance/length'] == '100mi']

mask = var_50km['Athlete performance'].notna()
var_50km = var_50km[mask]
mask = var_100km['Athlete performance'].notna()
var_100km = var_100km[mask]
mask = var_50mi['Athlete performance'].notna()
var_50mi = var_50mi[mask]
mask = var_100mi['Athlete performance'].notna()
var_100mi = var_100mi[mask]

var_50km['Athlete performance'] = var_50km['Athlete performance'].apply(duration_to_hours)
var_100km['Athlete performance'] = var_100km['Athlete performance'].apply(duration_to_hours)
var_50mi['Athlete performance'] = var_50mi['Athlete performance'].apply(duration_to_hours)
var_100mi['Athlete performance'] = var_100mi['Athlete performance'].apply(duration_to_hours)

var_50km = var_50km[var_50km['Athlete gender'].isin(['F', 'M'])]
var_100km = var_100km[var_100km['Athlete gender'].isin(['F', 'M'])]
var_50mi = var_50mi[var_50mi['Athlete gender'].isin(['F', 'M'])]
var_100mi = var_100mi[var_100mi['Athlete gender'].isin(['F', 'M'])]

fig, axs = plt.subplots(2, 2, figsize=(12, 10))

female_data = var_50km[var_50km['Athlete gender'] == 'F']
female_avg_performance = female_data.groupby('Year of event')['Athlete performance'].mean()

X_female = female_avg_performance.index.values.reshape(-1, 1)
y_female = female_avg_performance.values.reshape(-1, 1)
reg_female = LinearRegression().fit(X_female, y_female)
reg_line_female = reg_female.predict(X_female)

male_data = var_50km[var_50km['Athlete gender'] == 'M']
male_avg_performance = male_data.groupby('Year of event')['Athlete performance'].mean()

X_male = male_avg_performance.index.values.reshape(-1, 1)
y_male = male_avg_performance.values.reshape(-1, 1)
reg_male = LinearRegression().fit(X_male, y_male)
reg_line_male = reg_male.predict(X_male)

axs[0, 0].plot(female_avg_performance.index, female_avg_performance.values, label='Female', marker='o')
axs[0, 0].plot(X_female, reg_line_female, color='blue', linestyle='--', label='Female Regression')
axs[0, 0].plot(male_avg_performance.index, male_avg_performance.values, label='Male', marker='o')
axs[0, 0].plot(X_male, reg_line_male, color='orange', linestyle='--', label='Male Regression')

axs[0, 0].set_xlabel('Year of Event')
axs[0, 0].set_ylabel('Average Athlete Performance (hours)')
axs[0, 0].set_title('Average Athlete Performance Over Years for 50km')

axs[0, 0].legend()

plt.tight_layout()
plt.show()