import boto3
import json
import logging 
import os
import base64

from botocore.exceptions import ClientError

#dynamodb_client = boto3.client('dynamodb',endpoint_url='http://localhost:8000')
logger = logging.getLogger()
logger.setLevel(logging.INFO) 


def lambda_handler(event, context):
    try: 
        print(json.dumps(event, indent=2))
        if event.get('body'):
            # requestBody = json.loads(event['body']) 
            # requestBody = json.dumps({'body':json.dumps(event)})
            requestBody = json.loads({'body':json.dumps(event)})
            # requestBody = (json.loads(base64.b64decode(event.get('body')).decode('utf-8')))
            # requestBody = json.loads(base64.b64decode(event.get('body')).decode('utf-8'))
            print(f"==> {requestBody}") 
            print("====>type is ===>")
            print(type(requestBody)) 
            requestBody = base64.decode(json.loads(event['body'])) 
            bookingID = requestBody['bookingID']
            car = requestBody["car"]
        else:
            return {
                'statusCode': 200,
                'body': 'Error: incorrect body passed'
            }
        logger.info(f"Adding bookingID {bookingID} and car {car}") 
        updateTable(bookingID, car)
    except ClientError as err:
        print("Unexpected error: %s" % e)
        logger.error("Error adding to table.")
        

    return {
        'statusCode': 200,
        'body': 'Successfully inserted data!'
    }


def updateTable(bookingID, car): 

    table_name = os.environ.get('TABLE', 'HireCarTable')
    region = os.environ.get('REGION', 'eu-west-1')
    aws_environment = os.environ.get('AWSENV', 'AWS')

    if aws_environment == 'AWS_SAM_LOCAL':
        ddb = boto3.resource(
            'dynamodb',
            endpoint_url='http://localhost:8000'
        )
    else:
        ddb = boto3.resource(
            'dynamodb',
            region_name=region
        )

    table = ddb.Table(table_name)
    
    response = table.put_item(
        Item={
            'bookingID': bookingID,
            'car' : car
            }
        )

    return {
        'statusCode': 200,
        'body': 'Successfully inserted data!'
    }
