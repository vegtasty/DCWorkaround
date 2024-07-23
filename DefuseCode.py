import threading

from MQTTHandler import MQTTHandler
from UserInterface import UserInterface


class DefuseCode(object):
    instance = None
    interrupt = False

    def __new__(cls):
        if cls.instance is None:
            print('New instance')
            cls.instance = super(DefuseCode, cls).__new__(cls)
            cls.instance.mqtthandler = MQTTHandler()
            cls.instance.controllers = []
            cls.instance.ui = UserInterface()
            cls.current_level = None
        return cls.instance

    def start(self):
        print('Starting Defuse Code ...')
        self.mqtthandler.start()
        self.ui.run()

    def get_controller(self, index):
        return self.controllers[index]

    def add_controller(self, controller_name):
        controller_names = []
        for controller in self.controllers:
            controller_names.append(controller.name)
        if controller_name in controller_names:
            print('Controller already logged in')
        else:
            print('Controller login')
            from Controller import Controller
            self.controllers.append(Controller(controller_name))

    def remove_controller(self, controller_name):
        index = 0
        for controller in self.controllers:
            if controller.name == controller_name:
                self.controllers.pop(index)
                print(f"removed controller, lines: {len(self.controllers)}")
                return
        index += 1

    def set_sensor_state(self):
        pass


if __name__ == '__main__':
    DefuseCode().start()
