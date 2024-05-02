import os
from googledriver import download_folder

class DataDownloadUtility:
    def __init__(self, download_path):
        """
        Initializes the download utility with a specific path where files will be saved.
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


if __name__ == "__main__":
    drive_url = 'https://drive.google.com/drive/folders/1rgdMVClMHLoVVPDtU8BZhHy1TiWasdSS?usp=sharing'
    save_path = os.path.join('.', 'src', 'models', 'data', 'raw')
    downloader = DataDownloadUtility(save_path)
    downloader.download_files(drive_url)
