import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


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

var_50km = var_50km[var_50km['Athlete gender'].isin(['F', 'M'])]
var_100km = var_100km[var_100km['Athlete gender'].isin(['F', 'M'])]
var_50mi = var_50mi[var_50mi['Athlete gender'].isin(['F', 'M'])]
var_100mi = var_100mi[var_100mi['Athlete gender'].isin(['F', 'M'])]

fig, axs = plt.subplots(2, 2, figsize=(12, 10))

female_data_50km = var_50km[var_50km['Athlete gender'] == 'F']
female_avg_performance_50km = female_data_50km.groupby('Year of event')['Athlete performance'].mean()

X_female_50km = female_avg_performance_50km.index.values.reshape(-1, 1)
y_female_50km = female_avg_performance_50km.values.reshape(-1, 1)
reg_female_50km = LinearRegression().fit(X_female_50km, y_female_50km)
reg_line_female_50km = reg_female_50km.predict(X_female_50km)

male_data_50km = var_50km[var_50km['Athlete gender'] == 'M']
male_avg_performance_50km = male_data_50km.groupby('Year of event')['Athlete performance'].mean()

X_male_50km = male_avg_performance_50km.index.values.reshape(-1, 1)
y_male_50km = male_avg_performance_50km.values.reshape(-1, 1)
reg_male_50km = LinearRegression().fit(X_male_50km, y_male_50km)
reg_line_male_50km = reg_male_50km.predict(X_male_50km)

axs[0, 0].plot(female_avg_performance_50km.index, female_avg_performance_50km.values, label='Female', marker='o')
axs[0, 0].plot(X_female_50km, reg_line_female_50km, color='blue', linestyle='--', label='Female Regression')
axs[0, 0].plot(male_avg_performance_50km.index, male_avg_performance_50km.values, label='Male', marker='o')
axs[0, 0].plot(X_male_50km, reg_line_male_50km, color='orange', linestyle='--', label='Male Regression')

axs[0, 0].set_xlabel('Year of Event')
axs[0, 0].set_ylabel('Average Athlete Performance (hours)')
axs[0, 0].set_title('Average Athlete Performance Over Years for 50km')

axs[0, 0].legend()

# 100km
female_data_100km = var_100km[var_100km['Athlete gender'] == 'F']
female_avg_performance_100km = female_data_100km.groupby('Year of event')['Athlete performance'].mean()

X_female_100km = female_avg_performance_100km.index.values.reshape(-1, 1)
y_female_100km = female_avg_performance_100km.values.reshape(-1, 1)
reg_female_100km = LinearRegression().fit(X_female_100km, y_female_100km)
reg_line_female_100km = reg_female_100km.predict(X_female_100km)

male_data_100km = var_100km[var_100km['Athlete gender'] == 'M']
male_avg_performance_100km = male_data_100km.groupby('Year of event')['Athlete performance'].mean()

X_male_100km = male_avg_performance_100km.index.values.reshape(-1, 1)
y_male_100km = male_avg_performance_100km.values.reshape(-1, 1)
reg_male_100km = LinearRegression().fit(X_male_100km, y_male_100km)
reg_line_male_100km = reg_male_100km.predict(X_male_100km)

axs[0, 1].plot(female_avg_performance_100km.index, female_avg_performance_100km.values, label='Female', marker='o')
axs[0, 1].plot(X_female_100km, reg_line_female_100km, color='blue', linestyle='--', label='Female Regression')
axs[0, 1].plot(male_avg_performance_100km.index, male_avg_performance_100km.values, label='Male', marker='o')
axs[0, 1].plot(X_male_100km, reg_line_male_100km, color='orange', linestyle='--', label='Male Regression')

axs[0, 1].set_xlabel('Year of Event')
axs[0, 1].set_ylabel('Average Athlete Performance (hours)')
axs[0, 1].set_title('Average Athlete Performance Over Years for 100km')

axs[0, 1].legend()

# 50mi

female_data_50mi = var_50mi[var_50mi['Athlete gender'] == 'F']
female_avg_performance_50mi = female_data_50mi.groupby('Year of event')['Athlete performance'].mean()

X_female_50mi = female_avg_performance_50mi.index.values.reshape(-1, 1)
y_female_50mi = female_avg_performance_50mi.values.reshape(-1, 1)
reg_female_50mi = LinearRegression().fit(X_female_50mi, y_female_50mi)
reg_line_female_50mi = reg_female_50mi.predict(X_female_50mi)

male_data_50mi = var_50mi[var_50mi['Athlete gender'] == 'M']
male_avg_performance_50mi = male_data_50mi.groupby('Year of event')['Athlete performance'].mean()

X_male_50mi = male_avg_performance_50mi.index.values.reshape(-1, 1)
y_male_50mi = male_avg_performance_50mi.values.reshape(-1, 1)
reg_male_50mi = LinearRegression().fit(X_male_50mi, y_male_50mi)
reg_line_male_50mi = reg_male_50mi.predict(X_male_50mi)

axs[1, 0].plot(female_avg_performance_50mi.index, female_avg_performance_50mi.values, label='Female', marker='o')
axs[1, 0].plot(X_female_50mi, reg_line_female_50mi, color='blue', linestyle='--', label='Female Regression')
axs[1, 0].plot(male_avg_performance_50mi.index, male_avg_performance_50mi.values, label='Male', marker='o')
axs[1, 0].plot(X_male_50mi, reg_line_male_50mi, color='orange', linestyle='--', label='Male Regression')

axs[1, 0].set_xlabel('Year of Event')
axs[1, 0].set_ylabel('Average Athlete Performance (hours)')
axs[1, 0].set_title('Average Athlete Performance Over Years for 50mi')

axs[1, 0].legend()

# 100mi
female_data_100mi = var_100mi[var_100mi['Athlete gender'] == 'F']
female_avg_performance_100mi = female_data_100mi.groupby('Year of event')['Athlete performance'].mean()

X_female_100mi = female_avg_performance_100mi.index.values.reshape(-1, 1)
y_female_100mi = female_avg_performance_100mi.values.reshape(-1, 1)
reg_female_100mi = LinearRegression().fit(X_female_100mi, y_female_100mi)
reg_line_female_100mi = reg_female_100mi.predict(X_female_100mi)

male_data_100mi = var_100mi[var_100mi['Athlete gender'] == 'M']
male_avg_performance_100mi = male_data_100mi.groupby('Year of event')['Athlete performance'].mean()

X_male_100mi = male_avg_performance_100mi.index.values.reshape(-1, 1)
y_male_100mi = male_avg_performance_100mi.values.reshape(-1, 1)
reg_male_100mi = LinearRegression().fit(X_male_100mi, y_male_100mi)
reg_line_male_100mi = reg_male_100mi.predict(X_male_100mi)

axs[1, 1].plot(female_avg_performance_100mi.index, female_avg_performance_100mi.values, label='Female', marker='o')
axs[1, 1].plot(X_female_100mi, reg_line_female_100mi, color='blue', linestyle='--', label='Female Regression')
axs[1, 1].plot(male_avg_performance_100mi.index, male_avg_performance_100mi.values, label='Male', marker='o')
axs[1, 1].plot(X_male_100mi, reg_line_male_100mi, color='orange', linestyle='--', label='Male Regression')

axs[1, 1].set_xlabel('Year of Event')
axs[1, 1].set_ylabel('Average Athlete Performance (hours)')
axs[1, 1].set_title('Average Athlete Performance Over Years for 100mi')

axs[1, 1].legend()

plt.tight_layout()
plt.show()