import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

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


# Filter the DataFrame to keep only the rows where 'Year of the Event' is >= 1955
df = df[df['Year of event'] >= 1960]


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

var_50km_club = var_50km.dropna(subset=['Athlete club'])
var_50km_without = var_50km[var_50km['Athlete club'].isnull()]

var_100km_club = var_100km.dropna(subset=['Athlete club'])
var_100km_without = var_100km[var_100km['Athlete club'].isnull()]

var_50mi_club = var_50mi.dropna(subset=['Athlete club'])
var_50mi_without = var_50mi[var_50mi['Athlete club'].isnull()]

var_100mi_club = var_100mi.dropna(subset=['Athlete club'])
var_100mi_without = var_100mi[var_100mi['Athlete club'].isnull()]

# Assuming var_50km_club is already defined and includes 'Year of event' and 'Athlete performance'
# Calculate the average performance

average_performance_50km = var_50km_club.groupby('Year of event')['Athlete performance'].mean().reset_index()
average_performance_50km_without = var_50km_without.groupby('Year of event')['Athlete performance'].mean().reset_index()

# Calculate the average performance for 100km events
average_performance_100km = var_100km_club.groupby('Year of event')['Athlete performance'].mean().reset_index()
average_performance_100km_without = var_100km_without.groupby('Year of event')['Athlete performance'].mean().reset_index()

# Calculate the average performance for 50mi events
average_performance_50mi = var_50mi_club.groupby('Year of event')['Athlete performance'].mean().reset_index()
average_performance_50mi_without = var_50mi_without.groupby('Year of event')['Athlete performance'].mean().reset_index()

# Calculate the average performance for 100mi events
average_performance_100mi = var_100mi_club.groupby('Year of event')['Athlete performance'].mean().reset_index()
average_performance_100mi_without = var_100mi_without.groupby('Year of event')['Athlete performance'].mean().reset_index()


# First, let's create the 2x2 subplot structure
fig, axs = plt.subplots(2, 2, figsize=(15, 10))  # 2x2 subplot

# Calculate linear regression for the first dataset
slope1, intercept1, _, _, _ = linregress(average_performance_50km['Year of event'], average_performance_50km['Athlete performance'])
regression_line1 = slope1 * average_performance_50km['Year of event'] + intercept1

# Calculate linear regression for the second dataset
slope2, intercept2, _, _, _ = linregress(average_performance_50km_without['Year of event'], average_performance_50km_without['Athlete performance'])
regression_line2 = slope2 * average_performance_50km_without['Year of event'] + intercept2

# Plotting on the [0, 0] subplot
# Scatter plot for the first dataset
axs[0, 0].scatter(average_performance_50km['Year of event'], average_performance_50km['Athlete performance'], color='blue', label='50km Club')
# Regression line for the first dataset
axs[0, 0].plot(average_performance_50km['Year of event'], regression_line1, color='blue', linestyle='--', label='Regression Line 50km club')
# Scatter plot for the second dataset
axs[0, 0].scatter(average_performance_50km_without['Year of event'], average_performance_50km_without['Athlete performance'], color='orange', label='50km without club')
# Regression line for the second dataset
axs[0, 0].plot(average_performance_50km_without['Year of event'], regression_line2, color='orange', linestyle='--', label='Regression Line 50km Without Club')
# Setting the title and labels
axs[0, 0].set_title('50km: Club vs No club')
axs[0, 0].set_xlabel('Year of Event')
axs[0, 0].set_ylabel('Average Performance')
axs[0, 0].legend()

# 100km

slope_100km, intercept_100km, _, _, _ = linregress(average_performance_100km['Year of event'], average_performance_100km['Athlete performance'])
regression_line_100km = slope_100km * average_performance_100km['Year of event'] + intercept_100km

# Calculate linear regression for 100km without club
slope_100km_without, intercept_100km_without, _, _, _ = linregress(average_performance_100km_without['Year of event'], average_performance_100km_without['Athlete performance'])
regression_line_100km_without = slope_100km_without * average_performance_100km_without['Year of event'] + intercept_100km_without

