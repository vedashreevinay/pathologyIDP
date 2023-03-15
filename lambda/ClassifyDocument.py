import json
import os
import textractcaller as tc
from textractprettyprinter.t_pretty_print import get_lines_string
import boto3

comprehendClient = boto3.client('comprehend')
s3Client = boto3.client('s3')
InputLocation = os.getenv('INPUTBUCKET', None)

def lambda_handler(event, context):
    print(event)
    
    #Download the document from S3 
    s3_response_object = s3Client.get_object(Bucket = InputLocation, Key = event['Document'])
    file_for_analysis = s3_response_object['Body'].read()
    
    comprehend_sync_response = comprehendClient.classify_document(
        EndpointArn='arn:aws:comprehend:us-east-1:291131278872:document-classifier-endpoint/Classifier-20230224181749',
        Bytes=file_for_analysis)
        
    print(comprehend_sync_response)
        
    #print(comprehend_response['Classes'])
    classes = comprehend_sync_response['Classes'] 

    class_name = max(classes, key=lambda x:x['Score'])
        
    print(class_name)
    
    return {
        'statusCode': 200,
        'class': class_name['Name'],
        'Score': class_name['Score']
    }
