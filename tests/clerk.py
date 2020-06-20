# clerk.py

import io 
import os.path

def file_to_string(path):
  f = open(path, "r")
  file = f.read()
  file = file.replace('\n','')
  file = file.replace('  ', '')
  return file 

def get_file_type(path):
  extension = os.path.splitext(path)[1]
  return extension [1:]