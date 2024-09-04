from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.postgres.operators.postgres import SQLExecuteQueryOperator
from airflow.utils import timezone

# Variables

postgres_driver_jar="/opt/bitnami/spark/resources/jars/postgresql-42.6.2.jar"
filename='restaurant_detail.csv' #FIXME change to your file name
tablename='restaurant_detail' #FIXME change to your table name

# Query

create_pg_table=f'''CREATE TABLE IF NOT EXISTS {tablename} (
    ID VARCHAR(255),
    RESTAURANT_NAME VARCHAR(255),
    CATEGORY VARCHAR(255),
    ESTIMATED_COOKING_TIME DOUBLE PRECISION,
    LATITUDE DOUBLE PRECISION,
    LONGITUDE DOUBLE PRECISION
);'''

load_pg_table = f"""
    TRUNCATE TABLE {tablename};
    COPY restaurant_detail
    FROM '/opt/bitnami/spark/resources/data/{filename}'
    WITH (FORMAT csv, HEADER true);
"""

# DAG

with DAG(
    dag_id='etl',
    start_date=timezone.datetime(2024,1,1),
    schedule= None,
):

    # Define the task
    create_pg_table = SQLExecuteQueryOperator(
        task_id='create_pg_table',
        sql=create_pg_table,
        conn_id='postgres_docker'
    )

    load_pg_table = SQLExecuteQueryOperator(
        task_id='load_pg_table',
        sql=load_pg_table,
        conn_id='postgres_docker'
    )

    load_to_hive = SparkSubmitOperator(
    application="/opt/bitnami/spark/app/load_to_hive.py", 
    task_id="load_to_hive",
    conn_id='spark_default',
    jars=postgres_driver_jar,
    driver_class_path=postgres_driver_jar,
    verbose=True
    )
    
    create_hive_table = SparkSubmitOperator(
    application="/opt/bitnami/spark/app/create_hive_table.py", 
    task_id="create_hive_table",
    conn_id='spark_default',
    )

create_pg_table >> load_pg_table >> load_to_hive
create_hive_table >> load_to_hive