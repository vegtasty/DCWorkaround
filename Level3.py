from Level.LevelInterface import LevelIF


class Level3(LevelIF):
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
        print('Level 3 start')

        Step.forbidden_steps = ["BT01", "BT02"]
        Step.sensor_queue = []

        Step("KP01", "1024")
        # Step.Step("KP01", "0")

        Step("KP02", "1024")
        # Step.Step("KP02", "0")

        Step("KP03", "1024")
        # Step.Step("KP03", "0")

        Step("KP04", "1024")
        # Step.Step("KP05", "0")

        print("Level Done")