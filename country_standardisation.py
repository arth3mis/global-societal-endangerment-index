import pycountry
import pandas as pd
from fuzzywuzzy import process

UNKNOWN_COUNTRY = 'aaa.Unknown'


def all_countries():
    return [c.name for c in pycountry.countries]


def lookup_country(country_name: str, fuzzy_threshold=80):
    try:
        return pycountry.countries.lookup(country_name).name
    except LookupError: pass

    countries = all_countries()
    c_match = [c.casefold() for c in countries]
    try:
        if country_name.casefold() in c_match:
            return countries[c_match.index(country_name.casefold())]
    except Exception: pass

    # special cases
    if country_name == 'Canary Islands' or country_name == 'SPI':
        print(f"Using special case for '{country_name}' -> 'Spain'")
        return 'Spain'
    elif country_name == 'Turkey':
        print(f"Using special case for '{country_name}' -> 'Türkiye'")
        return 'Türkiye'
    elif 'Korea' in country_name and 'DPR' in country_name:
        print(f"Using special case for '{country_name}' -> 'Korea, Democratic People's Republic of'")
        return "Korea, Democratic People's Republic of"
    elif 'Congo' in country_name and ('dem' in country_name.casefold() or 'DR' in country_name):
        print(f"Using special case for '{country_name}' -> 'Congo, Democratic Republic of the'")
        return 'Congo, Democratic Republic of the'

    # fuzzy match
    try:
        best_match, score = process.extractOne(country_name, countries)
        if score > fuzzy_threshold:
            print(f"Using fuzzy match for '{country_name}' -> '{best_match}'")
            return best_match
        else:
            raise LookupError(f"Country '{country_name}' not found (best fuzzy match too low: {best_match} ({score}))")
    except LookupError as e:
        print(e)
        return UNKNOWN_COUNTRY


def standardise_countries(country_col: pd.Series, fuzzy_threshold=80):
    return country_col.map(lambda c: lookup_country(c, fuzzy_threshold=fuzzy_threshold))
