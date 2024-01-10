import cv2
import numpy as np
from time import sleep, strftime
from random import randint


# Note, All public methods (aka actions) should return a boolean so that our orchestrator
# knows if a particular task has succeeded for failed.
class KingdomClicker:
    """Kingdom Clicker framework! Making automation for KG Easier"""

    # These are fed directly to sleep()....
    retryDelay = 1  # How long to wait until we try an image match again.
    # TODO: This is clickDelay a good idea, but it ya know, needs to be used somewhere.
    clickDelay = 1  # How long to wait after making a click

    def __init__(self, client, device, logger):
        logger.info("Initiating KingdomClicker")
        # A client that matches what the VNC class provides function wise
        self.client = client
        self.device = device
        self.locations = self.device["locations"]
        self.templatePath = f'./resources/devices/{self.device["folder"]}/'
        self.defaultCrop = {
            "left": 0,
            "right": self.device["width"],
            "top": 0,
            "bottom": self.device["height"],
        }
        self.logger = logger

    # TODO: Make this more robust with image detection
    # - Check if left most hero slot is empty
    # - if so we are done
    # - If not, keep looping through clearing that first spot until it is empty
    def ClearMith(self):
        self.logger.info("Clearing Mith")
        for i in range(5):
            # TODO: Update this to use config file
            self.client.MouseClick(150, 2000)  # Bottom left character slot in mith
            sleep(1.5)
            self.client.MouseClick(380, 1175)
            sleep(1.5)

        return True

    # EnterAdvMith:
    # - Find Dimensional Tunnel in the castle view
    # - Click on Dimensional Tunnel
    # - Click on Advanced Mithril
    def EnterMith(self, level: str = "advMith"):
        self.logger.info("Entering Mith")
        castle = self.locations["castle"]
        castleTemplates = castle["templates"]
        mithLocation = self.locations["mith"][level]
        tunnel = self.__FindLocation(castleTemplates["tunnel"], crop=castle["tunnel"])

        if tunnel["found"]:
            self.client.MouseClick(tunnel["randomX"], tunnel["randomY"])
            sleep(3)
            # TODO: We SHOULD add image detection here
            self.client.MouseClickRandom(
                x1=mithLocation["left"],
                x2=mithLocation["right"],
                y1=mithLocation["top"],
                y2=mithLocation["bottom"],
            )
            sleep(3)

            return True
        return False

    # TODO: Decide if this should be private with a smarter "action" function
    def AttackMith(self, level: str = "advMith", index=None):
        self.logger.info("Attacking Mith")
        mith = self.locations["mith"]
        templates = mith["templates"]
        spots = mith["spots"]
        location = {} if index is None else spots[index]
        mine = self.__FindLocation(templates[level], crop=location)

        if mine["found"]:
            self.client.MouseClick(mine["left"] + 100, mine["bottom"])
        else:
            return False

        sleep(1)

        attack = self.__FindLocation(templates["attack"])

        if attack["found"]:
            self.client.MouseClick(attack["randomX"], attack["randomY"])
            sleep(1)

            depart = self.__FindLocation(templates["depart"])

            if depart["found"]:
                self.client.MouseClick(depart["randomX"], depart["randomY"])
                sleep(1)

        return True

    def EnterGame(self):
        self.logger.info("Entering Game")
        menu = self.locations["menu"]
        menuTemplates = menu["templates"]
        ads = self.locations["ads"]
        adsTemplates = ads["templates"]
        gameLoc = self.locations["desktop"]["game"]
        self.client.MouseClick(gameLoc["x"], gameLoc["y"])
        inGame = False
        inGameAttempts = 0

        # Wait for a few seconds then try to start detecting a possible marketing X...
        # We likely want to make this a TAD smarter by looking for something besides
        # the X first as the X isn't always there and it could create significant delay
        # for entering the game...
        # Let's start with a 30 second sleep and then start trying to figure out what
        # we need to do next...
        sleep(30)

        # We are going to jump back and forth checking between the castle in the lower
        # left and the X in the upper right. Once one is detected, we know where to go
        # from there... On even loops we will check the X, on odd, the castle
        while not inGame:
            # Failsafe in case servers are down or something.
            # TODO: Better detection of failure case
            if inGameAttempts >= 5:
                self.logger.info("Failed to get into game")
                self.TakeSS(strftime("%Y-%m-%d_%H-%M-%S"))
                return False

            if inGameAttempts % 2 == 0:
                findLocationOutput = {
                    "type": "x",
                    "data": self.__FindLocation(
                        adsTemplates["exit"],
                        crop=ads["exit"],
                    ),
                }
            else:
                findLocationOutput = {
                    "type": "present",
                    "data": self.__FindLocation(
                        menuTemplates["present"],
                        crop=menu["present"],
                    ),
                }

            if findLocationOutput["data"]["found"]:
                # We need to know which one we found...
                if findLocationOutput["type"] == "x":
                    # First close the box that we found...
                    self.client.MouseClick(
                        findLocationOutput["data"]["randomX"],
                        findLocationOutput["data"]["randomY"],
                    )
                    sleep(3)

                    # Because there can potentially be multiple windows to close, let's
                    # now loop through until we find no more X icons...
                    foundX = True
                    foundXAttempts = 0
                    while foundX:
                        self.logger.info("Found X, looking for more")
                        sleep(5)
                        if foundXAttempts > 10:
                            print("Failed to finish closing X")
                            return False

                        findExOutput = self.__FindLocation(
                            adsTemplates["exit"],
                            crop=ads["exit"],
                        )

                        if findExOutput["found"]:
                            self.client.MouseClick(
                                findExOutput["randomX"],
                                findExOutput["randomY"],
                            )
                        else:
                            foundX = False

                        foundXAttempts += 1
                else:
                    # No adds! Yay! Click on the castle to get us to our
                    # default starting position
                    castleOutput = self.__FindLocation(
                        menuTemplates["castle"],
                        crop=menu["castle"],
                    )
                    sleep(3)
                    self.client.MouseClick(
                        castleOutput["randomX"],
                        castleOutput["randomY"],
                    )
                    inGame = True
                    self.logger.info("We should be fully in game now")

            inGameAttempts += 1

        return True

    # We are getting aggressive now... The reason we need to ensure that the game is
    # fully closed is because sometimes the game gets stuck where it cannot connect
    # to the servers. The only way to resolve this is to ensure that the game is totally
    # closed so that it is forced to open a net new connection each time.

    # - open app switcher
    # - Detect if KG is open by looking for icon
    # - Long press icon
    # - Go into app details
    # - force close the app
    def ExitGame(self):
        self.logger.info("Exit Game")
        desktop = self.locations["desktop"]


        self.client.KeyPress("ctrl-shift-esc")
        sleep(0.75)
        icon = self.__FindLocation(
            desktop["templates"]["gameIcon"],
            crop=desktop["gameIcon"],
        )

        if icon["found"]:
            self.logger.info("Found icon to exit")
            self.client.MouseClick(x=icon["randomX"], y=icon["randomY"], delay=1.5)
            sleep(1)
            self.client.MouseClick(desktop["appInfo"]["x"], desktop["appInfo"]["y"])
            sleep(1)
            self.client.MouseClick(desktop["forceQuit"]["x"], desktop["forceQuit"]["y"])
            sleep(1)
            self.client.MouseClick(desktop["confirm"]["x"], desktop["confirm"]["y"])
            sleep(1)

        self.client.KeyPress("home")

    # Click into Cornucopia
    # Search for template
    # Click on template
    # Click on Go
    def EnterEvent(self, template: str):
        events = self.locations["events"]
        templates = events["templates"]

        cornucopia = self.__FindLocation(
            templates["cornucopia"],
            crop=events["cornucopia"],
            maxRetry=3
        )

        if cornucopia["found"]:
            self.client.MouseClick(
                cornucopia["randomX"],
                cornucopia["randomY"],
            )
            sleep(3)

            event = self.__FindLocation(
                templates[template],
                maxRetry=3
            )

            if event["found"]:
                self.client.MouseClick(
                    event["randomX"],
                    event["randomY"],
                )
                sleep(3)

                goBtn = self.__FindLocation(
                    templates["go"],
                    maxRetry=3
                )

                if goBtn["found"]:
                    self.client.MouseClick(
                        goBtn["randomX"],
                        goBtn["randomY"],
                    )

                    return True

        return False



    # If Alliance: Search for Alliance tab & Click
    # Search for blue summon & click
    # Move Haka
    # Search for Yellow summon & Click
    # If Alliance: Search for share icon & click
    # If Alliance: Search for alliance button & click
    # Search for Rally & Click
    # Search for Depart & Click
    def SummonHaka(self, is_alliance: bool):
        events = self.locations["events"]
        templates = events["templates"]

        if is_alliance:
            alliance = self.__FindLocation(
                templates["alliance_challenge"],
                crop=events["alliance"],
                maxRetry=3
            )
            
            if alliance["found"]:
                self.client.MouseClick(
                    alliance["randomX"],
                    alliance["randomY"],
                )

                sleep(1)
                for i in range(50):
                    checkSummonBlue = self.__FindLocation(
                        templates["summon_blue"],
                        crop=events["summon_blue"],
                        maxRetry=3
                    )
            
                    if checkSummonBlue["found"]:
                        self.logger.info("summoning another haka")
                        break;
                    else:
                        sleep(15)
        
        summonBlue = self.__FindLocation(
            templates["summon_blue"],
            crop=events["summon_blue"],
            maxRetry=3
        )
        
        if summonBlue["found"]:
            self.client.MouseClick(
                summonBlue["randomX"],
                summonBlue["randomY"],
            )

            sleep(2)
            self.client.Scroll(**events["haka_move"])
            sleep(1)

            summonYellow = self.__FindLocation(
                templates["summon_yellow"],
                crop=events["summon_yellow"],
                maxRetry=3
            )
            
            if summonYellow["found"]:
                self.client.MouseClick(
                    summonYellow["randomX"],
                    summonYellow["randomY"],
                )

                sleep(2)

                self.client.MouseClick(
                    x=events["haka_move"]["endX"],
                    y=events["haka_move"]["endY"]
                )

                sleep(1)

                if is_alliance:
                    hakaShare = self.__FindLocation(
                        templates["haka_share"],
                        #crop=events["haka_share"],
                        maxRetry=3
                    )
                    
                    if hakaShare["found"]:
                        self.client.MouseClick(
                            hakaShare["randomX"],
                            hakaShare["randomY"],
                        )

                        sleep(2)
                        self.client.MouseClickRandom(**events['alliance_share'])

                rally = self.__FindLocation(
                    templates["rally"],
                    crop=events["rally"],
                    maxRetry=3
                )
                
                if rally["found"]:
                    self.client.MouseClick(
                        rally["randomX"],
                        rally["randomY"],
                    )

                    sleep(2) 

                    depart = self.__FindLocation(
                        templates["depart"],
                        crop=events["depart"],
                        maxRetry=3
                    )
                    
                    if depart["found"]:
                        self.client.MouseClick(
                            depart["randomX"],
                            depart["randomY"],
                        )

                        return True
        else:
            goBtn = self.__FindLocation(
                templates["summon_yellow"],
                crop=events["summon_yellow"],
                maxRetry=3
            )

        return False

    def ViewWar(self):
        alliance = self.locations["alliance"]
        if self.__EnterAlliance():
            sleep(1)

            war = self.__FindLocation(
                alliance["templates"]["war"],
                crop=alliance["war"],
                maxRetry=3
            )
            
            if war["found"]:
                self.client.MouseClick(
                    war["randomX"],
                    war["randomY"],
                )
                return True
        return False

    def DetectMonster(self, template):
        self.logger.info(f'Detecting {template}')
        war = self.locations["war"]
        return self.__FindLocation(
            war["templates"][template],
            crop=war["monster"]
        )

    # Filename should not include an extension
    def TakeSS(self, fileName: str = ""):
        filePath = self.__GenerateFilePath(fileName)
        self.client.GetScreenshot(filePath)
        return True

    def __GoHome(self):
        menu = self.locations["menu"]

        castle = self.__FindLocation(
            menu["templates"]["castle"],
            crop=menu["castle"],
        )
        
        if castle["found"]:
            self.client.MouseClick(
                castle["randomX"],
                castle["randomY"],
            )
            return True

        # If we didn't find the castle, we could be in an
        # area with a bucket, OR we could already be on the
        # castle tab. Let's check for those 2 scenarios.
        backBtn = self.__FindLocation(
            menu["templates"]["back_btn"],
            crop=menu["back_btn"],
        )
        
        if backBtn["found"]:
            self.client.MouseClick(
                backBtn["randomX"],
                backBtn["randomY"],
            )

            sleep(1)

            # If we found the back button, we could be 
            # multiple buttons deep...
            return self.__GoHome()
        else:
            alliance = self.__FindLocation(
                menu["templates"]["alliance"],
                crop=menu["alliance"],
            )

            # If we find the alliance button, we should
            # also be able to click the castle button
            if alliance["found"]:
                self.client.MouseClickRandom(
                    x1=menu["castle"]["left"],
                    x2=menu["castle"]["right"],
                    y1=menu["castle"]["top"],
                    y2=menu["castle"]["bottom"]
                )

                return True

        return False

    def __EnterAlliance(self):
        if self.__GoHome():
            sleep(1)

            menu = self.locations["menu"]

            alliance = self.__FindLocation(
                menu["templates"]["alliance"],
                crop=menu["alliance"],
            )
            
            if alliance["found"]:
                self.client.MouseClick(
                    alliance["randomX"],
                    alliance["randomY"],
                )
                return True

        return False

    def __GenerateFilePath(self, fileName: str = ""):
        if fileName == "":
            return f'{self.device["tmp"]}/{self.device["folder"]}.png'
        else:
            return f'{self.device["tmp"]}/{self.device["folder"]}/{fileName}.png'

    def __FindLocation(
        self,
        templateFile: str,
        threshold: float = 0.9,
        crop: dict = {},
        maxRetry: int = 0,
    ):
        self.logger.info("Finding Location " + templateFile)
        # A little python magic to ensure we always have SOME crop values
        crop = {**self.defaultCrop, **crop}
        self.TakeSS()
        templatePath = f"{self.templatePath}/{templateFile}.png"
        self.logger.info("Loading Screenshot")
        screenshot = cv2.imread(self.__GenerateFilePath(), cv2.IMREAD_GRAYSCALE)
        screenshot = screenshot[
            crop["top"] : crop["bottom"], crop["left"] : crop["right"]
        ]

        self.logger.info("Loading Template")
        template = cv2.imread(templatePath, cv2.IMREAD_GRAYSCALE)
        w, h = template.shape[::-1]
        self.logger.info("Matching Template")
        res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        self.logger.info("Detecting Threshold")
        loc = np.where(res >= threshold)

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
            xOffset = int(w / 4)
            yOffset = int(h / 4)

            randomBounding = {
                "top": data["top"] + yOffset,
                "left": data["left"] + xOffset,
                "bottom": data["bottom"] - yOffset,
                "right": data["right"] - xOffset,
            }

            data["randomY"] = randint(randomBounding["top"], randomBounding["bottom"])
            data["randomX"] = randint(randomBounding["left"], randomBounding["right"])

            return data

        if maxRetry:
            sleep(self.retryDelay)
            maxRetry -= 1
            return self.__FindLocation(templateFile, threshold, crop, maxRetry)
        else:
            return {"found": False}
