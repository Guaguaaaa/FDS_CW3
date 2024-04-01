import numpy as np
import re

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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

# 路程/速度=时间

# 读取CSV文件
df = pd.read_csv("TWO_CENTURIES_OF_UM_RACES.csv", dtype=dtypes)

"""mi_to_km = 1.60934
var_50km['Finishing Time'] = None  # Initialize the column
var_50km['Athlete average speed'] = var_50km['Athlete average speed'].astype(float)

# df.loc[df['Event distance/length'] == '50 km', 'Finishing Time'] = df.loc[df['Event distance/length'] == '50 km', 'Athlete average speed'].apply(lambda speed: 50 / speed)

# For 100 km dataset
df.loc[df['Event distance/length'] == '100 km', 'Finishing Time'] = df.loc[df['Event distance/length'] == '100 km', 'Athlete average speed'].apply(lambda speed: 100 / speed)

# For 50 mi dataset
df.loc[df['Event distance/length'] == '50 mi', 'Finishing Time'] = df.loc[df['Event distance/length'] == '50 mi', 'Athlete average speed'].apply(lambda speed: 50 * mi_to_km / speed)

# For 100 mi dataset
df.loc[df['Event distance/length'] == '100 mi', 'Finishing Time'] = df.loc[df['Event distance/length'] == '100 mi', 'Athlete average speed'].apply(lambda speed: 100 * mi_to_km / speed)"""

# print(var_50km['Finishing Time'])

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
    '''pattern = r'(\d+)d\s+(\d+):(\d+):(\d+)\s+h'
    match = re.match(pattern, duration_str)

    if match:
        days = int(match.group(1)) if match.group(1) else 0
        hours = int(match.group(2))
        minutes = int(match.group(3))
        seconds = int(match.group(4))

        # Convert to total hours
        total_hours = days * 24 + hours + minutes / 60 + seconds / 3600
        print(total_hours)
        return total_hours
    else:
        # If the pattern doesn't match, try to convert directly to float
        try:
            return float(duration_str)
        except ValueError:
            #print("in none")
            return None'''


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

# var_50km['Athlete performance'] = var_50km['Athlete performance'].astype(str)
var_50km['Athlete performance'] = var_50km['Athlete performance'].apply(duration_to_hours)
var_100km['Athlete performance'] = var_100km['Athlete performance'].apply(duration_to_hours)
var_50mi['Athlete performance'] = var_50mi['Athlete performance'].apply(duration_to_hours)
var_100mi['Athlete performance'] = var_100mi['Athlete performance'].apply(duration_to_hours)

#print(var_50km['Athlete performance'])

average_performance = var_50km.groupby('Year of event')['Athlete performance'].mean().reset_index()
print(average_performance)

plt.figure(figsize=(10, 6))
plt.plot(average_performance['Year of event'], average_performance['Athlete performance'], marker='o', linestyle='-')
#plt.plot(var_50km['Year of event'], var_50km['Athlete performance'], marker='o', linestyle='-')
plt.title('Average Athlete Performance Over Years for 50km')
plt.xlabel('Year of Event')
plt.ylabel('Average Athlete Performance')
plt.grid(True)
plt.show()
'''fig, axs = plt.subplots(2, 2, figsize=(12, 8))

# Plot for '50 km' dataset
axs[0, 0].plot(var_50km['Year of event'], var_50km['Athlete performance'], marker='o', linestyle='-')
axs[0, 0].set_title('50 km')
axs[0, 0].set_xlabel('Year of Event')
axs[0, 0].set_ylabel('Athlete Performance (hours)')

# Plot for '100 km' dataset
axs[0, 1].plot(var_100km['Year of event'], var_100km['Athlete performance'], marker='o', linestyle='-')
axs[0, 1].set_title('100 km')
axs[0, 1].set_xlabel('Year of Event')
axs[0, 1].set_ylabel('Athlete Performance (hours)')

# Plot for '50 mi' dataset
axs[1, 0].plot(var_50mi['Year of event'], var_50mi['Athlete performance'], marker='o', linestyle='-')
axs[1, 0].set_title('50 mi')
axs[1, 0].set_xlabel('Year of Event')
axs[1, 0].set_ylabel('Athlete Performance (hours)')

# Plot for '100 mi' dataset
axs[1, 1].plot(var_100mi['Year of event'], var_100mi['Athlete performance'], marker='o', linestyle='-')
axs[1, 1].set_title('100 mi')
axs[1, 1].set_xlabel('Year of Event')
axs[1, 1].set_ylabel('Athlete Performance (hours)')

# Adjust layout
plt.tight_layout()

# Show plot
plt.show()
'''