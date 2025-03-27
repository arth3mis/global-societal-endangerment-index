import json


# load category JSON file
def load(version=''):
    with open(f'data/processing/category_indicator_map{"_" + version if version != "" else ""}.json', 'r') as json_file:
        return json.load(json_file)


# filter dataframe based on category
def filter(df, category):
    columns = load().get(category, [])
    return df[columns]


def drop(json_data, columns):
    for key in json_data.keys():
        for column in columns:
            if column in json_data[key]:
                json_data[key].remove(column)
    return json_data
