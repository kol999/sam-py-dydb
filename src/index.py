import boto3
import json
import logging
import os
import time
from botocore.exceptions import ClientError

# dynamodb_client = boto3.client('dynamodb',endpoint_url='http://localhost:8000')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def lambda_handler(event, context):
    try:
        #          print(json.dumps(event, indent=2))
        if event.get("body"):
            requestBody = json.loads(event["body"])
            bookingID = requestBody["bookingID"]
            car = requestBody["car"]
            #  startHireDate = requestBody["startDate"]
            #  endHireDate = requestBody["endDate"]
            status = requestBody["bookingStatus"]
            startHireDate = "2023-05-03"
            endHireDate = "2023-05-09"
        else:
            return {
                'statusCode': 400,
                'body': 'Error: incorrect body passed'
            }
        logger.info(f"Adding bookingID {bookingID} and car {car}")
        return updateTable(bookingID, car, startHireDate, endHireDate, status)
    except ClientError as err:
        logger.error(f"ClientError: Unexpected error: {err}.")
    except Exception as e:
        logger.error(f"Exception: Unexpected exception: {e}.")

    return {
        'statusCode': 400,
        'body': 'Lambda has thrown an error'
    }


def updateTable(bookingID, car, startHireDate, endHireDate, bookingStatus):

    table_name = os.environ.get('TABLE', 'HireCarTable')
    region = os.environ.get('REGION', 'eu-west-1')
    aws_environment = os.environ.get('AWSENV', 'AWS')

    #  The return code
    rc = 0
    returnBody = ""
    print(f"aws_environment: {aws_environment}")
    if aws_environment == 'AWS_SAM_LOCAL':
        local_ipaddress = os.environ.get('LocalHostIP')
        print(f"local_ipaddress: {local_ipaddress}")

        ddb = boto3.resource(
            'dynamodb',
            endpoint_url=f"http://{local_ipaddress}:8000"
        )
    else:
        ddb = boto3.resource(
            'dynamodb',
            region_name=region
        )

    try:
        table = ddb.Table(table_name)
        params = {
            'bookingID': bookingID,
            'car': car,
            'startHireDate': startHireDate,
            'endHireDate': endHireDate,
            'status': bookingStatus,
            'timestamp': str(int(time.time()))
        }

        response = table.put_item(
            TableName=table_name,
            Item=params
        )
        rc = response['ResponseMetadata']['HTTPStatusCode']
        returnBody = 'Successfully inserted data!'
    except ClientError as err:
        logger.error(f"Error adding to table.{err}")
        returnBody = err
        rc = response['ResponseMetadata']['HTTPStatusCode']

    return {
        'statusCode': rc,
        'body': returnBody
    }


if __name__ == "__main__":
    event = {
        "body": "{\"bookingID\": \"1\", \"car\": \"Tesla\", \"startDate\": \"2023-05-03\", \"endDate\": \"2023-05-09\", \"bookingStatus\": \"pending\"}"
    }
    lambda_handler(event, {})
    #  updateTable("1", "Tesla", "2023-05-03", "2023-05-09", "pending")
    #  updateTable("2", "Tesla", "2023-05-03", "2023-05-09", "pending")
    #  updateTable("3", "Tesla", "2023-05-03", "2023-05-09", "pending")
    #  updateTable("4", "Tesla", "2023-05-03", "2023-05-09", "pending")
