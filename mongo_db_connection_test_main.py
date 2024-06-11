##Not required in Production

from sensor.configuration.mongo_db_connection import MongoDBClient

if __name__ == '__main__':
    mongodb_client= MongoDBClient()
    ##Printing the collection name present in our database
    print("Collection Name:", mongodb_client.database.list_collection_names())

    ##In order to test this script updated requirements.txt file by adding 
    ##certifi and pymongo[srv]. Also made correction in mongo_db_connection.py
    ##to read the connection url from .env by first load_dotenv()