import pprint, os, logging, json
from time import sleep
from pathlib import Path
from kg.vnc import VNC
from kg.kingdom_clicker import KingdomClicker


pp = pprint.PrettyPrinter(indent=4)


# Notable Locations (Pixel 3 related)
# Dimensional tunnel from main screen =  300, 1865
# Dragon present from main screen = 645, 225
# Alliance tab from home screen = 815, 2080
# Main tab = 85, 2085
# Login X top left - 968, 343
# Recent apps = CTRL-SHFT-ESC


def main():
    logging.basicConfig(filename="executions.log", format="%(asctime)s %(message)s")
    logger = logging.getLogger(__name__)
    logger.setLevel("INFO")

    logger.info("Starting job")
    # setup temp dir
    # TODO: Move this to KingdomClicker init sub
    Path("./tmp").mkdir(parents=True, exist_ok=True)
    device = json.load(open(f"./resources/devices/pixel_3.json"))
    # Initiate the appropriate client... Right now we only have VNC
    client = VNC(logger=logger)

    kc = KingdomClicker(client=client, device=device, logger=logger)

    if kc.EnterGame():
        sleep(3)

        if kc.EnterAdvMith():
            sleep(1)
            if kc.ClearMith():
                sleep(0.5)
                for i in range(6):
                    # If we are about to go into index 1, add an extra sleep
                    # as the victory banner COULD mess up the image detection
                    if i in range(3):
                        sleep(4)
                    else:
                        sleep(1)

                    kc.AttackMith(i)

    sleep(0.5)
    kc.ExitGame()
    sleep(0.5)

    client.Disconnect()
    os._exit(0)


if __name__ == "__main__":
    main()
