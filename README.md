# Amazon API Gateway to AWS Lambda to Amazon DynamoDB

API Gateway -> Lambda -> DynamoDB

## Deployment Instructions
From the root directory
    ```
    sam deploy --guided  
    ```
The above will create a config (samconfig.toml) for the respective environment. 

All subsequent deployments can use the config file as follows (to use the test environment): 
    ```
    sam deploy --config-env test
    ```

When running locally. Start up the dynamodb instance 
    ```
    docker-compose up  
    ```
Environment parameters can be placed in the config file as follows:

    ```
    sam local start-api --env-vars env.json
    ```

env.json 
   ```
{
    "Parameters": {
        "AWSENV": "AWS_SAM_LOCAL"
    }
}
   ```

Fire off a request to the local endpoint as follows 
   ```
    curl -d "@event.json" -X POST http://localhost:3000
   ```
where event.json is  
```
{
	"bookingID" : 33972,
    "car" : "Toyota",
	"startDate" : "2023-05-01", 
	"endDate" : "2023-05-10", 
	"bookingStatus" : "PAID"
}
```


1. Note the outputs from the SAM deployment process. These contain the resource names and/or ARNs which are used for testing.

## How it works

When an HTTP POST request is sent to the Amazon API Gateway endpoint, the AWS Lambda function is invoked and inserts an item into the Amazon DynamoDB table.

## Testing

After deployment, use the AWS Management Console (explained below) to test this pattern by sending an HTTP POST request to the Amazon API Gateway endpoint (found in the CloudFormation console Stacks Outputs tab) to confirm an item is added to the Amazon DynamoDB table. Alternatively, a command line shell or another application can be used to send the HTTP POST request.

Using the Amazon API Gateway console, select the API, Resources, and POST method execution. Click Test on the Client box and the Test button without a request body. The request should return a response message 'Successfully inserted data!'. If any errors occur, this view also shows logs from the invocation for troubleshooting. Navigate to the Amazon DynamoDB console to verify the item was added into the table.

## Cleanup
 
1. Delete the stack
    ```bash
    aws cloudformation delete-stack --stack-name STACK_NAME
    ```
1. Confirm the stack has been deleted
    ```bash
    aws cloudformation list-stacks --query "StackSummaries[?contains(StackName,'STACK_NAME')].StackStatus"
    ```
----
Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.

SPDX-License-Identifier: MIT-0
