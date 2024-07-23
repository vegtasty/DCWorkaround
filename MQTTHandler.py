import json
import random
import threading

from paho.mqtt import client as mqtt_client


def publish(client, topic, msg):
    y = json.loads(msg)
    msg = json.dumps(y)
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


class MQTTHandler(threading.Thread):
    def __init__(self):
        super().__init__()
        self.client = None
        self.client_id = None
        self.port = None
        self.broker = None

    def subscribe(self, client: mqtt_client, topic):
        def on_message(client, userdata, msg):
            from DefuseCode import DefuseCode

            if msg.topic == 'CONTROLLER/ACTION':
                m_in = json.loads(msg.payload.decode())
                controller_name = m_in['controller']
                controller_sensor = m_in['action_device']
                controller_sensor_value = m_in['action_value']
                if 'DV' in controller_name:
                    if 'LGIN' in controller_sensor:
                        DefuseCode().add_controller(controller_name)
                    elif 'LGOF' in controller_sensor:
                        DefuseCode().remove_controller(controller_name)
                    elif 'BT' in controller_sensor:
                        for controller in DefuseCode().controllers:
                            if controller.name == controller_name:
                                controller.change_sensor_state(controller_sensor, controller_sensor_value)
                    else:
                        print(int(controller_name[2:4]) - 1)
                        controller = DefuseCode().get_controller(int(controller_name[2:4]) - 1)
                        controller.change_sensor_state(controller_sensor, controller_sensor_value)
                # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic `")
            elif msg.topic == 'CONTROLLER/DEMO':
                print(DefuseCode().controllers[0].sensors[0].name)

        client.subscribe(topic)
        client.on_message = on_message

    def run(self):
        def connect_mqtt(client_id, broker, port):
            def on_connect(client, userdata, flags, rc):
                if rc == 0:
                    print("Connected to MQTT Broker!")
                else:
                    print("Failed to connect, return code %d\n", rc)

            client = mqtt_client.Client(client_id)
            # client.username_pw_set(username, password)
            client.on_connect = on_connect
            client.connect(broker, port)
            return client

        self.broker = '127.0.0.1'
        self.port = 1883
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'
        try:
            self.client = connect_mqtt(self.client_id, self.broker, self.port)
            self.subscribe(self.client, 'CONTROLLER/#')
            self.client.loop_forever()
        except:
            print("MQTT Error")
