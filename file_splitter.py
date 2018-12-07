# coding: utf-8

import sys
import os
from socket import *

# clean up: https://superuser.com/questions/482435/how-to-remove-all-files-starting-with-a-certain-string-in-linux/482436
# from https://www.tutorialspoint.com/How-to-spilt-a-binary-file-into-multiple-files-using-Python
class FileSplitter:
  def __init__(self, chunk_size = 50):
    self.chunk_size = chunk_size

  def split(self, file):
    chunk_file_names = []
    
    file_number = 1
    with open(file) as f:
        chunk = f.read(self.chunk_size)
        while chunk:
            with open(file + str(file_number), "w+") as chunk_file:
                chunk_file.write(chunk)
            file_number += 1
            chunk = f.read(self.chunk_size)
            chunk_file_names.append(chunk_file.name)

    return chunk_file_names