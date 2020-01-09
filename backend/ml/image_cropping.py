import cv2
import numpy as np


"""
Parameters
----------
orientation : int
              Possible values are 
              0 for horizontal,
              1 for verticle,
              2 for both
"""


def auto_crop(img, orientation=2):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = 255 * (gray < 128).astype(np.uint8)
    coords = cv2.findNonZero(gray)
    x, y, w, h = cv2.boundingRect(coords)

    if orientation == 0:
        return img[:, x : x + w]

    elif orientation == 1:
        return img[y : y + h, :]

    else:
        return img[y : y + h, x : x + w]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?")
    parser.add_argument(
        "-o",
        dest="orientation",
        type=int,
        default=2,
        help="Cropping Orientation. Possible values are 0, 1, 2",
    )
    parser.add_argument(
        "-r", dest="replace", action="store_true", help="Replace original file",
    )

    args = parser.parse_args()

    img = cv2.imread(args.file)
    cropped = auto_crop(img, orientation=args.orientation)

    if args.replace:
        cv2.imwrite(args.file, cropped)
    else:
        directory = "/".join(args.file.split("/")[:-1])
        filename = "cropped_" + args.file.split("/")[-1]
        cv2.imwrite(directory + "/" + filename, cropped)
