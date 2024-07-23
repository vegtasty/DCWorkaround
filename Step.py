import time


class Step:
    sensor_queue = []
    forbidden_steps = []

    def __init__(self, sensor_name, sensor_value):
        self.sensor_name = sensor_name
        self.sensor_value = sensor_value
        self.run_step()

    def run_step(self):
        print("runStep")
        while True:
            # if level ended
            from DefuseCode import DefuseCode
            from UserInterface import GameWindow
            if DefuseCode.interrupt:
                return
            for sensor in Step.sensor_queue:
                print(sensor.name, sensor.get_current_state(), "COUNT", GameWindow.current_step)
                # if input is vorbidden
                if sensor.name in Step.forbidden_steps:
                    DefuseCode.interrupt = True
                    return
                # if input is valid
                if sensor.name == self.sensor_name:
                    print("Test: ", sensor.name, sensor.get_current_state())
                    # if str(sensor.get_current_state()) == str(self.sensor_value):
                    print('Processed Step')
                    # src.Level.LevelDemo.LevelDemo.current_step += 1
                    GameWindow.current_step += 1
                    return
            Step.sensor_queue = []
