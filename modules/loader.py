from os import path, makedirs, sep
import os

from numpy.core.fromnumeric import std
import requests
import sys
import zipfile

class Loader:

    def __init__(self, remote, zip_folder_path, extraction_target = None):
        """
            zip_folder_path doit terminer par un separateur ('/' ou '\')
        """
        self.remote = remote
        self.folder_path = zip_folder_path
        
        # recuperation du nom du zip
        self.file = self.folder_path + remote.split('/')[-1]

        self.extraction_target = extraction_target

    def ensure_data_loaded(self):
        '''
        Ensure if data are already loaded. Download if missing
        '''

        if path.exists(self.file):
            print('Le fichier existe déjà')
            return self.file.split('/')[-1]

        if not Loader.__ask_download_zip():
            return self.file.split('/')[-1]
    
        try:
            self._download_data()
        except requests.exceptions.ConnectionError as e:
            os.rmdir(self.file)
            raise e

        if self.extraction_target:
            self._extract_data()

        print('\nLes fichiers sont correctement téléchargés')
        return self.file.split('/')[-1]

    def __ask_download_zip():
        user_input = "PATRICK"
        user_input = input("Télécharger le fichier [y]/n ? ")
        while user_input not in ["n", "N", "y", "Y", ""]:
            user_input = input("Télécharger le zip [y]/n ? ")

        if user_input in ["n", "N"]:
            return False
        else:
            return True

    @staticmethod
    def __test_folder(folder):
        if path.exists(folder) == False:
            try:
                makedirs(folder)
            except OSError:
                print(f"Creation of the directory {folder} failed")
                exit(1)
            else:
                print(f"Successfully created the directory {folder}")


    def _download_data(self):
        '''
        Download the data from internet
        '''
        
        Loader.__test_folder(self.folder_path)

        print('Downloading data')
        with open(self.file, "wb") as f:
            response = requests.get(self.remote, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None: # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
            
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                    sys.stdout.flush()

    def _extract_data(self):
        '''
        Extract the zip file to the hard disk
        '''

        print('Begin extracting data')
        with zipfile.ZipFile(self.file, 'r') as zip_ref:
            zip_ref.extractall(self.extraction_target)
        print('Data extract successfully')

if __name__ == "__main__":
    loader = Loader(
        "https://stdatalake010.blob.core.windows.net/public/cifar-100.zip",
        '../datas/ZIP/',
        '../datas/RAW/'
    )
    loader.ensure_data_loaded()
    