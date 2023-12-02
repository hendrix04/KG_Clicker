import cv2, pprint, os, json
from PIL import Image
from pathlib import Path
import numpy as np
from time import sleep
from random import randint


class KingdomClicker:
    """Kingdom Clicker framework! Making automation for KG Easier"""

    def __init__(self, client, device):
        # A client that matches what the VNC class provides function wise
        self.client = client
        self.device = json.load(open("./resources/devices/" + device))
        self.templatePath = "./resources/devices/" + self.device["folder"] + "/"

    def ClearMith(self):
        for i in range(5):
            # TODO: Update this to use config file
            self.client.MouseClick(150, 2000)  # Bottom left character slot in mith
            sleep(1.5)
            self.client.MouseClick(380, 1175)
            sleep(1.5)

    def AttackMith(self, index=None):
        templates = self.device["locations"]["mith"]["templates"]
        spots = self.device["locations"]["mith"]["spots"]
        location = {} if index is None else spots[index]
        mine = self.FindLocation(templates["spots"], 0.8, location)

        if mine["found"]:
            self.client.MouseClick(mine["left"] + 100, mine["bottom"])
            sleep(1)

        attack = self.FindLocation(templates["attack"], 0.9)

        if attack["found"]:
            self.client.MouseClick(attack["randomX"], attack["randomY"])
            sleep(1)

            depart = self.FindLocation(templates["depart"], 0.9)

            if depart["found"]:
                self.client.MouseClick(depart["randomX"], depart["randomY"])
                # It looks like the victory banner might be messing
                # up our image detection. This is why this sleep is longer
                sleep(5)

    # TODO: Add wait / retry logic to FindLocation
    def FindLocation(self, templateFile: str, threshold: float, crop: dict = {}):
        self.client.GetScreenshot(self.device["tmp"])
        templatePath = self.templatePath + templateFile

        screenshot = cv2.imread(self.device["tmp"], cv2.IMREAD_GRAYSCALE)

        if len(crop) > 0:
            screenshot = screenshot[
                crop["top"] : crop["bottom"], crop["left"] : crop["right"]
            ]

        template = cv2.imread(templatePath, cv2.IMREAD_GRAYSCALE)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        # print(loc)

        if len(loc[0]) > 0:
            data = {
                "found": True,
                "top": loc[0][-1],
                "left": loc[1][-1],
                "bottom": loc[0][-1] + h,
                "right": loc[1][-1] + w,
            }

            if len(crop) > 0:
                data["top"] += crop["top"]
                data["bottom"] += crop["top"]
                data["left"] += crop["left"]
                data["right"] += crop["left"]

            # Let's get a quarter of our template size and use that as
            # bounding for our random numbers
            xoffset = int(w / 4)
            yoffset = int(h / 4)

            randomBounding = {
                "top": data["top"] + yoffset,
                "left": data["left"] + xoffset,
                "bottom": data["bottom"] - yoffset,
                "right": data["right"] - xoffset,
            }

            data["randomY"] = randint(randomBounding["top"], randomBounding["bottom"])
            data["randomX"] = randint(randomBounding["left"], randomBounding["right"])

            return data

        return {"found": False}
