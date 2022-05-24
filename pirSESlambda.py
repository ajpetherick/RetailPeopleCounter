import boto3
from botocore.exceptions import ClientError
import csv
import datetime
import json
from operator import itemgetter


def lambda_handler(event, context):
    region = 'us-east-1'
    dynamodb = boto3.client('dynamodb', region_name=region)
    dynamodbResource = boto3.resource('dynamodb', region_name=region)

    sensorTable = dynamodbResource.Table('sensor_readings')
    sensorTableScan = sensorTable.scan()
    sensorData = sensorTableScan["Items"]
    userEmail = "a_petherick@hotmail.com"

    sensor_list = []
    for i in range(len(sensorData)):
        reading = sensorData[i]  # ["device_data"]
        sensor_list.append(reading)
        print("unsorted", reading)

    # sort ascending
    newlist = sorted(sensor_list, key=itemgetter('sample_time'), reverse=True)
    latest_reading = dict(newlist[0])

    time_stamp = latest_reading["device_data"]["timestamp"]
    cumulative_count = latest_reading["device_data"]["cumulativeCount"]
    device_name = latest_reading["device_data"]["deviceName"]
    device_type = latest_reading["device_data"]["deviceType"]

    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "admant85@gmail.com"

    # Replace recipient@example.com with a "To" address. If your account
    # is still in the sandbox, this address must be verified.
    RECIPIENT = "a_petherick@hotmail.com"

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    # CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"

    # The subject line for the email.
    SUBJECT = "Your latest people count"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                 "<p>People count: " + str(cumulative_count) + "</p>\r\n"

                 )

    # The HTML body of the email.
    BODY_HTML = """<html>
<head></head>
<body>
  <h2>Your PIR sensor data</h2>
  <p>Time: {0}</p>
  <p>People through the door: {1}</p>
  <p>Store: {2}</p>
  <p>Sesnor: {3}</p>
  <p>This email was sent with
    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
    <a href='https://aws.amazon.com/sdk-for-python/'>
      AWS SDK for Python (Boto)</a>.</p>
</body>
</html>
            """.format(time_stamp, cumulative_count, device_name, device_type)

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=AWS_REGION)

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])