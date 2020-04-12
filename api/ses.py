import boto3
from botocore.exceptions import ClientError
from django.conf import settings


def send_email(
    to_email,
    subject,
    body_html,
    from_email=f"eTests<{settings.DEFAULT_EMAIL_ID}>",
    charset="UTF-8",
):
    client = boto3.client("ses", region_name=settings.AWS_REGION)
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
