"""
    This program (UnZipper) can decompress a compressed directory with 
    multiple files/directories and mutil-levels of depth without altering 
    the directory tree of the commpressed file. Decompression is done at 
    each level for all avaibale diretories and move into the next level 
    recursively.

    Supports both ZIP and RAR file formats.
"""

__author__ = "Chaluka Salgado"
__copyright__ = "Copyright 2020 @ Kamikaze"
__email__ = "chaluka.salgado@gmail.com"
__date__ = "29-Oct-2019"
__updated__ = "28-May-2021"
__version__ = "1.0"


import zipfile
from os import listdir
from os.path import isfile, join
import glob

RECURSION_DEPTH_LIMIT = 5

# def getFileList(path_directory):
#     onlyfiles = [path_directory + f for f in listdir(path_directory) if isfile(join(path_directory, f))]
#     return onlyfiles

def getFileList(path_directory, file_extension):
    extended_path = path_directory + "*" + file_extension
    file_list = glob.glob(extended_path)
    return file_list


def unZipMe(path_to_zip_file, file_extension):
    extract_directory_path = path_to_zip_file.strip(file_extension) + "/"
    print("path", extract_directory_path)
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_directory_path)

def extractAllZipFiles(path_directory, file_extension):
    #first extact all zip files in current directory
    file_list = getFileList(path_directory,file_extension)
    print(file_list)
    if len(file_list)==0:
        print(path_directory , " IS EMPTY. ABORTED..!!")
    else:
        print(len(file_list) ," ZIP FILES FOUND. EXTRACTING..!!")
        for file in file_list:
            print(file, " EXTRACTED")
            unZipMe(file,file_extension)
            current_directory_path = file.strip(file_extension) + "/"
            print(current_directory_path)
            extractAllZipFiles(current_directory_path, file_extension)


path_to_zip_file = "/Users/chalukasalgado/test/testfile2.zip"
directory_to_extract = "/Users/chalukasalgado/test/extracted"
path_directory = "/Users/chalukasalgado/test/"
file_extension = ".zip"

extractAllZipFiles(path_directory, file_extension)

# extract_directory_path = path_to_zip_file.strip(file_extension)

# print(extract_directory_path)