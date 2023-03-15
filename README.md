# PathologyIDP

This application creates a step functions state machine to classify and extract information from pathology documents. 

## Workflow 

![Workflow architecture](/images/workflow-img.png)

## Requirements 

- AWS account 
- [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

## Deployment 

To deploy this application
1. Create a classifier using [workflow1](https://github.com/aws-samples/aws-document-classifier-and-splitter). 
2. git clone this repo
3. cd pathologyIDP
4. Run the following commands: 

```bash 
sam build 
sam deploy --guided 
``` 

## Testing 

To test the workflow, navigate to step functions console and click on start execution on the DocumentWorkflowStatemachine-XXXX statemachine that is created. 

In the Input - optional window, provide the S3 prefix of the test document. 

For example: 

{
    "Document": "medical-records/test-documents/mammogram1.png"
}

You can visualize the steps in the workflow as they execute. The output of each step can be seen on the console. 
