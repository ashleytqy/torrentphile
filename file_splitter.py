# coding: utf-8
import os
from config import SOCK_CONFIG
# clean up: https://superuser.com/questions/482435/how-to-remove-all-files-starting-with-a-certain-string-in-linux/482436
# from https://www.tutorialspoint.com/How-to-spilt-a-binary-file-into-multiple-files-using-Python

class FileSplitter:
  def __init__(self):
    self.chunk_size = SOCK_CONFIG['DATA_SIZE']

  def split(self, client_directory, file_path):
    full_path = client_directory + '/' + file_path
    file_name, file_ext = os.path.splitext(file_path)
    prefix = client_directory + '/' + file_name
    new_folder = prefix if os.path.exists(prefix) else os.makedirs(prefix)

    sequence = 1
    chunk_file_names = []
    with open(full_path) as file:
        chunk = file.read(self.chunk_size)
        while chunk:
            with open(prefix + '/' + str(sequence) + file_ext, "w+") as chunk_file:
                chunk_file.write(chunk)
            sequence += 1
            chunk = file.read(self.chunk_size)
            chunk_file_names.append(chunk_file.name)

    return chunk_file_names