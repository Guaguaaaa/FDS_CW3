import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress


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

var_50km['Event name'] = var_50km['Event name'].str[-4:-1]
var_100km['Event name'] = var_100km['Event name'].str[-4:-1]
var_50mi['Event name'] = var_50mi['Event name'].str[-4:-1]
var_100mi['Event name'] = var_100mi['Event name'].str[-4:-1]

var_50km['Event name'] = var_50km['Event name'].astype(str)
var_50km['Athlete country'] = var_50km['Athlete country'].astype(str)


consistent_values_50km = var_50km[var_50km['Event name'] == var_50km['Athlete country']]
inconsistent_values_50km = var_50km[var_50km['Event name'] != var_50km['Athlete country']]

avg_performance_per_year_consistent_50km = consistent_values_50km.groupby('Year of event')['Athlete performance'].mean()

avg_performance_per_year_inconsistent_50km = inconsistent_values_50km.groupby('Year of event')['Athlete performance'].mean()

fig, axs = plt.subplots(2, 2, figsize=(12, 10))
axs[0, 0].plot(avg_performance_per_year_consistent_50km.index, avg_performance_per_year_consistent_50km.values, label='Consistent Athlete performance', color='blue')
axs[0, 0].plot(avg_performance_per_year_inconsistent_50km.index, avg_performance_per_year_inconsistent_50km.values, label='Inconsistent Athlete performance', color='red')

slope_consistent_50km, intercept_consistent_50km, _, _, _ = linregress(avg_performance_per_year_consistent_50km.index, avg_performance_per_year_consistent_50km.values)
slope_inconsistent_50km, intercept_inconsistent_50km, _, _, _ = linregress(avg_performance_per_year_inconsistent_50km.index, avg_performance_per_year_inconsistent_50km.values)

axs[0, 0].plot(avg_performance_per_year_consistent_50km.index, slope_consistent_50km * avg_performance_per_year_consistent_50km.index + intercept_consistent_50km, color='blue', linestyle='--', label='Regression Line (Consistent)')
axs[0, 0].plot(avg_performance_per_year_inconsistent_50km.index, slope_inconsistent_50km * avg_performance_per_year_inconsistent_50km.index + intercept_inconsistent_50km, color='red', linestyle='--', label='Regression Line (Inconsistent)')

axs[0, 0].set_xlabel('Year of event')
axs[0, 0].set_ylabel('Average Athlete performance')
axs[0, 0].set_title('Average Athlete performance per Year (100km)')
axs[0, 0].legend()

# 100km
consistent_values_100km = var_100km[var_100km['Event name'] == var_100km['Athlete country']]
inconsistent_values_100km = var_100km[var_100km['Event name'] != var_100km['Athlete country']]

avg_performance_per_year_consistent_100km = consistent_values_100km.groupby('Year of event')['Athlete performance'].mean()
avg_performance_per_year_inconsistent_100km = inconsistent_values_100km.groupby('Year of event')['Athlete performance'].mean()

axs[0, 1].plot(avg_performance_per_year_consistent_100km.index, avg_performance_per_year_consistent_100km.values, label='Consistent Athlete performance', color='blue')
axs[0, 1].plot(avg_performance_per_year_inconsistent_100km.index, avg_performance_per_year_inconsistent_100km.values, label='Inconsistent Athlete performance', color='red')

slope_consistent_100km, intercept_consistent_100km, _, _, _ = linregress(avg_performance_per_year_consistent_100km.index, avg_performance_per_year_consistent_100km.values)
slope_inconsistent_100km, intercept_inconsistent_100km, _, _, _ = linregress(avg_performance_per_year_inconsistent_100km.index, avg_performance_per_year_inconsistent_100km.values)

axs[0, 1].plot(avg_performance_per_year_consistent_100km.index, slope_consistent_100km * avg_performance_per_year_consistent_100km.index + intercept_consistent_100km, color='blue', linestyle='--', label='Regression Line (Consistent)')
axs[0, 1].plot(avg_performance_per_year_inconsistent_100km.index, slope_inconsistent_100km * avg_performance_per_year_inconsistent_100km.index + intercept_inconsistent_100km, color='red', linestyle='--', label='Regression Line (Inconsistent)')

