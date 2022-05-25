from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
from datetime import datetime
import json
import time
import RPi.GPIO as GPIO
import time

ENDPOINT = "a2jv0zm6reglkj-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "iot_people_counter"
PATH_TO_CERT = "/home/vaughan/Documents/a3certs/f7236a911e1f35ad84eba3a369a6308c3ea24a4befbfbfd1e1ecc4c9f79994ce-certificate.pem.crt"
PATH_TO_KEY = "/home/vaughan/Documents/a3certs/f7236a911e1f35ad84eba3a369a6308c3ea24a4befbfbfd1e1ecc4c9f79994ce-private.pem.key"
PATH_TO_ROOT = "/home/vaughan/Documents/a3certs/AmazonRootCA1 (3).pem"
SENSOR_ID = "1"
TOPIC = "device/" +SENSOR_ID + "/data"
LED_PIN = 16
PIR_PIN = 12
IR_PIN = 19
IR_END = 0
sum_total = 0
with open('./counter.csv', 'r') as f:
    sum_total = int(f.read())
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(LED_PIN, GPIO.OUT)         #LED output pin
GPIO.setup(IR_PIN, GPIO.OUT)         #LED output pin
GPIO.add_event_detect(PIR_PIN, GPIO.BOTH, bouncetime=5)

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

def pir_rx():
    global sum_total, IR_END
    while True:
        if GPIO.event_detected(PIR_PIN):
            #time.sleep(0.005)
            if GPIO.input(PIR_PIN) == 1:
                print("rising")
                night = False
                now = datetime.now()
                if now.hour > 17 or now.hour < 7:
                    GPIO.output(IR_PIN, 1)
                    IR_END = now.hour+1
                    night = True
                else:
                    GPIO.output(LED_PIN, 1)
                dtg = now.strftime("%Y-%d-%m %H:%M:%S")
                sum_total+=1
                JSONTemplate = {
                   "timestamp":dtg,
                   "storeName":"Albany Store",
                   "deviceType":"Door-Mount-PIR",
                   "cumulativeCount":sum_total,
                   "activation":"rising",
                   "night":night
                }
                print(night)
                print("Sending data")
                sendData(JSONTemplate)
                with open('./counter.csv', 'w') as f:
                    f.write(str(sum_total))
            else:
                print("falling")
                GPIO.output(LED_PIN, 0)
                if now.hour > IR_END:
                    GPIO.output(IR_PIN, 0)
                    IR_END = 0


pir_rx()

