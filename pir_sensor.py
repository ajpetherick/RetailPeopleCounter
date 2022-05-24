from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
from datetime import datetime
import json
import time

ENDPOINT = "a2jv0zm6reglkj-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "iot_people_counter"
PATH_TO_CERT = "C:/Users/apetherick/Downloads/f7236a911e1f35ad84eba3a369a6308c3ea24a4befbfbfd1e1ecc4c9f79994ce-certificate.pem.crt"
PATH_TO_KEY = "C:/Users/apetherick/Downloads/f7236a911e1f35ad84eba3a369a6308c3ea24a4befbfbfd1e1ecc4c9f79994ce-private.pem.key"
PATH_TO_ROOT = "C:/Users/apetherick/Downloads/AmazonRootCA1 (3).pem"
SENSOR_ID = "1"
TOPIC = "device/" +SENSOR_ID + "/data"

def sendData(data):
    # Spin up resources
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=ENDPOINT,
        cert_filepath=PATH_TO_CERT,
        pri_key_filepath=PATH_TO_KEY,
        client_bootstrap=client_bootstrap,
        ca_filepath=PATH_TO_ROOT,
        client_id=CLIENT_ID,
        clean_session=False,
        keep_alive_secs=6
    )
    print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_ID))
    # Make the connect() call
    connect_future = mqtt_connection.connect()
    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")
    # Publish message to server desired number of times.
    print('Begin Publish')
    mqtt_connection.publish(topic=TOPIC, payload=json.dumps(data), qos=mqtt.QoS.AT_LEAST_ONCE)
    print("Published: '" + json.dumps(data) + "' to the topic: " + TOPIC)
    print('Publish End')
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()

dt = datetime.now()
store = 'Albany Store'
device_type ='Door Mount Sensor'
count = 30
voltage = 3.3
JSONPayload = {
   "timestamp":"{0}".format(dt),
   "storeName":"{0}".format(store),
   "deviceType":"{0}".format(device_type),
   "cumulativeCount":"{0}".format(count),
   "supplyVoltage":{
      "value":"{0}".format(voltage),
      "unit":"V"
   }
}

sendData(JSONPayload)