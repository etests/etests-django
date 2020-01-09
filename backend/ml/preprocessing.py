import cv2
import sys
import numpy as np


def clean(img, alpha=2.2, beta=-160):
    return np.clip(alpha * img + beta, 0, 255).astype(np.uint8)

def binarize(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (thresh, img_bw) = cv2.threshold(
        img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU
    )
    return img_bw


def smoothen(img):
    return cv2.GaussianBlur(img, (1, 1), 0)


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?")
    parser.add_argument(
        "-r", dest="replace", action="store_true", help="Replace original file",
    )

    args = parser.parse_args()

    img = cv2.imread(args.file)
    binarized = smoothen(binarize(img))

    if args.replace:
        cv2.imwrite(args.file, binarized)
    else:
        directory = "/".join(args.file.split("/")[:-1])
        filename = "binarized_" + args.file.split("/")[-1]
        cv2.imwrite(directory + "/" + filename, binarized)

