from abc import ABC, abstractmethod


class Listener(ABC):
    @abstractmethod
    def listen_for_speech(self):
        """
        Listen on the specified input device and return the text.
        :return: the text heard.
        """
