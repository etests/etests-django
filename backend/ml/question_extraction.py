import os
import re
import sys

import cv2
import numpy as np
import pytesseract


def get_boxes(img, ITERS=10):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # smooth the image to avoid noises
    gray = cv2.medianBlur(gray, 5)

    # Apply adaptive threshold
    thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)
    thresh_color = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

    # apply some dilation and erosion to join the gaps - change iteration to detect more or less area's
    thresh = cv2.dilate(thresh, None, iterations=ITERS)
    thresh = cv2.erode(thresh, None, iterations=ITERS)

    # Find the contours
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1
    )

    boxes = []

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        boxes.append((x, x + w, y, y + h))

    boxes.sort()

    return boxes


def get_labeled_boxes(
    img, MARGIN_WIDTH=100, config="-l eng --oem 1 --psm 8", digit_labeled=True
):
    H, W, _ = img.shape

    left_margin = img[0:H, 0:MARGIN_WIDTH]

    boxes = get_boxes(left_margin)
    if not digit_labeled:
        return [(y1, y2) for (x1, x2, y1, y2) in boxes]

    labeled_boxes = []
    take_last = -1
    for (i, box) in enumerate(boxes):
        (x1, x2, y1, y2) = box
        label = pytesseract.image_to_string(
            img[max(0, y1 - 10) : min(H, y2 + 10), 0:MARGIN_WIDTH], config=config
        )
        label = re.sub(r"[^\w]", "", label).lower()
        if (label.isdigit() or label in ["ans", "sol"]) and x1 <= MARGIN_WIDTH / 2:
            take_last = i
            labeled_boxes.append((y1, y2, label))

    if take_last < len(boxes) - 1:
        (x1, x2, y1, y2) = boxes[take_last + 1]
        if x1 <= MARGIN_WIDTH / 2:
            labeled_boxes.append((y1, y2, "END"))

    return labeled_boxes


def extract_questions(img, save_directory="", OFFSET=20, **kwargs):

    H, W, _ = img.shape

    detected_boxes = get_labeled_boxes(img, **kwargs)

    last_y = -OFFSET
    last_name = ""
    last_label = ""
    filename = ""

    questions = []

    i = 1
    for box in detected_boxes:

        cur_offset = OFFSET

        if len(box) == 3:
            y1, y2, label = box
        else:
            y1, y2 = box

        k = 120
        if y1 >= k:
            offset_boxes = get_boxes(img[y1 - k : y1 + int(k/10), 0:W], ITERS=15)
            cv2.rectangle(img, (0, y1-k), (W, y1), color=(0,255,0), thickness=2)
            top_offset = k
            bottom_offset = 0
            for offset_box in offset_boxes:
                (a1, b1, a2, b2) = offset_box
                if b2 >= k:
                    cv2.rectangle(img, (a1, y1-k+a2), (b1, y1-k+b2), color=(255,0,0), thickness=1)
                    bottom_offset = max(bottom_offset, int(6*k/5) - a2)
                else:
                    cv2.rectangle(img, (a1, y1-k+a2), (b1, y1-k+b2), color=(0,0,255), thickness=1)
                    top_offset = min(top_offset, int(3*k/5) - b2)

                cur_offset = max(top_offset, bottom_offset)
        else:
            cur_offset = y1
        
        if len(box) == 3:
            if last_y >= 0:
                questions.append(
                    (img[last_y : y1 - cur_offset, 0:W], filename + ".tif")
                )

            if label.isdigit():
                filename = str(i) + "_" + label
                last_name = filename
            elif label in ["ans", "sol"]:
                filename = last_name + "_" + label
            
            last_label = label

        else:
            if last_y >= 0:
                questions.append((img[last_y : y1 - cur_offset, 0:W], str(i) + ".tif"))

        last_y = max(0, y1 - cur_offset)
        i += 1

    if not kwargs.get("digit_labeled", True) and last_y >= 0:
        questions.append((img[last_y:H, 0:W], str(i) + ".tif"))
    elif last_label != "END" and last_y >= 0:
        questions.append((img[last_y:H, 0:W], str(i) + "_" + last_label + ".tif"))

    cv2.imshow("red", cv2.resize(img, (600,1000)))
    cv2.imwrite("Red.tif", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return questions


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?")
    parser.add_argument(
        "-u",
        dest="digit_labeled",
        action="store_false",
        help="Digit labled question extraction",
    )

    parser.add_argument(
        "-w",
        dest="margin_width",
        type=int,
        default=150,
        help="Width of digit labels in image",
    )

    args = parser.parse_args()

    questions = extract_questions(
        cv2.imread(args.file),
        OFFSET=30,
        digit_labeled=args.digit_labeled,
        MARGIN_WIDTH=args.margin_width,
    )

    final_directory = (
        "/".join(args.file.split("/")[:-1])
        + "/"
        + args.file.split("/")[-1].split(".")[0]
    )

    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    for image, filename in questions:
        print(final_directory + "/" + filename)
        cv2.imwrite(final_directory + "/" + filename, image)
