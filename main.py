import numpy as np

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

# 读取CSV文件
df = pd.read_csv("TWO_CENTURIES_OF_UM_RACES.csv", dtype=dtypes)

# change date
df['Event dates'] = pd.to_datetime(df['Event dates'], errors='coerce', format='%d.%m.%Y', dayfirst=True)

# clean 'Athlete year of birth' data, convert to int type (all 4 digit int of year)
df['Athlete year of birth'] = df['Athlete year of birth'].astype(str).str.replace('.0', '')
# df['Athlete year of birth'] = df['Athlete year of birth'].astype(int)
df['Athlete year of birth'] = pd.to_numeric(df['Athlete year of birth'], errors='coerce').astype('Int64')


# delete exceptions in date
# df = df.dropna(subset=['Event dates'])

# convert time to seconds
# df['Athlete performance'] = pd.to_timedelta(df['Athlete performance']).dt.total_seconds() / 3600

# participles and year
plt.figure(figsize=(10, 6))
sns.lineplot(data=df.groupby('Year of event')['Event number of finishers'].sum())
plt.title('Number of Finishers Over Years')
plt.xlabel('Year')
plt.ylabel('Number of Finishers')
plt.show()
