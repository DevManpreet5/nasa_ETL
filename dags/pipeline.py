import os 
import json 
from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.utils.dates import days_ago

with DAG(
    dag_id='nasa_project',
    start_date=days_ago(1),
    schedule_interval='@daily'

) as dag:
    
    @task
    def create_table():
        posthook=PostgresHook(postgres_conn_id='postgres_id')

        create_table_query='''
        CREATE TABLE IF NOT EXISTS NASADATA(
            context TEXT,
            url TEXT
        );
        
        '''
        posthook.run(create_table_query)
        print('table created succesfully');
    
    #https://api.nasa.gov/planetary/apod?api_key=TLnQfhbikfGL2U1eL6NM6EiAHm1TUT2DfJF2MU1u

    #task 2 - extract
    extracted=SimpleHttpOperator(
        task_id='extract',
        http_conn_id='nasa_api',
        endpoint='planetary/apod',
        method='GET',
        data={"api_key": "{{conn.nasa_api.extra_dejson.api_key}}"},
        response_filter=lambda response:response.json()
    )

   # task 3-  transform
    @task
    def transform_data(response):
        data={
            'title':response.get('title'),
            'url':response.get('url')
        }
        print(data)
        return data

    # task 4 - load 
    @task
    def load_data_to_db(response):
        posthook=PostgresHook(postgres_conn_id='postgres_id')
        insert_query="""
        INSERT INTO NASADATA(context,url)
        VALUES (%s , %s);
        """

        posthook.run(insert_query,parameters=(response['title'],response['url']))
        print('data loaded to db')
    
    
    create_table() >>extracted
    api_response=extracted.output
    transf_data=transform_data(api_response)
    load_data_to_db(transf_data)

