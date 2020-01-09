import os
import threading

import cv2 as cv
import numpy as np


def remove_mark(img, alpha=2.2, beta=-160):
    return np.clip(alpha * img + beta, 0, 255).astype(np.uint8)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?")
    parser.add_argument(
        "-r", dest="replace", action="store_true", help="Replace original file",
    )

    args = parser.parse_args()

    img = cv.imread(args.file)
    cleaned = remove_mark(img)

    if args.replace:
        cv.imwrite(args.file, cleaned)
    else:
        directory = "/".join(args.file.split("/")[:-1])
        filename = "cleaned_" + args.file.split("/")[-1]
        cv.imwrite(directory + "/" + filename, cleaned)
