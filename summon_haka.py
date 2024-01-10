import pprint, os, logging, json
from time import sleep
from pathlib import Path
from kg.vnc import VNC
from kg.kingdom_clicker import KingdomClicker


pp = pprint.PrettyPrinter(indent=4)

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

    # Flow:
    #   Enter Game
    #   Click Cornucopia
    #   Search for Haka Event & Click
    #   Search for Go & Click
    #   Search for Alliance tab & Click
    #   Search for blue summon & click
    #   Move Haka
    #   Search for Yellow summon & Click
    #   Search for share icon & click
    #   Search for alliance button & click
    #   Search for Rally & Click
    #   Search for Depart & Click
    #   Search for Alliance Menu & Click
    #   Search for War & Click
    #   Wait for 30 seconds & check if Haka still exists
    #   When Haka leaves war tab, figure out if Haka is actually gone
    #   Search for Back button & click

    # if kc.EnterGame():
    #     sleep(3)

    for i in range(8):
        if kc.EnterEvent("haka_sm"):
            sleep(3)

            if kc.SummonHaka(is_alliance=True):
                sleep(1)
            else:
                logger.info("Could not summon Haka")
        else:
            logger.info("Could not enter event")

    # sleep(5)
    # kc.ExitGame()
    sleep(0.5)

    client.Disconnect()
    os._exit(0)


if __name__ == "__main__":
    main()
