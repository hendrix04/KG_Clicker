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

    kc = KingdomClicker(VNC(), "pixel_3.json")

    kc.ClearMith()

    for i in range(5):
        kc.AttackMith(i)

    kc.client.client.disconnect()
    os._exit(0)


# def DoAdvMith():
#     # First, make sure none of our heroes are on the map...

#     # Now look for empty spots to go into
#     for i in range(5):
#         FindAndEnterMith()

if __name__ == "__main__":
    main()
