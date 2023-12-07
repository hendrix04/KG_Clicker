from vncdotool import api
from time import sleep
from random import randint


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
        sleep(0.05)
        self.client.mouseDown(1)  # 1 is left button here
        sleep(0.1)
        self.client.mouseUp(1)

    def MouseClickRandom(self, x1: int, x2: int, y1: int, y2: int):
        x = randint(x1, x2)
        y = randint(y1, y2)
        self.MouseClick(x, y)

    # You will want a small step for percise movement such as potitioning a haka
    # or a big step for swiping things away.
    def Scroll(
        self,
        startX: int,
        startY: int,
        endX: int,
        endY: int,
        step: int = 0,
        delay: float = 0.01,
    ):
        self.client.mouseMove(startX, startY)
        sleep(delay)
        self.client.mouseDown(1)

        while abs(startX - endX) > step or abs(startY - endY) > step:
            if abs(startX - endX) > step:
                if startX > endX:
                    startX -= step
                else:
                    startX += step

            if abs(startY - endY) > step:
                if startY > endY:
                    startY -= step
                else:
                    startY += step

            self.client.mouseMove(startX, startY)
            sleep(delay)

        self.client.mouseUp(1)
        return True

    def GetScreenshot(self, save_path):
        try:
            self.client.captureScreen(save_path)
        except TimeoutError:
            print("Timeout when capturing screen")

    def Disconnect(self):
        # Not really needed but makes my code cleaner...
        self.client.disconnect()

    def KeyPress(self, key):
        self.client.keyPress(key)
