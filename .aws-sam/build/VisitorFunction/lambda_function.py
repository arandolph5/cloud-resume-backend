import json, os, boto3

dynamodb = boto3.resource("dynamodb", region_name="us-west-1")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def handler(event, context):
    method = (event.get("requestContext", {}).get("http", {}).get("method", "GET"))
    key = {"pk": "visitors"}

    if method == "POST":
        table.update_item(
            Key=key,
            UpdateExpression="SET #c = if_not_exists(#c, :zero) + :one",
            ExpressionAttributeNames={"#c": "count"},
            ExpressionAttributeValues={":zero": 0, ":one": 1},
        )

    resp = table.get_item(Key=key)
    count = resp.get("Item", {}).get("count", 0)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
            "Access-Control-Allow-Headers": "content-type",
        },
        "body": json.dumps({"count": count}),
    }

# make the name the tests expect:
lambda_handler = handler