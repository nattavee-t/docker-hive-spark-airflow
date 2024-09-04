from pyspark.sql import SparkSession
from pyspark.sql.functions import lit

dbname='hive_db' # FIXME change to your db name
tablename='restaurant_detail' # FIXME change to your table name

# Postgres config

jdbc_url = "jdbc:postgresql://postgres/my_db"
DB_USER = 'airflow'
DB_PASSWORD = 'airflow'

# Init Logger

def logger_init():
    log4jLogger = spark._jvm.org.apache.log4j
    logger = log4jLogger.LogManager.getLogger(__name__)
    return logger


# Function to read data from PostgreSQL table
def read_data(table_name):
    try:
        df = spark.read \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("dbtable", table_name) \
            .option("user", DB_USER) \
            .option("password", DB_PASSWORD) \
            .load()
        return df
    except Exception as e:
        logger.error(f"Error reading data from PostgreSQL: {e}")
        raise

# Process restaurant_detail table
def process():

    restaurant_df = read_data(tablename)
    restaurant_df = restaurant_df.withColumn('dt', lit('latest'))

    logger.info(f'No. of records: {restaurant_df.count()}')

    # Writing to Hive table
    restaurant_df.write.insertInto(f"{dbname}.{tablename}",overwrite=True)
    logger.info('Data successfully written to Hive.')

# Initialize a SparkSession

spark = SparkSession.builder \
    .appName("Load Table to Hive") \
    .config("spark.hadoop.hive.metastore.uris", "thrift://metastore:9083") \
    .config("spark.sql.warehouse.dir", "/opt/hive/data/warehouse") \
    .config("spark.master", "local") \
    .enableHiveSupport() \
    .getOrCreate()

logger = logger_init()

process()
logger.info('Showing preview of table on Hive')
spark.sql(f'SELECT * FROM {dbname}.{tablename} LIMIT 5').show()

spark.stop()