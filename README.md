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
