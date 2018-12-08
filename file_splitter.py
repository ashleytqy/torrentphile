# coding: utf-8
import os

# clean up: https://superuser.com/questions/482435/how-to-remove-all-files-starting-with-a-certain-string-in-linux/482436
# from https://www.tutorialspoint.com/How-to-spilt-a-binary-file-into-multiple-files-using-Python

class FileSplitter:
  def __init__(self, chunk_size = 500):
    self.chunk_size = chunk_size

  def split(self, file_path):
    chunk_file_names = []
    file_name, file_ext = os.path.splitext(file_path)
    
    file_number = 1
    with open(file_path) as file:
        chunk = file.read(self.chunk_size)
        while chunk:
            with open(file_name + str(file_number) + file_ext, "w+") as chunk_file:
                chunk_file.write(chunk)
            file_number += 1
            chunk = file.read(self.chunk_size)
            chunk_file_names.append(chunk_file.name)

    return chunk_file_names