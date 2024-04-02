import pandas as pd
from sklearn.linear_model import LinearRegression

csv_file_path = 'modified_csv_file.csv'
df = pd.read_csv(csv_file_path)
X = df.drop(columns=['Athlete performance']).to_numpy(copy=True)
y = df['Athlete performance'].to_numpy()

# Using Linear Regression instead of Logistic Regression
model = LinearRegression().fit(X, y)

# Getting the intercept and coefficients
intercept = model.intercept_
coefficients = model.coef_

print("Intercept:", intercept)
print("Coefficients:", coefficients)

# Display as Series with names to aid explanation
coeffs_series = pd.concat([pd.Series({'Intercept': intercept}),
                           pd.Series(coefficients, index=df.columns[df.columns != 'Athlete performance'])])
print(coeffs_series)

