import os
import boto3
import psycopg2
import pandas as pd
import pytz
from datetime import datetime, timedelta

""" Get environment variables """

client_ssm = boto3.client('ssm')
parameters = client_ssm.get_parameters(
    Names=[
        '/export_ghost/AWS_ACCESS_KEY_ID',
        '/export_ghost/AWS_SECRET_ACCESS_KEY',
        '/export_ghost/BUCKET_NAME',
        '/export_ghost/DB_HOST',
        '/export_ghost/DB_NAME',
        '/export_ghost/DB_PASSWORD',
        '/export_ghost/DB_USER'
    ],
    WithDecryption=True
)

def connect():
    """ Connect to the PostgreSQL database server """

    conn = None
    try:
        # formating today day
        tz_america_sp = datetime.now(tz=pytz.timezone('America/Sao_Paulo'))
        today_day = tz_america_sp.strftime('%Y-%m-%d')

        previous_day = (tz_america_sp - timedelta(days=1)).strftime('%Y-%m-%d')
        file_name = f"comments-{today_day}.csv"

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host=parameters['Parameters'][3]['Value'],
            database=parameters['Parameters'][4]['Value'],
            password=parameters['Parameters'][5]['Value'],
            user=parameters['Parameters'][6]['Value'],
            port="5432"
        )
		
        # create a cursor
        cursor = conn.cursor()
        
	    # execute a statement
        print('PostgreSQL database version:')
        cursor.execute('SELECT version()')
        print(cursor.fetchall())

        # execute select in author_id
        print('Executing query:')
        query = (
            "SELECT author_id,"
            +   " commentable_id,"
            +   " commentable_type,"
            +   " REGEXP_REPLACE(content, E'[\\n|\\t|\\r]', ' ', 'g') AS content,"
            +   " to_char(created_at, 'YYYY-MM-DD HH:MI:SS') AS created_at,"
            +   " device_type,"
            +   " id,"
            +   " to_char(moderated_at, 'YYYY-MM-DD HH:MI:SS') AS moderated_at,"
            +   " moderator_id,"
            +   " rejection_reasons,"
            +   " state,"
            +   " to_char(updated_at, 'YYYY-MM-DD HH:MI:SS') AS updated_at,"
            +   " upvotes"
            +" FROM comments"
            +f" WHERE (created_at >= timestamp with time zone '{previous_day} 00:00:00.000-03:00'"
            +    f" AND created_at < timestamp with time zone '{today_day} 00:00:00.000-03:00');")
        
        # generating file
        sql_df = pd.read_sql_query(query, conn)

        sql_df["content"] = sql_df["content"].apply(lambda x: x.replace("|", ""))
        sql_df.to_csv(f"/tmp/{file_name}", sep="|", index=False)

        # close connection with database
        cursor.close()
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    
    return file_name


def upload_file(file, bucket, object_name=None):
    """ Upload a file to S3 bucket """

    if object_name is None:
        object_name = os.path.basename(file)

    # Upload the file
    print('Uploading to s3...')
    client_s3 = boto3.client(
        's3',
        aws_access_key_id=parameters['Parameters'][0]['Value'],
        aws_secret_access_key=parameters['Parameters'][1]['Value'],
    )
    client_s3.upload_file(file, bucket, object_name)


def delete_file(file):
    """ Delete file of cache """

    # Delete file
    print('Deleting file...')
    os.remove(f"/tmp/{file}")


def lambda_handler(event, context):
    file_name = connect()
    upload_file(
        file=f"/tmp/{file_name}",
        bucket=parameters['Parameters'][2]['Value'],
        object_name=f"comments/aurora/pre-load/{file_name}"
    )
    delete_file(
        file=file_name
    )