axs[0, 1].set_xlabel('Year of event')
axs[0, 1].set_ylabel('Average Athlete performance')
axs[0, 1].set_title('Average Athlete performance per Year (100km)')
axs[0, 1].legend()


# 50mi
consistent_values_50mi = var_50mi[var_50mi['Event name'] == var_50mi['Athlete country']]
inconsistent_values_50mi = var_50mi[var_50mi['Event name'] != var_50mi['Athlete country']]

avg_performance_per_year_consistent_50mi = consistent_values_50mi.groupby('Year of event')['Athlete performance'].mean()
avg_performance_per_year_inconsistent_50mi = inconsistent_values_50mi.groupby('Year of event')['Athlete performance'].mean()

axs[1, 0].plot(avg_performance_per_year_consistent_50mi.index, avg_performance_per_year_consistent_50mi.values, label='Consistent Athlete performance', color='blue')
axs[1, 0].plot(avg_performance_per_year_inconsistent_50mi.index, avg_performance_per_year_inconsistent_50mi.values, label='Inconsistent Athlete performance', color='red')

slope_consistent_50mi, intercept_consistent_50mi, _, _, _ = linregress(avg_performance_per_year_consistent_50mi.index, avg_performance_per_year_consistent_50mi.values)
slope_inconsistent_50mi, intercept_inconsistent_50mi, _, _, _ = linregress(avg_performance_per_year_inconsistent_50mi.index, avg_performance_per_year_inconsistent_50mi.values)

axs[1, 0].plot(avg_performance_per_year_consistent_50mi.index, slope_consistent_50mi * avg_performance_per_year_consistent_50mi.index + intercept_consistent_50mi, color='blue', linestyle='--', label='Regression Line (Consistent)')
axs[1, 0].plot(avg_performance_per_year_inconsistent_50mi.index, slope_inconsistent_50mi * avg_performance_per_year_inconsistent_50mi.index + intercept_inconsistent_50mi, color='red', linestyle='--', label='Regression Line (Inconsistent)')

axs[1, 0].set_xlabel('Year of event')
axs[1, 0].set_ylabel('Average Athlete performance')
axs[1, 0].set_title('Average Athlete performance per Year (50mi)')
axs[1, 0].legend()

# 100mi
consistent_values_100mi = var_100mi[var_100mi['Event name'] == var_100mi['Athlete country']]
inconsistent_values_100mi = var_100mi[var_100mi['Event name'] != var_100mi['Athlete country']]

avg_performance_per_year_consistent_100mi = consistent_values_100mi.groupby('Year of event')['Athlete performance'].mean()
avg_performance_per_year_inconsistent_100mi = inconsistent_values_100mi.groupby('Year of event')['Athlete performance'].mean()

axs[1, 1].plot(avg_performance_per_year_consistent_100mi.index, avg_performance_per_year_consistent_100mi.values, label='Consistent Athlete performance', color='blue')
axs[1, 1].plot(avg_performance_per_year_inconsistent_100mi.index, avg_performance_per_year_inconsistent_100mi.values, label='Inconsistent Athlete performance', color='red')

slope_consistent_100mi, intercept_consistent_100mi, _, _, _ = linregress(avg_performance_per_year_consistent_100mi.index, avg_performance_per_year_consistent_100mi.values)
slope_inconsistent_100mi, intercept_inconsistent_100mi, _, _, _ = linregress(avg_performance_per_year_inconsistent_100mi.index, avg_performance_per_year_inconsistent_100mi.values)

axs[1, 1].plot(avg_performance_per_year_consistent_100mi.index, slope_consistent_100mi * avg_performance_per_year_consistent_100mi.index + intercept_consistent_100mi, color='blue', linestyle='--', label='Regression Line (Consistent)')
axs[1, 1].plot(avg_performance_per_year_inconsistent_100mi.index, slope_inconsistent_100mi * avg_performance_per_year_inconsistent_100mi.index + intercept_inconsistent_100mi, color='red', linestyle='--', label='Regression Line (Inconsistent)')

axs[1, 1].set_xlabel('Year of event')
axs[1, 1].set_ylabel('Average Athlete performance')
axs[1, 1].set_title('Average Athlete performance per Year (100mi)')
axs[1, 1].legend()

plt.tight_layout()
plt.show()
