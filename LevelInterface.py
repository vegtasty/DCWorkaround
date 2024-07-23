import abc
import threading


class LevelIF(abc.ABC, threading.Thread):

    @abc.abstractmethod
    def init_level(self, controllers):
        pass

    @abc.abstractmethod
    def run(self):
        pass