# Lambda CloudWatch Events to Hipchat v2

This is a Python 3.6 lambda function that relays CloudWatch Events to Hipchat via a CloudWatch Event Rule Target. Simply set your rule to pass the message to the Lambda at it will be sent to Hipchat. Due to the nature of the Events, you may need to add the ones you are interested in. Simply add a routing IF statement and the logic for the message. Currently it supports:

 - Glue Jobs 
 - Glue Crawlers 
 - Code Build Jobs
 - Codepipeline Pipelines

If you need help creating a rule see:
https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/Create-CloudWatch-Events-Rule.html

You will also need to allow CloudWatch Events to trigger the function.

    aws lambda add-permission \
    --function-name MyFunction \
    --statement-id MyId \
    --action 'lambda:InvokeFunction' \
    --principal events.amazonaws.com \
    --source-arn arn:aws:events:us-east-1:123456789012:rule/MyRule


If you still have issues, AWS have a troubleshooting guide here:
https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/CWE_Troubleshooting.html
