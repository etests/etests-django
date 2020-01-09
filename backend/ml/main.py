import concurrent.futures
import os
import sys

import cv2

from column_detection import rearrange_columns
from image_cropping import auto_crop
from pdf_extraction import extract_images
from question_extraction import extract_questions
from watermark_utils import remove_mark

import argparse


def directory_operation(operation, open_directory, save_directory, *args, **kwargs):

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for img in os.listdir(open_directory):
            processed = executor.submit(
                operation, cv2.imread(open_directory + "/" + img), *args, **kwargs
            ).result()

            if type(processed) == list:

                final_directory = save_directory + "/" + img.split(".")[0]

                if not os.path.exists(final_directory):
                    os.makedirs(final_directory)

                for image, filename in processed:
                    cv2.imwrite(final_directory + "/" + filename, image)
            else:
                cv2.imwrite(save_directory + "/" + img, processed)


parser = argparse.ArgumentParser()
parser.add_argument("file", nargs="?")
parser.add_argument(
    "-p", dest="pdf", action="store_true", help="Extract from pdf",
)
parser.add_argument(
    "-w", dest="clean", action="store_true", help="Remove watermark",
)
parser.add_argument(
    "-r", dest="rearrange", action="store_true", help="Rearrange columns",
)
parser.add_argument(
    "-c", dest="crop", action="store_true", help="Auto crop",
)
parser.add_argument(
    "-q", dest="questions", action="store_true", help="Extract questions",
)
args = parser.parse_args()

directory = os.getcwd() + "/extracted/" + args.file.split("/")[-1].split(".")[0]

raw_directory = directory + "/raw/"
cleaned_directory = directory + "/cleaned/"
columns_directory = directory + "/columns/"
cropped_directory = directory + "/cropped/"
questions_directory = directory + "/questions/"

if args.pdf:
    print("Exctracting...")
    extract_images(args.file, raw_directory, threads=4)

if args.clean:
    print("Removing watermark...")
    directory_operation(remove_mark, raw_directory, cleaned_directory)

if args.rearrange:
    print("Rearranging columns...")
    if os.path.exists(cleaned_directory):
        open_directory = cleaned_directory
    else:
        open_directory = raw_directory
    directory_operation(rearrange_columns, open_directory, columns_directory)

if args.crop:
    print("Autocropping margins...")
    if os.path.exists(columns_directory):
        open_directory = columns_directory
    elif os.path.exists(cleaned_directory):
        open_directory = cleaned_directory
    else:
        open_directory = raw_directory
    directory_operation(auto_crop, open_directory, cropped_directory)

if args.questions:
    print("Extracting questions...")
    if os.path.exists(cropped_directory):
        open_directory = cropped_directory
    else:
        open_directory = columns_directory
    directory_operation(
        extract_questions, open_directory, questions_directory, MARGIN_WIDTH=120
    )
