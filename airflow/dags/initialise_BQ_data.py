from airflow import DAG, macros
import os
import time
from urllib.parse import urlparse
from airflow import models
from airflow.operators.bash_operator import BashOperator
# No module named 'airflow.providers'
# from airflow.providers.google.cloud.operators import BigQueryCreateEmptyTableOperator
import bigquery

# No module named 'httplib2'
# from airflow.contrib.operators.bigquery_operator import (
#     BigQueryCreateEmptyDatasetOperator,
#     BigQueryCreateEmptyTableOperator,
#     BigQueryCreateExternalTableOperator,
#     BigQueryDeleteDatasetOperator,
#     BigQueryDeleteTableOperator,
#     BigQueryGetDatasetOperator,
#     BigQueryGetDatasetTablesOperator,
#     BigQueryPatchDatasetOperator,
#     BigQueryUpdateDatasetOperator,
#     BigQueryUpdateTableOperator,
#     BigQueryUpsertTableOperator,
# )
from airflow.utils.dates import days_ago

default_args ={
    'owner': 'Jakuta',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}

BQ_CONN_ID = "my_gcp_conn"
BQ_PROJECT = "horizontal-cab-315308"
BQ_DATASET = "kaggle"

# [START instantiate_dag]
load_initial_BQ_data_dag = DAG(
    'BQ_1_load_initial_data',
    default_args=default_args,
    schedule_interval = None,
)

# # docker-compose -f docker-compose.yml run airflow test BQ_1_load_initial_data create_table 2020-06-02
create_table = bigquery.igQueryCreateEmptyTableOperator(
    task_id="create_table",
    dataset_id=BQ_DATASET,
    table_id="test_table",
    schema_fields=[
        {"name": "product_id", "type": "INTEGER", "mode": "REQUIRED"},
        {"name": "product_name", "type": "STRING", "mode": "NULLABLE"},
        {"name": "aisle_id", "type": "INTEGER", "mode": "NULLABLE"},
        {"name": "department_id", "type": "INTEGER", "mode": "NULLABLE"},
    ],
    bigquery_conn_id=BQ_CONN_ID,
    dag=load_initial_BQ_data_dag
)


# check_table_exists = BigQueryTableExistenceSensor(
#     task_id="check_table_exists", project_id=BQ_PROJECT, dataset_id=BQ_DATASET, table_id=TABLE_NAME
# )

