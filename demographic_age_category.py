import numpy as np
import re

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression


"""
U23
23-35
35-45
A45
"""

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

# Convert age category column to string type for each dataset
var_50km['Athlete age category'] = var_50km['Athlete age category'].astype(str)
var_100km['Athlete age category'] = var_100km['Athlete age category'].astype(str)
var_50mi['Athlete age category'] = var_50mi['Athlete age category'].astype(str)
var_100mi['Athlete age category'] = var_100mi['Athlete age category'].astype(str)

# Define age category groups
age_groups = {
    'Under 23': ['U20', 'U23', '20'],
    '23 to 40': [str(i) for i in range(23, 40)],
    '40 and above': [str(i) for i in range(40, 100)]
}

# Create subplots
fig, axs = plt.subplots(2, 2, figsize=(15, 10))

datasets = {
    'var_50km': var_50km,
    'var_100km': var_100km,
    'var_50mi': var_50mi,
    'var_100mi': var_100mi
}

for (dataset_name, dataset), ax in zip(datasets.items(), axs.flatten()):
    for age_group, categories in age_groups.items():
        # Filter data for age categories within the current age group
        category_data = dataset[dataset['Athlete age category'].str[1:].isin(categories)]

        # Calculate average performance for each year
        avg_performance = category_data.groupby('Year of event')['Athlete performance'].mean()

        if len(avg_performance) > 0:
            X = avg_performance.index.values.reshape(-1, 1)
            y = avg_performance.values.reshape(-1, 1)
            reg = LinearRegression().fit(X, y)
            reg_line = reg.predict(X)

            # Plot data points and regression line
            ax.plot(avg_performance.index, avg_performance.values, label=age_group, marker='o')
            ax.plot(X, reg_line, linestyle='--')

    # Add legend inside the plot at top-left corner
    ax.legend(loc='upper left', title=None)

    # Set graph title
    ax.set_title(f'{dataset_name}')

    # Set labels
    ax.set_xlabel('Year of Event')
    ax.set_ylabel('Average Athlete Performance (hours)')

# Adjust layout and show plot
plt.tight_layout()
plt.show()