# Plotting on the [0, 1] subplot for 100km
# Scatter plot for 100km with club
axs[0, 1].scatter(average_performance_100km['Year of event'], average_performance_100km['Athlete performance'], color='blue', label='100km Club')
# Regression line for 100km with club
axs[0, 1].plot(average_performance_100km['Year of event'], regression_line_100km, color='blue', linestyle='--', label='Regression Line 100km Club')

# Scatter plot for 100km without club
axs[0, 1].scatter(average_performance_100km_without['Year of event'], average_performance_100km_without['Athlete performance'], color='orange', label='100km Without Club')
# Regression line for 100km without club
axs[0, 1].plot(average_performance_100km_without['Year of event'], regression_line_100km_without, color='orange', linestyle='--', label='Regression Line 100km Without Club')
# Setting the title and labels for the 100km subplot
axs[0, 1].set_title('100km: Club vs. No Club')
axs[0, 1].set_xlabel('Year of Event')
axs[0, 1].set_ylabel('Average Performance')
axs[0, 1].legend()

#50miles
slope_50mi, intercept_50mi, _, _, _ = linregress(average_performance_50mi['Year of event'], average_performance_50mi['Athlete performance'])
regression_line_50mi = slope_50mi * average_performance_50mi['Year of event'] + intercept_50mi

# Calculate linear regression for 50mi without club
slope_50mi_without, intercept_50mi_without, _, _, _ = linregress(average_performance_50mi_without['Year of event'], average_performance_50mi_without['Athlete performance'])
regression_line_50mi_without = slope_50mi_without * average_performance_50mi_without['Year of event'] + intercept_50mi_without

# Plotting on the [1, 0] subplot for 50mi
axs[1, 0].scatter(average_performance_50mi['Year of event'], average_performance_50mi['Athlete performance'], color='blue', label='50mi Club')
axs[1, 0].plot(average_performance_50mi['Year of event'], regression_line_50mi, color='blue', linestyle='--', label='Regression Line 50mi Club')
axs[1, 0].scatter(average_performance_50mi_without['Year of event'], average_performance_50mi_without['Athlete performance'], color='orange', label='50mi Without Club')
axs[1, 0].plot(average_performance_50mi_without['Year of event'], regression_line_50mi_without, color='orange', linestyle='--', label='Regression Line 50mi Without Club')
axs[1, 0].set_title('50mi: Club vs. No Club')
axs[1, 0].set_xlabel('Year of Event')
axs[1, 0].set_ylabel('Average Performance')
axs[1, 0].legend()

# Assuming you have similar DataFrames for 100mi events and repeating the process...
# Calculate linear regression for 100mi with club
slope_100mi, intercept_100mi, _, _, _ = linregress(average_performance_100mi['Year of event'], average_performance_100mi['Athlete performance'])
regression_line_100mi = slope_100mi * average_performance_100mi['Year of event'] + intercept_100mi

# Calculate linear regression for 100mi without club
slope_100mi_without, intercept_100mi_without, _, _, _ = linregress(average_performance_100mi_without['Year of event'], average_performance_100mi_without['Athlete performance'])
regression_line_100mi_without = slope_100mi_without * average_performance_100mi_without['Year of event'] + intercept_100mi_without

# Plotting on the [1, 1] subplot for 100mi
axs[1, 1].scatter(average_performance_100mi['Year of event'], average_performance_100mi['Athlete performance'], color='blue', label='100mi Club')
axs[1, 1].plot(average_performance_100mi['Year of event'], regression_line_100mi, color='blue', linestyle='--', label='Regression Line 100mi Club')
axs[1, 1].scatter(average_performance_100mi_without['Year of event'], average_performance_100mi_without['Athlete performance'], color='orange', label='100mi Without Club')
axs[1, 1].plot(average_performance_100mi_without['Year of event'], regression_line_100mi_without, color='orange', linestyle='--', label='Regression Line 100mi Without Club')
axs[1, 1].set_title('100mi: Club vs. No Club')
axs[1, 1].set_xlabel('Year of Event')
axs[1, 1].set_ylabel('Average Performance')
axs[1, 1].legend()

# Adjust layout
plt.tight_layout()

# Display the plot
plt.show()