from geo_requests.processing import *
import sys
import psycopg2

logging.basicConfig(
    level=logging.DEBUG,  # Set log level to DEBUG for detailed logs
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def main(filePath):
    try:
        logging.info(f"Starting the geolocation data processing for file: {filePath}")

        geolocations = csv_to_dict(filePath)
        logging.info(f"Successfully converted {len(geolocations)} geolocations from CSV file.")

        # Set chunk size for processing geolocations
        GeoLocationQuantity = 100
        logging.info(f"Processing geolocations in chunks of {GeoLocationQuantity}.")

        df = process_geolocations(geolocations, GeoLocationQuantity)
        logging.info(f"Processed {len(df)} geolocations after chunk processing.")

        # Handle missing values and infer object types
        df = df.infer_objects()
        df = df.fillna('NULL VALUE')
        logging.info("Handled missing values and inferred object types.")

        # # Establish database connection and ingest data
        
        #retry mechanism for connect to database
        while True:
            time.sleep(30)
            try:
                engine = database_ingestion('bia_challenge', 'postgres', 'postgres')
                if db_engine:
                    break
            except Exception as e:
                logging.warning(f"++++ Retrying connection to the database because of the issue {str(e)}++++")
        #logging.info(f"Database connection to {database} established successfully.")
        
        df.to_sql('post_codes_raw', con=engine, if_exists='replace', index=False, schema = 'bronze')
        
        # Write the DataFrame to the database
        logging.info("Data successfully written to the 'post_codes_raw' table in the database.")
    
    except Exception as e:
        logging.error(f"An error occurred during the main processing flow: {str(e)}")
    
if __name__ == "__main__":
    
    filePath = sys.argv[1]
    # database = sys.argv[2]
    # dbUser = sys.argv[3]
    # dbPassword = sys.argv[4]
    
    main(filePath)