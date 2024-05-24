import os
import zipfile
import shutil
from googledriver import download_folder
# from google_drive_downloader import GoogleDriveDownloader as gdd

# CACHE_DRIVE_URL = 'https://drive.google.com/drive/folders/1fggdYaswNC5-AafMH1cK-iuIEJY-nWY0?usp=sharing&confirm=t'

CACHE_DRIVE_URL = 'https://drive.usercontent.google.com/download?id=1-Dht7o2lEzRqcM-KYY0Bl1sX7N9V_XhZ&export=download&authuser=1&confirm=t'

class DataDownloadUtility:
    def __init__(self, download_path):
        """
        Initializes the download utility with a specific path where data will be saved.
        """
        self.download_path = download_path
        os.makedirs(self.download_path, exist_ok=True)

    def download_files(self, url):
        """
        Downloads files from a specified Google Drive URL to the download path.
        """
        try:
            download_folder(url, self.download_path)
            print("Download completed successfully.")
        except Exception as e:
            print(f"An error occurred during data download: {e}")
        

class ZipUtility:
    def __init__(self, extract_base_path):
        """
        Initializes the zip utility with a base path where extracted files will be stored.
        """
        self.extract_base_path = extract_base_path
        os.makedirs(self.extract_base_path, exist_ok=True)

    def unzip_files(self, zip_file_path, extract_subfolder=None):
        """
        Unzips files from a given zip file path to an optionally specified subfolder of the base path.
        """
        extract_path = os.path.join(self.extract_base_path, extract_subfolder) if extract_subfolder else self.extract_base_path
        try:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
                print(f"Files extracted to {extract_path}")
        except zipfile.BadZipFile:
            print("Failed to unzip files: File may be corrupted or not a zip file.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")



if __name__ == "__main__":
    save_path_cache = os.path.join('.')
    cache_downloader = DataDownloadUtility(save_path_cache)
    cache_downloader.download_files(CACHE_DRIVE_URL)
    
    unzip_utility = ZipUtility(save_path_cache)
    
    # cache_zip_file = os.path.join(save_path_cache, 'cache.zip')
    # unzip_utility.unzip_files(cache_zip_file, 'cache' )
    # faiss_zip_file = os.path.join(save_path_cache, 'faiss.zip')
    # unzip_utility.unzip_files(cache_zip_file, 'faiss' )
    
    # faiss_dest_dir = os.path.join('.', 'src', 'models')
    # faiss_src_dir = os.path.join(save_path_cache, 'faiss')
    # shutil.move(faiss_src_dir, faiss_dest_dir)

    # gdd.download_file_from_google_drive(file_id='1-Dht7o2lEzRqcM-KYY0Bl1sX7N9V_XhZ',
    #                                 dest_path='./cache',
    #                                 unzip=True)