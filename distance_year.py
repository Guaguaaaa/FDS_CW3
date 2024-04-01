import numpy as np
import re

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress
from sklearn.cluster import KMeans


dtypes = {
    'Year of event': 'int64',
    'Event dates': object,
    'Event name': object,
    'Event distance/length': object,
    'Event number of finishers': 'int64',
    'Athlete performance': object,
    'Athlete club': object,
    'Athlete country': object,
    'Athlete year of birth': 'float64',
    'Athlete gender': object,
    'Athlete age category': object,
    'Athlete average speed': object,
    'Athlete ID': 'int64'
}

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

# Plot
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# 50 km
average_performance_50km = var_50km.groupby('Year of event')['Athlete performance'].mean().reset_index()

# Fit a linear regression model
slope, intercept, _, _, _ = linregress(average_performance_50km['Year of event'], average_performance_50km['Athlete performance'])
regression_line = slope * average_performance_50km['Year of event'] + intercept

# Apply k-means clustering to the data
X = average_performance_50km[['Year of event', 'Athlete performance']]
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X)
cluster_centers = kmeans.cluster_centers_
labels = kmeans.labels_


axs[0, 0].scatter(average_performance_50km['Year of event'], average_performance_50km['Athlete performance'], c=labels, cmap='viridis', label='Data')
axs[0, 0].scatter(cluster_centers[:, 0], cluster_centers[:, 1], marker='X', s=100, color='red', label='Cluster Centers')
axs[0, 0].plot(average_performance_50km['Year of event'], regression_line, color='black', linestyle='-', label='Regression Line')
axs[0, 0].set_title('K-Means Clustering for 50 km')
axs[0, 0].set_xlabel('Year of Event')
axs[0, 0].set_ylabel('Average Athlete Performance')
axs[0, 0].legend()

# 100 km

average_performance_100km = var_100km.groupby('Year of event')['Athlete performance'].mean().reset_index()

# Fit a linear regression model
slope, intercept, _, _, _ = linregress(average_performance_100km['Year of event'], average_performance_100km['Athlete performance'])
regression_line = slope * average_performance_100km['Year of event'] + intercept

# Apply k-means clustering to the data
X = average_performance_100km[['Year of event', 'Athlete performance']]
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X)
cluster_centers = kmeans.cluster_centers_
labels = kmeans.labels_


axs[0, 1].scatter(average_performance_100km['Year of event'], average_performance_100km['Athlete performance'], c=labels, cmap='viridis', label='Data')
axs[0, 1].scatter(cluster_centers[:, 0], cluster_centers[:, 1], marker='X', s=100, color='red', label='Cluster Centers')
axs[0, 1].plot(average_performance_100km['Year of event'], regression_line, color='black', linestyle='-', label='Regression Line')
axs[0, 1].set_title('K-Means Clustering for 100 km')
axs[0, 1].set_xlabel('Year of Event')
axs[0, 1].set_ylabel('Average Athlete Performance')
axs[0, 1].legend()


# 50 mi
average_performance_50mi = var_50mi.groupby('Year of event')['Athlete performance'].mean().reset_index()

# Fit a linear regression model
slope, intercept, _, _, _ = linregress(average_performance_50mi['Year of event'], average_performance_50mi['Athlete performance'])
regression_line = slope * average_performance_50mi['Year of event'] + intercept

# Apply k-means clustering to the data
X = average_performance_50mi[['Year of event', 'Athlete performance']]
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X)
cluster_centers = kmeans.cluster_centers_
labels = kmeans.labels_


axs[1, 0].scatter(average_performance_50mi['Year of event'], average_performance_50mi['Athlete performance'], c=labels, cmap='viridis', label='Data')
axs[1, 0].scatter(cluster_centers[:, 0], cluster_centers[:, 1], marker='X', s=100, color='red', label='Cluster Centers')
axs[1, 0].plot(average_performance_50mi['Year of event'], regression_line, color='black', linestyle='-', label='Regression Line')
axs[1, 0].set_title('K-Means Clustering for 50 mi')
axs[1, 0].set_xlabel('Year of Event')
axs[1, 0].set_ylabel('Average Athlete Performance')
axs[1, 0].legend()

# 100 mi
average_performance_100mi = var_100mi.groupby('Year of event')['Athlete performance'].mean().reset_index()

# Fit a linear regression model
slope, intercept, _, _, _ = linregress(average_performance_100mi['Year of event'], average_performance_100mi['Athlete performance'])
regression_line = slope * average_performance_100mi['Year of event'] + intercept

# Apply k-means clustering to the data
X = average_performance_100mi[['Year of event', 'Athlete performance']]
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X)
cluster_centers = kmeans.cluster_centers_
labels = kmeans.labels_


axs[1, 1].scatter(average_performance_100mi['Year of event'], average_performance_100mi['Athlete performance'], c=labels, cmap='viridis', label='Data')
axs[1, 1].scatter(cluster_centers[:, 0], cluster_centers[:, 1], marker='X', s=100, color='red', label='Cluster Centers')
axs[1, 1].plot(average_performance_100mi['Year of event'], regression_line, color='black', linestyle='-', label='Regression Line')
axs[1, 1].set_title('K-Means Clustering for 100 mi')
axs[1, 1].set_xlabel('Year of Event')
axs[1, 1].set_ylabel('Average Athlete Performance')
axs[1, 1].legend()

plt.tight_layout()
plt.show()