import math
import sys

import cv2
import numpy as np

from image_cropping import auto_crop


def detect_columns(img):

    H, W, _ = img.shape

    dst = cv2.Canny(img, 50, 200, None, 3)

    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)

    lines = cv2.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)

    linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)

    max_d = 0
    max_d_x = 0
    max_d_ends = (0, 0)
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            if abs(l[2] - l[0]) <= 0.01:
                d = math.sqrt((l[2] - l[0]) ** 2 + (l[3] - l[1]) ** 2)
                if d > max_d:
                    max_d = d
                    max_d_x = l[2]
                    max_d_ends = (min(l[1], l[3]) + 10, max(l[1], l[3]) - 30)

    cv2.line(
        cdstP,
        (max_d_x, max_d_ends[0]),
        (max_d_x, max_d_ends[1]),
        (255, 0, 0),
        5,
        cv2.LINE_AA,
    )
    if max_d < 0.5 * H:
        return (1, 0, 0, 0)
    else:
        # print(max_d, max_d_x, max_d_ends)
        return (2, max_d_x, max_d_ends[0], max_d_ends[1])


def rearrange_columns(img):

    H, W, _ = img.shape

    cols, x_c, y_top, y_bottom = detect_columns(img)
    print(cols, x_c, y_top, y_bottom)

    if cols == 2:
        img[:, x_c - 10 : x_c + 10] = np.full((H, 20, 3), 255, np.uint8)
        img1 = auto_crop(img[y_top:y_bottom, 0:x_c], orientation=0)
        img2 = auto_crop(img[y_top:y_bottom, x_c:W], orientation=0)
        h1, w1, _ = img1.shape
        h2, w2, _ = img2.shape
        if w1 < w2:
            white = np.zeros((h1, w2 - w1, 3), dtype=np.uint8)
            white.fill(255)
            img1 = np.concatenate((img1, white), axis=1)
        elif w1 > w2:
            white = np.zeros((h2, w1 - w2, 3), dtype=np.uint8)
            white.fill(255)
            img2 = np.concatenate((img2, white), axis=1)
        white = np.zeros((100, max(w1, w2), 3), dtype=np.uint8)
        white.fill(255)
        return np.concatenate((img1, white, img2), axis=0)
    else:
        return img


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?")
    parser.add_argument(
        "-r", dest="replace", action="store_true", help="Replace original file",
    )

    args = parser.parse_args()

    img = cv2.imread(args.file)
    rearranged = rearrange_columns(img)

    if args.replace:
        cv2.imwrite(args.file, rearranged)
    else:
        directory = "/".join(args.file.split("/")[:-1])
        filename = "rearranged_" + args.file.split("/")[-1]
        cv2.imwrite(directory + "/" + filename, rearranged)
