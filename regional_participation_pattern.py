import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np


# Define the path to your Excel file
csv_file_path = 'TWO_CENTURIES_OF_UM_RACES.csv'

# Load the Excel file
df = pd.read_csv(csv_file_path)


transformed_data = df[df['Event distance/length'].isin(['50km', '100km', '50 miles', '100 miles'])]
# Drop data that is not relavant
transformed_data = transformed_data.drop(['Athlete club','Athlete age category','Event number of finishers','Athlete gender','Event dates', 'Event name', 'Event distance/length','Athlete performance','Athlete average speed','Athlete ID','Athlete year of birth'], axis=1)

transformed_data = transformed_data.groupby('Year of event')['Athlete country'].nunique().reset_index()

transformed_data.columns = ['Year', 'Number of Countries participated']

# Perform linear regression
slope, intercept, r_value, p_value, std_err = linregress(transformed_data['Year'], transformed_data['Number of Countries participated'])

# Generate a range of years for plotting the linear regression
years_range = np.linspace(transformed_data['Year'].min(), transformed_data['Year'].max(), 200)
linear_values = slope * years_range + intercept

# Plotting the linear regression with data points as a line plot
plt.figure(figsize=(12, 7))

# Linear regression line
plt.plot(years_range, linear_values, color='green', linestyle='-', label='Linear Regression')
# Data as line plot
plt.plot(transformed_data['Year'], transformed_data['Number of Countries participated'], color='darkblue', marker='o', linestyle='-', label='Data as Line')

plt.title('Number of Countries Participated Over Years with Linear Regression')
plt.xlabel('Year')
plt.ylabel('Number of Countries Participated')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

print(f"Equation of the regression line: y = {slope:.4f}x + {intercept:.4f}")
print(f"Coefficient of determination (R^2): {r_value**2:.4f}")


