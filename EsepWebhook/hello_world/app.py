import os
import json
import logging
import urllib.request


def lambda_handler(event, context):
    # Log event for debugging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info(f"FunctionHandler received: {event}")

    # Parse incoming JSON
    if "body" in event:
        body = json.loads(event["body"])
    else:
        body = event

    # Find issue URL
    issue_url = body["issue"]["html_url"]

    # Preapare payload
    payload = json.dumps({
        "text": f"Issue Created: {issue_url}"
    }).encode("utf-8")
    slack_url = os.environ["SLACK_URL"]

    # Make Slack API call
    req = urllib.request.Request(
        slack_url,
        data=payload,
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req) as res:
        result = res.read().decode("utf-8")

    return {
        "statusCode": 200,
        "body": result
    }
