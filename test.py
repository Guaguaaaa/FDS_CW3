import pandas as pd

def filter(column_name, filter_symbol, contain, df):
    mask = df[column_name].notna()

    df = df[mask]

    if contain == 1:
        filtered_values = df[df[column_name].str.contains(filter_symbol)][column_name]
    elif contain == 0:
        filtered_values = df[~df[column_name].str.contains(filter_symbol)][column_name]
    else:
        filtered_values = df[~df[column_name].astype(str).str.match(r'^\d{4}$')][column_name]

    return filtered_values


def testing(df):
    column_name = 'Athlete year of birth'
    filter_symbol = ".0"
    df = df[~df[column_name].astype(str).str.match(r'^\d{4}$')][column_name]
    df = df[~df[column_name].str.contains(filter_symbol)][column_name]

    print(df)

if __name__ == '__main__':
    df = pd.read_csv("TWO_CENTURIES_OF_UM_RACES.csv", dtype='str')

    print(df['Athlete age category'].unique())
    '''count_X = df['Athlete gender'].value_counts()['X']
    print("Number of 'X' occurrences:", count_X)'''

    '''column = "Athlete performance"
    symbol = "-"

    var_50km = df[df['Event distance/length'] == '50km']
    mask = var_50km[column].notna()

    var_50km = var_50km[mask]

    var_50km[column] = var_50km[column].astype(str)
    filtered_values = var_50km[var_50km[column].str.contains('d')][column]
    print(filtered_values)


    #print(filter(column, symbol, -1, df))'''

    #testing(df)