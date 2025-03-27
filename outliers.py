import pandas as pd


def find_outliers(df, column):
    # Calculate Q1, Q3, and IQR
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    # Define outlier boundaries
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    # Find outliers
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return outliers


def find_outliers_per_indicator(df):
    outliers = pd.DataFrame()
    for col in df:
        outliers = pd.concat([outliers, find_outliers(df, col)[[col]].count()], axis=0)
    outliers.reset_index(inplace=True)
    outliers['Outlier Percentage'] = outliers[0].apply(lambda x: round(x/len(df)*100, 2))
    outliers.columns = ['Indicator', 'Outliers', 'Outlier Percentage']
    return outliers.sort_values(by='Outliers', ascending=False)