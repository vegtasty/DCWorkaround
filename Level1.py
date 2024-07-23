import abc

from Level.LevelInterface import LevelIF


class Level1(LevelIF):
    def __init__(self):
        super().__init__()
        self.steps = None

    def init_level(self, controllers):
        self.steps = []
        print('Level Demo init')

    def run(self):
        from UserInterface import GameWindow
        from Step import Step
        GameWindow.set_max_steps(4)
        print('Level 1 start')

        Step.forbidden_steps = []
        Step.sensor_queue = []

        Step("KP02", "1024")
        # Step.Step("KP02", "0")

        Step("KP04", "1024")
        # Step.Step("KP04", "0")

        Step("KP01", "1024")
        # Step.Step("KP01", "0")

        Step("KP03", "1024")
        # Step.Step("KP03", "0")

        print("Level Done")