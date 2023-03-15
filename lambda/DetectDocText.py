import json
import os
import textractcaller as tc
from textractprettyprinter.t_pretty_print import get_lines_string
import boto3
import trp.trp2 as t2

textractClient = boto3.client('textract')
InputLocation = os.getenv('INPUTBUCKET', None)


def lambda_handler(event, context):
    print(event)
    
    q1 = tc.Query(text="What is the test result or diagnosis?", alias="test-result", pages=["1"])
    q2 = tc.Query(text="Is there a tumor?", alias="tumor", pages=["1"])
    q3 = tc.Query(text="What is Bi-rads score?", alias="bi-rads", pages=["1"])
    
    textract_json = tc.call_textract(
        input_document="s3://{}/{}".format(
            InputLocation, event["Document"]),
        queries_config=tc.QueriesConfig(queries=[q1, q2, q3]),
        features=[tc.Textract_Features.QUERIES],
        force_async_api=True,
        boto3_textract_client=textractClient)
    t_doc: t2.TDocument = t2.TDocumentSchema().load(textract_json)  # type: ignore
    answers = []
    for page in t_doc.pages:
        query_answers = t_doc.get_query_answers(page=page)
        for x in query_answers:
            qa = {x[1]: x[2]}
            # print(type(qa))
            # print(qa)
            print(f"{x[1]}:{x[2]}")
            answers.append(qa)

    return {
        'statusCode': 200,
        'body': json.loads(json.dumps(answers))
    }
