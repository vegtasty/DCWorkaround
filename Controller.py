import datetime
import time


class Sensor:
    def __init__(self, name, parent):
        self.__state = '0'
        self.name = name
        self.__lastChanged = datetime.datetime.now()
        self.parent = parent

    def get_current_state(self):
        self.__lastChanged = datetime.datetime.now()
        return self.__state

    def set_state(self, state):
        self.__state = state
        self.__lastChanged = datetime.datetime.now()
        return self.__state, self.__lastChanged


class Controller:
    controller_list = []

    def __init__(self, name):
        self.name = name
        self.sensors = [
            Sensor("BT01", name),
            Sensor("BT02", name),
            Sensor("KP01", name),
            Sensor("KP02", name),
            Sensor("KP03", name),
            Sensor("KP04", name),
            Sensor("PM01", name),
            Sensor("SW01", name),
        ]
        Controller.controller_list.append(self)

    def __del__(self):
        Controller.controller_list.remove(self)
        print("destructor" + self.__str__())

    def change_sensor_state(self, sensor_name, state):
        print('Change sensor ', sensor_name, 'with state ', state)
        for sensor in self.sensors:
            if sensor.name == sensor_name:
                sensor.set_state("1024")
                from Step import Step
                Step.sensor_queue.append(sensor)
                sensor.set_state("0")
                return


if __name__ == '__main__':
    Controller('DV01')
    controller = Controller('DV02')
    Controller('DV03')
    controller.__del__()
    print(Controller.controller_list)
