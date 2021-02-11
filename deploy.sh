#!/bin/bash

# make the bucket
aws s3 mb "s3://${PROJECT_NAME}"

# set CORS rules for the bucket
aws s3api put-bucket-cors \
    --bucket ${PROJECT_NAME} \
    --cors-configuration file://cors.json

# enable bucket versioning
aws s3api put-bucket-versioning \
	--bucket ${PROJECT_NAME} \
	--versioning-configuration Status=Enabled

source package.sh

# create the lambda function and upload packaged code
aws lambda create-function \
    --function-name ${PROJECT_NAME} \
    --zip-file fileb://package.zip \
    --handler function.lambda_handler \
    --runtime python3.7 \
    --layers arn:aws:lambda:us-east-2:796077402566:layer:tableau-scraper:1 \
    --role ${AWS_LAMBDA_ROLE} \
    --timeout 900 \
    > 'function.json'

rm package.zip

source set-env-vars.sh

source schedule.sh