from zipfile import ZipFile
import os
import time


def get_all_file_paths(directory):

    # initializing empty file paths list
    file_paths = []

    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    # returning all file paths
    return file_paths


def main():
    # path to folder which needs to be zipped
    directory = "models/faiss"

    # calling function to get all file paths in the directory
    file_paths = get_all_file_paths(directory)
    len_files = len(file_paths)
    start = time.time()
    # writing files to a zipfile
    with ZipFile("faiss.zip", "w") as zip:
        # writing each file one by one
        for index, file in enumerate(file_paths):
            print(f"File {index + 1}/{len_files}, Percentage: {((index + 1) / len_files) * 100} %, Time: {time.time() - start} sec...", end="\r")
            zip.write(file)

    print("All files zipped successfully!")


if __name__ == "__main__":
    main()
