from vncdotool import api
from time import sleep


class VNC:
    """This will add VNC specific logic to our framework."""

    client = None

    def __init__(self):
        self.client = api.connect("192.168.86.125", password=None)
        self.client.timeout = 30

    # The built in mouseClick didn't move the mouse nor did it add a
    # delay between press and release so I created my own wrapper
    def MouseClick(self, x: int, y: int):
        self.client.mouseMove(x, y)
        self.client.mouseDown(1)  # 1 is left button here
        sleep(0.05)
        self.client.mouseUp(1)

    def GetScreenshot(self, save_path):
        try:
            self.client.captureScreen(save_path)
        except TimeoutError:
            print("Timeout when capturing screen")
