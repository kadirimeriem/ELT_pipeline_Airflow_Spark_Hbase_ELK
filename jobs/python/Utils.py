import logging
from pyspark.sql import SparkSession
import happybase
import Yahoo



def create_spark_connection():
    s_conn=None
    # create spark conn here
    try:
        s_conn=SparkSession.builder.appName("Historical_data").getOrCreate()
        s_conn.sparkContext.setLogLevel("ERROR")
        logging.info("Spark connection created succesfully")
    except Exception as e:
        logging.error(f"connection to spark failed due to {e} ")

    return s_conn

def create_hbase_connection():
    #create cassandra conn here
   
    try:
        connection = happybase.Connection("hbase")
        return connection
    except Exception as e:
        logging.error(f"could not create cassandra connection due to {e}")
        return None

def create_hbase_table_if_not_exist(connection, table_name, column_families):

    try:
        # Create a table if it does not exist
        tables = connection.tables()
        if table_name.encode() not in tables:
            column_family_dict = {f'{value}': dict() for i, value in enumerate(column_families)}
            connection.create_table(table_name, column_family_dict)
            print("historical_data table created")

        else:
            print("historical_data table already exists")
    except Exception as e:
        print(f"Error creating table: {e}")
 
def insert_historical_data(connection, table_name):
    # Open the table
    table = connection.table(table_name)

    # get data
    df = Yahoo.HistoricalData()  # Assuming this retrieves your DataFrame
    
    # Create an empty list to store the result
    result_list = []

    # Iterating over rows and storing values as lists with index
    for index, row in df.iterrows():
        values_list = row.values.tolist()  # Convert row values to list
        result_list.append([index.strftime('%Y-%m-%d %H:%M:%S')] + values_list)  # Append index and values as a list of lists
    
    # inserting data
    for row_data in result_list:
        row_key = row_data[0].encode()  # Convert row key to bytes
        data_dict_Adj = {
            b'Adj Close:AAPL': str(row_data[1]).encode(),  # Convert string to bytes
            b'Adj Close:AMZN': str(row_data[2]).encode(),  # Convert string to bytes
            b'Adj Close:BA': str(row_data[3]).encode(),  # Convert string to bytes
            b'Adj Close:GOOG': str(row_data[4]).encode(),  # Convert string to bytes
            b'Adj Close:MSFT': str(row_data[5]).encode()  # Convert string to bytes
        }
        
        data_dict_Close = {
            b'Close:AAPL': str(row_data[6]).encode(),  # Convert string to bytes
            b'Close:AMZN': str(row_data[7]).encode(),  # Convert string to bytes
            b'Close:BA': str(row_data[8]).encode(),  # Convert string to bytes
            b'Close:GOOG': str(row_data[9]).encode(),  # Convert string to bytes
            b'Close:MSFT': str(row_data[10]).encode()  # Convert string to bytes
        }
        
        data_dict_High = {
            b'High:AAPL': str(row_data[11]).encode(),  # Convert string to bytes
            b'High:AMZN': str(row_data[12]).encode(),  # Convert string to bytes
            b'High:BA': str(row_data[13]).encode(),  # Convert string to bytes
            b'High:GOOG': str(row_data[14]).encode(),  # Convert string to bytes
            b'High:MSFT': str(row_data[15]).encode()  # Convert string to bytes
        }
        
        data_dict_Low = {
            b'Low:AAPL': str(row_data[16]).encode(),  # Convert string to bytes
            b'Low:AMZN': str(row_data[17]).encode(),  # Convert string to bytes
            b'Low:BA': str(row_data[18]).encode(),  # Convert string to bytes
            b'Low:GOOG': str(row_data[19]).encode(),  # Convert string to bytes
            b'Low:MSFT': str(row_data[20]).encode()  # Convert string to bytes
        }
        data_dict_Open = {
            b'Open:AAPL': str(row_data[21]).encode(),  # Convert string to bytes
            b'Open:AMZN': str(row_data[22]).encode(),  # Convert string to bytes
            b'Open:BA': str(row_data[23]).encode(),  # Convert string to bytes
            b'Open:GOOG': str(row_data[24]).encode(),  # Convert string to bytes
            b'Open:MSFT': str(row_data[25]).encode()  # Convert string to bytes
        }
        data_dict_Volume = {
            b'Volume:AAPL': str(row_data[26]).encode(),  # Convert string to bytes
            b'Volume:AMZN': str(row_data[27]).encode(),  # Convert string to bytes
            b'Volume:BA': str(row_data[28]).encode(),  # Convert string to bytes
            b'Volume:GOOG': str(row_data[29]).encode(),  # Convert string to bytes
            b'Volume:MSFT': str(row_data[30]).encode()  # Convert string to bytes
        }
        
        # Inserting data for Adj Close into the table
        table.put(row_key, {column: value for column, value in data_dict_Adj.items()})
        #inserting data for Close
        table.put(row_key,{column: value for column, value in data_dict_Close.items()})
        #inserting data for High
        table.put(row_key,{column: value for column, value in data_dict_High.items()})
        #inserting data for Low
        table.put(row_key,{column: value for column, value in data_dict_Low.items()})
        #inserting data for Open
        table.put(row_key,{column: value for column, value in data_dict_Open.items()})
         #inserting data for Volume
        table.put(row_key,{column: value for column, value in data_dict_Volume.items()})
        
    print( "Insertion done")
