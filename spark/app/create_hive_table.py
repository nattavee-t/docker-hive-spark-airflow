from pyspark.sql import SparkSession

dbname = 'hive_db'  # FIXME change to your db name
tablename = 'restaurant_detail'  # FIXME change to your table name

# Init Logger

def logger_init():
    log4jLogger = spark._jvm.org.apache.log4j
    logger = log4jLogger.LogManager.getLogger(__name__)
    return logger

def create_table():
    
    # Create the database if it does not exist
    spark.sql(f'CREATE DATABASE IF NOT EXISTS {dbname};')

    # Create the external table
    spark.sql(
        f"""
        CREATE EXTERNAL TABLE IF NOT EXISTS {dbname}.{tablename} (
            id VARCHAR(255),
            restaurant_name VARCHAR(255),
            category VARCHAR(255),
            estimated_cooking_time DOUBLE,
            latitude DOUBLE,
            longitude DOUBLE
        )
        PARTITIONED BY (dt VARCHAR(100))
        STORED AS PARQUET
        LOCATION '/opt/hive/data/warehouse/{tablename}/'
        """
    )
    logger.info(f"Table {dbname}.{tablename} created successfully.")
       
# Initialize a SparkSession
spark = SparkSession.builder \
    .appName("Create Table on Hive") \
    .config("spark.hadoop.hive.metastore.uris", "thrift://metastore:9083") \
    .config("spark.sql.warehouse.dir", "/opt/hive/data/warehouse") \
    .enableHiveSupport() \
    .getOrCreate()

logger = logger_init()

create_table()

spark.stop()