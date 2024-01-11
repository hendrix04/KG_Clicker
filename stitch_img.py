import pprint, os, logging, json
from time import sleep
from pathlib import Path
from kg.vnc import VNC
from kg.kingdom_clicker import KingdomClicker
import cv2
import numpy as np
from PIL import Image
from stitching import AffineStitcher
import pytesseract


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
    device = json.load(open(f"./resources/devices/pixel_3.json"))
    logger.info("Starting job")
    # setup temp dir
    # TODO: Move this to KingdomClicker init sub
    Path("./tmp").mkdir(parents=True, exist_ok=True)

    # client = VNC(logger=logger)

    # kc = KingdomClicker(client=client, device=device, logger=logger)

    # kc.TakeSS()
    image_paths = [
        "./tmp/alliance1.png",
        "./tmp/alliance2.png",
        "./tmp/alliance3.png",
        "./tmp/alliance4.png",
    ]
    # initialized a list of images
    imgs = []

    settings = {
        "detector": "sift",
        "confidence_threshold": 1.0,
        "crop": False,
        "estimator": "affine",
        "wave_correct_kind": "no",
        "matcher_type": "affine",
        "adjuster": "affine",
        "warper_type": "affine",
        "compensator": "no",
    }

    # for i in range(len(image_paths)):
    #     # imgs.append(cv2.imread(image_paths[i]))
    #     imgs.append(Crop_Alliance(cv2.imread(image_paths[i])))
    #     # imgs[i] = cv2.resize(imgs[i], (0, 0), fx=0.7, fy=0.7)
    #     # img = Image.fromarray(imgs[i])
    #     # cv2.imwrite(f"./tmp/alliance_{i}_test2.png", imgs[i])
    # stitcher = AffineStitcher(**settings)
    # panorama = stitcher.stitch(imgs)
    # cv2.imwrite("./tmp/alliance_merge.png", panorama)
    image = cv2.imread("./tmp/alliance_merge.png")
    text = pytesseract.image_to_string(image)
    print(text)
    exit()
    # showing the original pictures
    # cv2.imshow("1", imgs[0])
    # cv2.imshow("2", imgs[1])
    # cv2.imshow("3", imgs[2])
    # cv2.imshow("4", imgs[3])

    stitchy = cv2.Stitcher.create(cv2.Stitcher_SCANS)
    (dummy, output) = stitchy.stitch(imgs)
    print(dummy)

    if dummy != cv2.STITCHER_OK:
        # checking if the stitching procedure is successful
        # .stitch() function returns a true value if stitching is
        # done successfully
        print("stitching ain't successful")
    else:
        print("Your Panorama is ready!!!")
        output = np.rot90(output)

    # final output
    # cv2.imshow("final result", output)

    # cv2.waitKey(0)

    sleep(0.5)

    # client.Disconnect()
    os._exit(0)


def Crop_Alliance(img):
    footer = {"top": 675, "bottom": 2001, "left": 0, "right": 1088}

    return img[footer["top"] : footer["bottom"], footer["left"] : footer["right"]]


if __name__ == "__main__":
    main()
