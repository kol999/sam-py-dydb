import boto3
import json
import logging 
import os
import base64
import socket

from botocore.exceptions import ClientError

#dynamodb_client = boto3.client('dynamodb',endpoint_url='http://localhost:8000')
logger = logging.getLogger()
logger.setLevel(logging.INFO) 


def lambda_handler(event, context):
    try: 
#         print(json.dumps(event, indent=2))
        if event.get('body'):
            requestBody = json.loads(event['body']) 
            bookingID = requestBody['bookingID']
            car = requestBody["car"]
        else:
            return {
                'statusCode': 200,
                'body': 'Error: incorrect body passed'
            }
        logger.info(f"Adding bookingID {bookingID} and car {car}") 
        response = updateTable(bookingID, car)
    except ClientError as err:
        logger.error("Unexpected error: {err}.")
        
    return response 

def updateTable(bookingID, car): 

    table_name = os.environ.get('TABLE', 'HireCarTable')
    region = os.environ.get('REGION', 'eu-west-1')
    aws_environment = os.environ.get('AWSENV', 'AWS')
    hostname = os.environ.get('hostname')

    # The return code 
    rc = 0 
    returnBody = "" 

    if aws_environment == 'AWS_SAM_LOCAL':
        local_ip = get_localip() 
        ddb = boto3.resource(
            'dynamodb',
            endpoint_url="http://{local_ip}:8000"
        )
    else:
        ddb = boto3.resource(
            'dynamodb',
            region_name=region
        )

    try:  
        table = ddb.Table(table_name)
        params = {
            'bookingID' : bookingID,
            'car' : car
        }

        response = table.put_item(
            TableName=table_name,
            Item=params
        )
        rc =  response['ResponseMetadata']['HTTPStatusCode']  
        returnBody = 'Successfully inserted data!'
    except ClientError as err:
        logger.error(f"Error adding to table.{err}")
        returnBody = err 
        rc = response['ResponseMetadata']['HTTPStatusCode']  


    return {
        'statusCode': rc,
        'body': returnBody  
    }

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP



