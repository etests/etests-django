import boto3
from botocore.exceptions import ClientError
from env import EMAIL_ID, AWS_REGION


def send_email(
    to_email,
    subject,
    body_html,
    from_email="eTests<noreply@etests.co.in>",
    charset="UTF-8",
):
    client = boto3.client("ses", region_name=AWS_REGION)
    try:
        response = client.send_email(
            Destination={"ToAddresses": [to_email]},
            Message={
                "Body": {"Html": {"Charset": charset, "Data": body_html}},
                "Subject": {"Charset": charset, "Data": subject},
            },
            Source=from_email,
            ConfigurationSetName="EmailDelivery",
        )
    except ClientError as e:
        print(e.response["Error"]["Message"])
        return False
    else:
        print("Email sent! Message ID:"),
        print(response["MessageId"])
        return True
