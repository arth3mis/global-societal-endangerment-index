import json


# load category JSON file
def load():
    with open('data/processing/category_indicator_map.json', 'r') as json_file:
        return json.load(json_file)


# filter dataframe based on category
def filter(df, category):
    columns = load().get(category, [])
    return df[columns]
