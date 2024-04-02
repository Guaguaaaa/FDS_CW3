import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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

# change date
df['Event dates'] = pd.to_datetime(df['Event dates'], errors='coerce', format='%d.%m.%Y', dayfirst=True)

df['Athlete year of birth'] = df['Athlete year of birth'].astype(str).str.replace('.0', '')
df['Athlete year of birth'] = pd.to_numeric(df['Athlete year of birth'], errors='coerce').astype('Int64')

# participles and year
plt.figure(figsize=(10, 6))
sns.lineplot(data=df.groupby('Year of event')['Event number of finishers'].sum())
plt.title('Number of Finishers Over Years')
plt.xlabel('Year')
plt.ylabel('Number of Finishers')
plt.show()
