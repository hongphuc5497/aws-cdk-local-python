import json

def handler(event, context):
    print("event request: {}".format(json.dumps(event)))
    message = "CDK Step Functions Lambda Example, event request: {}".format(event['path'])

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": message
        }),
    }
