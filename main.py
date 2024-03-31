import numpy as np

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


"""
在Athlete average speed中存在"18:00:00"格式。推测为24小时耐力赛中比赛结束时间而非平均速度
Note: XX小时耐力赛规则可能为直至最后一人倒下退出为比赛结束
数据出错大概率均为"Le Dernier Homme Debout - Andenne (BEL)"比赛
"""

# TODO 1: 找到 event number of finishers和athlete performance 的历史(year/date)趋势
# TODO 2: 分析 distance/length 和 event number of finisher 导致的 performance(完赛时间)变化
# TODO 3: 预测未来 ultra-marathon 完赛时间的模型开发

"""
问event number of finishers 是否与不同年同比赛相关
问athlete performance 是否只与不同年同比赛/同类型比赛/同时间或距离相关
"""

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
    'Athlete average speed': object,  # has data like '18:00:00' in it.
    'Athlete ID': 'int64'
}

# 读取CSV文件
df = pd.read_csv("TWO_CENTURIES_OF_UM_RACES.csv", dtype=dtypes)

# change date
df['Event dates'] = pd.to_datetime(df['Event dates'], errors='coerce', format='%d.%m.%Y', dayfirst=True)


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
