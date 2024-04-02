import pandas as pd

# Cleaning the data to prepare for the regression model

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


var_50km = df[df['Event distance/length'].isin(['50km', '100km', '50mi', '100mi'])]
mask = var_50km['Athlete performance'].notna()
var_50km = var_50km[mask]
var_50km['Athlete performance'] = var_50km['Athlete performance'].apply(duration_to_hours)
var_50km = var_50km.drop(columns=['Event dates'])
var_50km = var_50km.drop(columns=['Event name'])
var_50km = var_50km.drop(columns=['Athlete country'])
var_50km = var_50km.drop(columns=['Athlete ID'])
var_50km['Athlete club'] = var_50km['Athlete club'].fillna(0)
var_50km['Athlete club'] = var_50km['Athlete club'].apply(lambda x: 1 if x != 0 else 0)
var_50km['Athlete year of birth'] = var_50km['Athlete year of birth'].astype(str).str.replace('.0', '')
var_50km['Athlete year of birth'] = pd.to_numeric(var_50km['Athlete year of birth'], errors='coerce')
var_50km['Athlete year of birth'] = var_50km['Athlete year of birth'].fillna(0).astype(int)
var_50km['Athlete gender'] = var_50km['Athlete gender'].map({'M': 1, 'F': 0})
var_50km = var_50km[var_50km['Athlete gender'].isin([0, 1])]
var_50km['Athlete gender'] = var_50km['Athlete gender'].astype(int)
var_50km.dropna(subset=['Athlete age category'], inplace=True)
age_category_dummies = pd.get_dummies(var_50km['Athlete age category'], prefix='Age_category', dtype=int)
var_50km = pd.concat([var_50km, age_category_dummies], axis=1)
var_50km = var_50km.drop(columns=['Athlete age category'])
var_50km['Athlete average speed'] = pd.to_numeric(var_50km['Athlete average speed'], errors='coerce')
df.dropna(inplace=True)

# Creating new columns based on 'Event distance/length'
var_50km['Event_50km'] = (var_50km['Event distance/length'] == '50km').astype(int)
var_50km['Event_100km'] = (var_50km['Event distance/length'] == '100km').astype(int)
var_50km['Event_50miles'] = (var_50km['Event distance/length'] == '50mi').astype(int)
var_50km['Event_100miles'] = (var_50km['Event distance/length'] == '100mi').astype(int)
var_50km = var_50km.drop(columns=['Event distance/length'])
# Dropping the 'Event distance/length' column

var_50km = var_50km.drop(columns=['Athlete average speed'])

output_file_path = 'modified_csv_file.csv'

var_50km.to_csv(output_file_path, index=False)

