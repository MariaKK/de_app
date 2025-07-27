import os
import asyncio
import aiohttp
import pandas as pd
import logging
from sqlalchemy import create_engine  

# Logging set
logging.basicConfig(level=logging.INFO)

async def fetch_data(session, version, endpoint, params=None):
    url = f"https://restcountries.com/{version}/{endpoint}"

    try:
        async with session.get(url, params=params) as response:
            if response.status != 200:                                                                                  #if response is not success, log the error
                logging.error(f"Error fetching data from {url}: Status code {response.status}")
                return None
            data = await response.json()
            return pd.DataFrame(data)
    except Exception as e:
        logging.error(f"Error fetching data from {url}: {e}")
        return None

async def fetch_detailed_countries_info(version): 
    async with aiohttp.ClientSession() as session:
        countries_list = await fetch_data(session, version, "all", {"fields": "name"})                  #get country names for find more info
        if countries_list is not None:
            tasks = []
            for country in countries_list['name']:
                tasks.append(fetch_data(session, version, f"name/{country['common']}")) 
            detailed_country_data = await asyncio.gather(*tasks)
            return pd.concat(detailed_country_data, ignore_index=True) if detailed_country_data else pd.DataFrame()
        return pd.DataFrame()

def save_to_postgres(df):
    engine = create_engine(f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")

    df = df[sorted(df.columns)]                                                                                         #sorting columns alphabetically - only for my own convenience 
    df.to_sql('countries', engine, if_exists='replace', index=False)                                                    #Replace the table if it exists

def validate_data(df):
    # Check essential columns
    required_columns = ['name']  
    for column in required_columns:
        if column not in df.columns:
            logging.error(f"Missing required column: {column}")
            return False
    return True

def extract_relevant_data(df):
    # Checking columns with embedded data
    for column in df.columns:
        if df[column].apply(lambda x: isinstance(x, (dict, list))).any():
            logging.info(f"Extracting relevant data from column: {column}")

            if column == 'name':
                    df['name_common'] = df[column].apply(lambda x: x.get('common') if isinstance(x, dict) else None)
                    df['name_official'] = df[column].apply(lambda x: x.get('official') if isinstance(x, dict) else None)
                    df['name_native'] = df[column].apply(                                                               # Агрегируем значения из nativeName с указанием языка
                        lambda x: ', '.join([f"{v['official']} ({v['common']}) [{k}]" for k, v in x.get('nativeName', {}).items() if isinstance(v, dict)]) 
                        if isinstance(x, dict) else None
                    )
                    df = df.drop(columns=[column], errors='ignore')

            elif column == 'tld':
                    df['tld'] = df[column].apply(lambda x: ', '.join(x) if isinstance(x, list) else None)        
            elif column == 'currencies':
                    df['currencies'] = df[column].apply(lambda x: ', '.join([f"{v['name']} ({k}) - {v['symbol']}" for k, v in x.items()]) if isinstance(x, dict) else None)
            elif column == 'languages':
                    df['languages'] = df[column].apply(lambda x: ', '.join([f"{v} ({k})" for k, v in x.items()]) if isinstance(x, dict) else None)
          
            elif column == 'idd':
                    df['idd'] = df[column].apply(lambda x: f"Root: {x['root']}, Suffixes: {', '.join(x['suffixes'])}" if isinstance(x, dict) and 'root' in x and 'suffixes' in x else None)
            elif column == 'capital':
                    df['capital'] = df[column].apply(lambda x: ', '.join(x) if isinstance(x, list) else None)
            elif column == 'altSpellings':
                    df['altSpellings'] = df[column].apply(lambda x: ', '.join(x) if isinstance(x, list) else None)
            elif column == 'latlng':
                    df['latlng'] = df[column].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else None)
            elif column == 'borders':
                    df['borders'] = df[column].apply(lambda x: ', '.join(x) if isinstance(x, list) else None)
            elif column == 'demonyms':
                    df['demonyms'] = df[column].apply(lambda x: ', '.join([f"{lang}: {v['f']} (f: {v['f']}, m: {v['m']})" for lang, v in x.items()]) if isinstance(x, dict) else None)
            elif column == 'translations':
                    df['translations'] = df[column].apply(lambda x: ', '.join([f"{k}: {v['common']} ({v['official']})" for k, v in x.items()]) if isinstance(x, dict) else None)
            elif column == 'maps':
                    df['maps'] = df[column].apply(lambda x: ', '.join([f"{k}: {v}" for k, v in x.items()]) if isinstance(x, dict) else None)
            elif column == 'gini':
                    df['gini'] = df[column].apply(lambda x: list(x.values())[0] if isinstance(x, dict) and x else None)
            elif column == 'car':
                    df['car_signs'] = df[column].apply(lambda x: ', '.join(x.get('signs', [])) if isinstance(x, dict) else None)
                    df['car_side'] = df[column].apply(lambda x: x.get('side') if isinstance(x, dict) else None)
                    df = df.drop(columns=[column], errors='ignore')
            elif column == 'timezones':
                    df['timezones'] = df[column].apply(lambda x: ', '.join(x) if isinstance(x, list) else None)
            elif column == 'continents':
                    df['continents'] = df[column].apply(lambda x: ', '.join(x) if isinstance(x, list) else None)
            elif column == 'flags':
                    df['flag_png'] = df[column].apply(lambda x: x.get('png') if isinstance(x, dict) else None)
                    df['flag_svg'] = df[column].apply(lambda x: x.get('svg') if isinstance(x, dict) else None)
                    df = df.drop(columns=[column], errors='ignore')
            elif column == 'coatOfArms':
                    df['coatOfArms_png'] = df[column].apply(lambda x: x.get('png') if isinstance(x, dict) else None)
                    df['coatOfArms_svg'] = df[column].apply(lambda x: x.get('svg') if isinstance(x, dict) else None)
                    df = df.drop(columns=[column], errors='ignore')
            elif column == 'capitalInfo':
                   
                    df[['capital_lat', 'capital_lng']] = df[column].apply(
                        lambda x: pd.Series(x.get('latlng')) if isinstance(x, dict) and 'latlng' in x else pd.Series([None, None])
                    )    #if it is a dictionary, extract the latitude
                    df = df.drop(columns=[column], errors='ignore')
            elif column == 'postalCode':
                    df['postalCode_format'] = df[column].apply(lambda x: x.get('format') if isinstance(x, dict) else None)
                    df['postalCode_regex'] = df[column].apply(lambda x: x.get('regex') if isinstance(x, dict) else None)
                    df = df.drop(columns=[column], errors='ignore')

    return df

def clean_and_normalize_data(df):
    df = extract_relevant_data(df)                                                                                      #extracting essential data from the dictionary
    df = df.drop_duplicates()                                                                                           #deleting doubling data (about 20 territories will be deleted 'cause e.g. API will return Guinea-Bissau in request about Guinea-Bissau and Guinea and so on)
    return df

def enrich_data(df, api_version):                                                                                       #meta adding
    df['fetch_time'] = pd.Timestamp.now()  
    df['source'] = 'restcountries.com'     
    df['api_version'] = api_version        
    return df

def main():
    api_version = "v3.1"                  
    logging.info(f"Fetching data from {api_version}...")
    raw_countries_data = asyncio.run(fetch_detailed_countries_info(api_version))                                       
    
    if not raw_countries_data.empty:

        if validate_data(raw_countries_data):                                                                           #Data validation
            
            cleaned_data = clean_and_normalize_data(raw_countries_data)
            enriched_data = enrich_data(cleaned_data, api_version)
            save_to_postgres(enriched_data) 
        else:
            logging.error("Data validation failed.")
if __name__ == "__main__":
    main()

