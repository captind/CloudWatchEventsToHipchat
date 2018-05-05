#!/usr/bin/env python
# Script to route AWS Cloud Watch Notification events to Hipchat (easily adapted for other tools.) Due to the CloudWatch events
# Varing for each event time, you may need to extend with what you need. Samples can be found in the AWS Knowlegebase.
# https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/EventTypes.html


import json
import urllib

#Hipchat Configuration

#Hipchat Token
V2_TOKEN = 'Change Me'

#Room Number, get from Hipchat Web App
ROOM_ID = 12345

#From idenity

FROM = 'ThePlatform'


def lambda_handler(event, context):
    #Get recieved event type
    event_type = event['detail-type']

    #Route to correct message formatter

    if event_type == 'Glue Job State Change':
        glue_job_message_processor(event)
    
    elif event_type == 'Glue Crawler State Change':
        glue_crawler_message_processor(event)
    
    elif event_type == 'CodeBuild Build State Change':
        code_build_message_processor(event)

    elif event_type == 'CodePipeline Pipeline Execution State Change':
        code_pipeline_pipeline_message_processor(event)

    else:
        print(f'Event type: {event_type} is not currently supported, please add it.')

def state_to_color(state, hipchat_message):

    #The different services annoyingly use different variants of "state", this function covers it.

    if state.upper() == 'FAILED':
        post_to_hipchat(hipchat_message, 'red')

    elif state.upper() == 'STARTED':
        post_to_hipchat(hipchat_message, 'yellow')
    
    elif state.upper() == 'STOPPED':
        post_to_hipchat(hipchat_message, 'orange')
    
    else:
        post_to_hipchat(hipchat_message, 'green')

def glue_job_message_processor(event):

    jobName = event['detail']['jobName']
    jobRunId = event['detail']['jobRunId']
    state = event['detail']['state'].upper()

    hipchat_message = f'{state}: Glue Job: {jobName}, ID: {jobRunId}'
    
    state_to_color(state, hipchat_message)

def glue_crawler_message_processor(event):

    crawlerName = event['detail']['crawlerName']
    errorMessage = event['detail']['errorMessage']
    state = event['detail']['state'].upper()

    hipchat_message = f'{state}: Crawler: {crawlerName}, Error: {errorMessage}'
    
    state_to_color(state, hipchat_message)


def code_build_message_processor(event):

    state = event['detail']['build-status'].upper()
    project_name = event['detail']['project-name']
    build_id = event['detail']['build-id']

    hipchat_message = f'{state}: Build Project: {project_name} Build ID: {build_id}' 
    
    state_to_color(state, hipchat_message)

def code_pipeline_pipeline_message_processor(event):

    state = event['detail']['state'].upper()
    pipeline_name = event['detail']['pipeline']
    execution_id = event['detail']['execution-id']

    hipchat_message = f'{state}: Pipeline: {pipeline_name} Execution ID: {execution_id}' 
    
    state_to_color(state, hipchat_message)

def post_to_hipchat(message, color):
    
    # Use Hipchat API V2 to send message to room id:
    url = 'https://api.hipchat.com/v2/room/%d/notification' % ROOM_ID
    
    headers = {
        "content-type": "application/json",
        "authorization": "Bearer %s" % V2_TOKEN}
    
    data = json.dumps({
        'message': message,
        'color': color,
        'message_format': 'html',
        'notify': False,
        'from': FROM })
    
    #Hipchat message data must be encoded.
    binary_data = data.encode('UTF-8')
    
    request = urllib.request.Request (url, headers=headers, data=binary_data)

    uo = urllib.request.urlopen(request)
    uo.close()
    
    #Check for 204 response code to confirm post.
    assert uo.code == 204

