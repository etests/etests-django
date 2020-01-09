import pdf2image
import sys
import os


def extract_images(file, save_directory, threads=2):

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
        
    images_from_path = pdf2image.convert_from_path(
        file,
        dpi=400,
        fmt="tif",
        output_file=str(),
        output_folder=save_directory,
        thread_count=threads,
    )


if __name__=="__main__":

    file = sys.argv[1]
    directory = ".".join(file.split(".")[:-1])
    print(directory)
    extract_images(file, directory)
