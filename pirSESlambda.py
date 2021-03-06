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
    store_name = latest_reading["device_data"]["storeName"]
    device_type = latest_reading["device_data"]["deviceType"]
    activation = latest_reading["device_data"]["activation"]

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
    BODY_TEXT = ("Your PIR sensor data\r\n"
                 "Time: {0} \r\n"
                 "People through the door: {1} \r\n"
                 "Store: {2} \r\n"
                 "Sesnor: {3} \r\n"
                 "Activation: {4} \r\n".format(time_stamp, cumulative_count, store_name, device_type, activation)
                 )

    # The HTML body of the email.
    BODY_HTML = """<html lang="en">
    <head>
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Audiowide">
<style>
body {{
  font-family: "Audiowide", sans-serif;
}}
</style>
</head>
<body>
  <div style="font-family: Arial, Helvetica, sans-serif;">
    <div style="max-width: 900px;display: block;margin-left: auto; margin-right: auto">
      <div style="max-width: 900px; background-color:#ffffff; border-radius: 12px;  box-shadow: 0 2px 5px 0 rgba(0,0,0,0.05); margin-bottom: 12px;">
        <div id="header" style="padding:12px; text-align: center;">
          <img style="vertical-align:middle;height: 45px; border-radius:50%; margin-bottom:.9em" src="https://image-bucket-small.s3.amazonaws.com/98f6f554405048c88d941c440d03089a.png"/>
          <span style="font-size: 1.8em; font-weight:600; margin-top:3em">Retail People Counter</span>
        </div>
        <div style="padding:12px; text-align: center; ">
          <img
            style="width: 80%; border-top-left-radius: 9pt;  border-top-right-radius: 9pt"
            src="https://images.pexels.com/photos/987209/pexels-photo-987209.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
          />
        </div>
        <div style="padding:3em 1.5em 6em 1.5em;">
          <h1 style="color:#151a22">Hello,</h1>


          <p style="color:#3a4758; font-size: 1.2em">
            Thank you for subscribing to Retail People Counter.
          </p>
          <p style="color:#3a4758; font-size: 1.2em">
            Today, as at {0} local time, you received {1} people through the door of your {2} location.
          </p>
          <p style="color:#3a4758; font-size: 1.2em">
            Thank you very much for using our people counting technology!
          </p>
        </div>


      </div>
    </div>
  </div>

  <div style="max-width: 900px;display: block;margin-left: auto; margin-right: auto">
  <table cellpadding="0"
       cellspacing="0"
       class="sc-gPEVay eQYmiW"
       style="vertical-align: -webkit-baseline-middle; font-size: medium; font-family: Arial;">
	<tbody>
		<tr>
			<td>
				<table cellpadding="0"
				       cellspacing="0"
				       class="sc-gPEVay eQYmiW"
				       style="vertical-align: -webkit-baseline-middle; font-size: medium; font-family: Arial;">
					<tbody>
						<tr>
							<td style="vertical-align: top;">
								<table cellpadding="0"
								       cellspacing="0"
								       class="sc-gPEVay eQYmiW"
								       style="vertical-align: -webkit-baseline-middle; font-size: medium; font-family: Arial;">
									<tbody>
										<tr>
											<td height="30"/>
										</tr>
										<tr>
											<td style="text-align: center;">
												<table cellpadding="0"
												       cellspacing="0"
												       class="sc-gPEVay eQYmiW"
												       style="vertical-align: -webkit-baseline-middle; font-size: medium; font-family: Arial; display: inline-block;">
													<tbody>
														<tr style="text-align: center;">
															<td>
																<a href="https://www.facbook.com/peoplecounters"
																   color="#6a78d1"
																   class="sc-hzDkRC kpsoyz"
																   style="display: inline-block; padding: 0px; background-color: rgb(106, 120, 209);">
																	<img src="https://cdn2.hubspot.net/hubfs/53/tools/email-signature-generator/icons/facebook-icon-2x.png"
																	     alt="facebook"
																	     color="#6a78d1"
																	     height="24"
																	     class="sc-bRBYWo ccSRck"
																	     style="background-color: rgb(106, 120, 209); max-width: 135px; display: block;"/>
																</td>
																<td width="5">
																	<div/>
																</td>
																<td>
																	<a href="https://twitter.com/peoplecounters"
																	   color="#6a78d1"
																	   class="sc-hzDkRC kpsoyz"
																	   style="display: inline-block; padding: 0px; background-color: rgb(106, 120, 209);">
																		<img src="https://cdn2.hubspot.net/hubfs/53/tools/email-signature-generator/icons/twitter-icon-2x.png"
																		     alt="twitter"
																		     color="#6a78d1"
																		     height="24"
																		     class="sc-bRBYWo ccSRck"
																		     style="background-color: rgb(106, 120, 209); max-width: 135px; display: block;"/>
																	</td>
																	<td width="5">
																		<div/>
																	</td>
																	<td>
																		<a href="https://www.peoplecounters.com"
																		   color="#6a78d1"
																		   class="sc-hzDkRC kpsoyz"
																		   style="display: inline-block; padding: 0px; background-color: rgb(106, 120, 209);">
																			<img src="https://cdn2.hubspot.net/hubfs/53/tools/email-signature-generator/icons/linkedin-icon-2x.png"
																			     alt="linkedin"
																			     color="#6a78d1"
																			     height="24"
																			     class="sc-bRBYWo ccSRck"
																			     style="background-color: rgb(106, 120, 209); max-width: 135px; display: block;"/>
																		</td>
																		<td width="5">
																			<div/>
																		</td>
																		<td>
																			<a href="https://www.instagram.com/peoplecounters"
																			   color="#6a78d1"
																			   class="sc-hzDkRC kpsoyz"
																			   style="display: inline-block; padding: 0px; background-color: rgb(106, 120, 209);">
																				<img src="https://cdn2.hubspot.net/hubfs/53/tools/email-signature-generator/icons/instagram-icon-2x.png"
																				     alt="instagram"
																				     color="#6a78d1"
																				     height="24"
																				     class="sc-bRBYWo ccSRck"
																				     style="background-color: rgb(106, 120, 209); max-width: 135px; display: block;"/>
																			</td>
																			<td width="5">
																				<div/>
																			</td>
																		</tr>
																	</tbody>
																</table>
															</td>
														</tr>
													</tbody>
												</table>
											</td>
											<td width="46">
												<div/>
											</td>
											<td style="padding: 0px; vertical-align: middle;">
												<h3 color="#000000"
												    class="sc-fBuWsC eeihxG"
												    style=" font-size: 18px; color: rgb(0, 0, 0);">
													<span>People</span>
													<span>&nbsp;</span>
													<span>Counters LTD</span>
												</h3>
												<table cellpadding="0"
												       cellspacing="0"
												       class="sc-gPEVay eQYmiW"
												       style="vertical-align: -webkit-baseline-middle; font-size: medium; font-family: Arial; width: 100%;">
													<tbody>
														<tr>
															<td height="30"/>
														</tr>
														<tr>
															<td color="#f2547d"
															    direction="horizontal"
															    height="1"
															    class="sc-jhAzac hmXDXQ"
															    style="width: 100%; border-bottom: 1px solid rgb(242, 84, 125); border-left: none; display: block;"/>
														</tr>
														<tr>
															<td height="30"/>
														</tr>
													</tbody>
												</table>
												<table cellpadding="0"
												       cellspacing="0"
												       class="sc-gPEVay eQYmiW"
												       style="vertical-align: -webkit-baseline-middle; font-size: medium; font-family: Arial;">
													<tbody>
														<tr height="25"
														    style="vertical-align: middle;">
															<td width="30"
															    style="vertical-align: middle;">
																<table cellpadding="0"
																       cellspacing="0"
																       class="sc-gPEVay eQYmiW"
																       style="vertical-align: -webkit-baseline-middle; font-size: medium; font-family: Arial;">
																	<tbody>
																		<tr>
																			<td style="vertical-align: bottom;">
																				<span color="#f2547d"
																				      width="11"
																				      class="sc-jlyJG bbyJzT"
																				      style="display: block; background-color: rgb(242, 84, 125);">
																					<img src="https://cdn2.hubspot.net/hubfs/53/tools/email-signature-generator/icons/email-icon-2x.png"
																					     color="#f2547d"
																					     width="13"
																					     class="sc-iRbamj blSEcj"
																					     style="display: block; background-color: rgb(242, 84, 125);"/>
																				</td>
																			</tr>
																		</tbody>
																	</table>
																</td>
																<td style="padding: 0px;">
																	<a href="mailto:counters@peoplecounters.com"
																	   color="#000000"
																	   class="sc-gipzik iyhjGb"
																	   style="text-decoration: none; color: rgb(0, 0, 0); font-size: 12px;">
																		<span>counters@peoplecounters.com</span>
																	</a>
																</td>
															</tr>
															<tr height="25"
															    style="vertical-align: middle;">
																<td width="30"
																    style="vertical-align: middle;">
																	<table cellpadding="0"
																	       cellspacing="0"
																	       class="sc-gPEVay eQYmiW"
																	       style="vertical-align: -webkit-baseline-middle; font-size: medium; font-family: Arial;">
																		<tbody>
																			<tr>
																				<td style="vertical-align: bottom;">
																					<span color="#f2547d"
																					      width="11"
																					      class="sc-jlyJG bbyJzT"
																					      style="display: block; background-color: rgb(242, 84, 125);">
																						<img src="https://cdn2.hubspot.net/hubfs/53/tools/email-signature-generator/icons/address-icon-2x.png"
																						     color="#f2547d"
																						     width="13"
																						     class="sc-iRbamj blSEcj"
																						     style="display: block; background-color: rgb(242, 84, 125);"/>
																					</td>
																				</tr>
																			</tbody>
																		</table>
																	</td>
																	<td style="padding: 0px;">
																		<span color="#000000"
																		      class="sc-csuQGl CQhxV"
																		      style="font-size: 12px; color: rgb(0, 0, 0);">
																			<span>Level 1, 1569 Wellington Road, Auckland, New Zealand</span>
																		</span>
																	</td>
																</tr>
															</tbody>
														</table>
														<table cellpadding="0"
														       cellspacing="0"
														       class="sc-gPEVay eQYmiW"
														       style="vertical-align: -webkit-baseline-middle; font-size: medium; font-family: Arial;">
															<tbody>
																<tr>
																	<td height="30"/>
																</tr>
															</tbody>
														</table>
													</td>
												</tr>
											</tbody>
										</table>
									</td>
								</tr>
							</tbody>
						</table>
						</div>
</body>

</html>
            """.format(time_stamp, cumulative_count, store_name)

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