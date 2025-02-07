import requests
import pandas as pd
import time
from sqlalchemy import Table, MetaData, create_engine
from sqlalchemy.orm import sessionmaker
import concurrent.futures
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,  
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

url= 'https://api.postcodes.io/'
endpoint= 'postcodes'

def csv_to_dict(csvPath: str) -> dict:
    try:
        dfPostCodesGeo = pd.read_csv(csvPath, dtype={'lat': 'float64', 'lon': 'float64'})
        dfPostCodesGeo.rename(columns= {'lat': 'latitude', 'lon': 'longitude'}, inplace=True)
    
        numberOfDuplicatedCodes = len(dfPostCodesGeo[dfPostCodesGeo.duplicated(list(dfPostCodesGeo.columns))])
        dfPostCodesGeo.drop_duplicates(inplace=True)
        
        logging.info(f"Number of Geocodes duplicated: {numberOfDuplicatedCodes}")
        logging.info(f"Percentage of duplicates respect all the dataframe: {numberOfDuplicatedCodes / len(dfPostCodesGeo):.2%}")
        
        return dfPostCodesGeo.to_dict(orient= 'records')
    except Exception as e:
        logging.error(f"Error when processing CSV with path {csvPath}. Error {e}")
        sys.exit(1)

def json_response(url: str, endpoint: str, jsonBody: dict) -> dict:
    # Retry logic, attempts 3 times in case of failure
    attempt = 1
    while attempt <= 3:
        try:
            logging.info(f"Attempt {attempt}: Sending POST request to {url}{endpoint}")
            response = requests.post(f'{url}{endpoint}', json=jsonBody)
            
            statusCode = response.status_code
            statusMessage = response.reason

            # Raise exception for any HTTP errors
            response.raise_for_status()
    
            logging.info(f"Request successful. Status Code: {statusCode}, Message: {statusMessage}")
            
            return response.json()
        except Exception as e:
            logging.error(f"Error during request attempt {attempt}: {e}")
            
            attempt += 1
            time.sleep(30)
            
            # If it exceeds 3 attempts, log the failure
            if attempt > 3:
                logging.error(f"Failed to complete request after 3 attempts.")
                break
    
def transform_data(jsonResponse: dict) -> pd.DataFrame:
    df = pd.json_normalize(
        jsonResponse["result"],
        record_path='result',
        meta=[['query', 'latitude'], ['query', 'longitude']]
    )
    return df

def process_geolocation_chunk(geolocations_chunk, url, endpoint):
    try:
        logging.info(f"Processing geolocation chunk with {len(geolocations_chunk)} entries")
        
        # Prepare the JSON body for the API request
        jsonBody = {"geolocations": geolocations_chunk}
        
        jsonResponse = json_response(url, endpoint, jsonBody)
        
        logging.info(f"Successfully processed geolocation chunk")
        
        return transform_data(jsonResponse)
    except Exception as e:
        logging.error(f"Error processing geolocations chunk: {geolocations_chunk}. Error: {str(e)}")
        sys.exit(1)
        

def process_geolocations(geolocations, GeoLocationQuantity):
    df = pd.DataFrame()
    futures = []  # List to hold the future tasks for concurrent execution

    logging.info(f"Starting processing of {len(geolocations)} geolocations in chunks of {GeoLocationQuantity} entries each.")
    
    # Use ThreadPoolExecutor to parallelize processing in chunks
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Split the geolocations into chunks and submit each chunk for processing
        for i in range(0, 200, GeoLocationQuantity):
            geolocationsRequets = geolocations[i: i + GeoLocationQuantity]
            futures.append(executor.submit(process_geolocation_chunk, geolocationsRequets, url, endpoint))

        # Wait for all tasks to complete and gather the results
        for future in concurrent.futures.as_completed(futures):
            time.sleep(0.5)
            try:
                result = future.result()  # Get the result of each future task
                if result is not None:
                    df = pd.concat([df, result], axis=0, ignore_index=True)  # Combine the results into the dataframe
            except Exception as e:
                logging.error(f"Error in processing task: {str(e)}")
                sys.exit(1)
    
    logging.info(f"Geolocation processing completed. Total records processed: {len(df)}")
    return df

def database_ingestion(database, dbUser, dbPassword):
    try:
        # Construct the database connection URL
        DATABASE_URL = f"postgresql://{dbUser}:{dbPassword}@postgres:5432/{database}"
        logging.info(f"Connecting to database {database} as user {dbUser}")
        
        engine = create_engine(DATABASE_URL)
        
        # Set up sessionmaker for DB interaction
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        logging.info(f"Database connection established successfully.")
        
        return engine
    except Exception as e:
        logging.error(f"Error setting up database connection: {str(e)}")
        sys.exit(1)

def get_db_engine():
    return create_engine('postgresql://{}:{}@{}/{}'.format('postgres', 'postgres', 'postgres:5432', 'bia_test'))

# def insert_dataframe(df, table_name, conn):
#     columns = ", ".join(df.columns)
#     values_placeholder = ", ".join(["%s"] * len(df.columns))
#     insert_query = f"INSERT INTO bronze.{table_name} ({columns}) VALUES ({values_placeholder})"
    
#     try:
#         with conn.cursor() as cursor:
#             for row in df.itertuples(index=False, name=None):
#                 cursor.execute(insert_query, row)
#         conn.commit()
#         print(f"Data successfully inserted into {table_name}")
#     except Exception as e:
#         conn.rollback()
#         print(f"Error: {e}")
#     finally:
#         conn.close()