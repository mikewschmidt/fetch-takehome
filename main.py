import boto3
import json
from datetime import datetime
import hashlib
import psycopg2

###  FUNCTIONS  ###


def convert_messages(messages: list) -> list:
    """A list of strings from SQS to dict and hashes PII  and returns a list of dictionaries

        Use this function to pass in the response json/dictionary object,
        so it can extract the correct data and hash mask two PII data points: "device_id" and "ip".
    """
    date = datetime.datetime.now()
    l_messages = []
    for message in messages:
        body = json.loads(message.body)
        # Check for a user_id key, delete and continue if None
        if body.get('user_id') == None:
            message.delete()
            continue
        body['create_date'] = date
        body['device_id'] = hashlib.sha3_256(
            body['device_id'].encode()).hexdigest()
        body['ip'] = hashlib.sha3_256(body['ip'].encode()).hexdigest()
        body['receipt_handle'] = message.receipt_handle
        l_messages.append(body)
        print(body)

    return l_messages


def mask(pii: str) -> str:
    """Hashes and returns string. To mask PII (Personally Identifiable Information)"""
    return hashlib.sha3_256(pii.encode()).hexdigest()


def db_execute_statement(sql_statement: str):
    """Makes a connection to the database and executes the input SQL statement."""

    try:
        conn = psycopg2.connect(
            database="postgres",
            host="localhost",
            user="postgres",
            password="postgres",
            port='5432'
        )
    except (Exception) as e:
        print("ERROR! Connecting to the database. ", e)

    try:
        with conn.cursor() as cur:
            cur.execute(sql_statement)
            output = None
            conn.commit()

    except (Exception, psycopg2.DatabaseError) as e:
        print("ERROR! There was a problem with executing the SQL statement: ", e)
        output = e

    finally:
        conn.close()
        return output


def db_insert_messages(l_messages: list):
    """ Inserts all the messages into the database.
        Loops through all the messages inserts one at a time 
        and masks the PII columns.
        Returns nothing.
    """
    if not l_messages or len(l_messages) == 0:
        print("Messages is empty, can not insert anything into the database")
        return

    for message in l_messages:
        body = json.loads(message.body)
        print(body)
        # Check for a user_id key, skipping if None
        if body.get('user_id') == None:
            continue

        insert = f"""
            INSERT INTO public.user_logins(user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
            VALUES ('{body.get('user_id')}', 
                    '{body.get('device_type')}', 
                    '{mask(body.get('ip'))}',
                    '{mask(body.get('device_id'))}', 
                    '{body.get('locale')}',
                    '{body.get('app_version')}', 
                    '{datetime.now()}');
            """
        # If something returns then there is an issue
        if not db_execute_statement(insert):
            message.delete()
        else:
            print("Something bad happened when inserting into the database")


if __name__ == "__main__":
    # Alter the table, because the application version uses the format 1.2.3, which is not a number.
    statement = "ALTER TABLE user_logins ALTER COLUMN app_version TYPE varchar(10);"
    db_execute_statement(statement)

    # Creating the SQS and queue objects
    sqs = boto3.resource(
        'sqs',
        endpoint_url='http://localhost:4566',
        region_name="us-east-1",
        aws_access_key_id="access_key_id",
        aws_secret_access_key="secret"
    )
    queue = sqs.get_queue_by_name(QueueName='login-queue')

    ### PROCESS ALL THE MESSAGES FROM THE QUEUE ###
    messages = queue.receive_messages(
        MaxNumberOfMessages=10, WaitTimeSeconds=1, VisibilityTimeout=20)
    count = 0

    while len(messages) > 0:
        count += len(messages)
        # Inserts the messages into the database
        db_insert_messages(messages)
        messages = queue.receive_messages(
            MaxNumberOfMessages=10, WaitTimeSeconds=1, VisibilityTimeout=20)

    print(count, "messages were extracted, transformed and loaded into the database")
