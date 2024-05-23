# importing the zipfile module
from zipfile import ZipFile


def main():
    # loading the temp.zip and creating a zip object
    with ZipFile("cache.zip", "r") as zObject:

        # Extracting all the members of the zip
        # into a specific location.
        zObject.extractall(path="test")


if __name__ == "__main__":
    main()
