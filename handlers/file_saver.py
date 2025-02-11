import os


class FileSaver:
    def __init__(self, download_folder):
        self.download_folder = download_folder
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)

    def save_file(self, filename, payload):
        filepath = os.path.join(self.download_folder, filename)
        with open(filepath, 'wb') as file:
            file.write(payload)
        return filepath
