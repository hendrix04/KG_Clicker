import pprint, os
from pathlib import Path
from lib.vnc import VNC
from lib.kingdom_clicker import KingdomClicker


pp = pprint.PrettyPrinter(indent=4)


# Notable Locatons (Pixel 3 related)
# Dimentional tunnel from main screen =  300, 1865
# Dragon present from main screen = 645, 225
# Alliance tab from home screen = 815, 2080
# Main tab = 85, 2085
# Login X top left - 968, 343
# Recent apps = CTRL-SHFT-ESC


def main():
    # setup temp dir
    Path("./tmp").mkdir(parents=True, exist_ok=True)
    # client = api.connect("192.168.86.125", password=None)
    # client.timeout = 10
    # client.captureScreen("./pix_3/tmp/ss.png")
    kc = KingdomClicker(VNC(), "pixel_3.json")
    # kc.client.GetScreenshot(kc.device["tmp"])
    kc.AttackMith(0)
    # This is where we decide which function set to call into
    # Currently we only have adv mith and can't currently
    # get from desktop to game... That is coming though.
    # DoAdvMith()

    kc.client.client.disconnect()
    os._exit(0)


# def DoAdvMith():
#     # First, make sure none of our heroes are on the map...

#     # Now look for empty spots to go into
#     for i in range(5):
#         FindAndEnterMith()

if __name__ == "__main__":
    main()
