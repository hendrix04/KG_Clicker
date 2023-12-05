import pprint, os
from time import sleep
from pathlib import Path
from lib.vnc import VNC
from lib.kingdom_clicker import KingdomClicker


pp = pprint.PrettyPrinter(indent=4)


# Notable Locations (Pixel 3 related)
# Dimensional tunnel from main screen =  300, 1865
# Dragon present from main screen = 645, 225
# Alliance tab from home screen = 815, 2080
# Main tab = 85, 2085
# Login X top left - 968, 343
# Recent apps = CTRL-SHFT-ESC


def main():
    # setup temp dir
    Path("./tmp").mkdir(parents=True, exist_ok=True)

    # Initiate the appropriate client... Right now we only have VNC
    client = VNC()

    kc = KingdomClicker(client, "pixel_3.json")

    kc.EnterGame()
    sleep(2)

    kc.EnterAdvMith()
    sleep(1)

    kc.ClearMith()
    sleep(0.5)

    for i in range(5):
        # If we are about to go into index 1, add an extra sleep
        # as the victory banner COULD mess up the image detection
        if i in range(3):
            sleep(4)
        else:
            sleep(1)

        kc.AttackMith(i)

    kc.ExitGame()
    client.Disconnect()
    os._exit(0)


if __name__ == "__main__":
    main()
