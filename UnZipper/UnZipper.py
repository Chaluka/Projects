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


# from tester import unZipMe
import zipfile
import os 
import sys
from os.path import isfile, join
import glob
from typing import TypeVar, List


class UnZipper:
    
    RECURSION_DEPTH_LIMIT = 3

    def __init__(self) -> None:
        self.root_dir_path = '/home/kamikaze/Documents/GitHub/Projects/UnZipper/files/' 
        self.log_string = []
        self.file_extension = ".zip"
        self.log_file_path = self.root_dir_path + 'log_file.txt'

    def set_directory(self, dir_path:str)->None:
        self.root_dir_path = dir_path

    def set_file_extension(self, file_extension:str)->None:
        self.file_extension = file_extension

    def __str__(self):
        return self.cur_dir_path
    
    def __get_file_list(self, dir_path):
        extended_path = dir_path + "*" + self.file_extension
        print(extended_path)
        file_list = glob.glob(extended_path)
        return file_list

    def __unzip_file(self, file, dir_path):
        file_dir_path = file.strip(self.file_extension) + "/"
        print("path", file_dir_path)
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(dir_path)
        return file_dir_path

    def extract_all_files(self, dir_path="", depth=0):
        if depth< self.RECURSION_DEPTH_LIMIT:
            dir_path = self.root_dir_path if not dir_path else dir_path
            file_list = self.__get_file_list(dir_path)
            self.log_string.append([dir_path, file_list])
            if not len(file_list):
                print(dir_path , " IS EMPTY. ABORTED..!!")
            else:
                print(len(file_list) ," ZIP FILES FOUND. EXTRACTING..!!")
                for file in file_list:
                    print(file, " EXTRACTED")
                    file_dir_path = self.__unzip_file(file,dir_path)
                    self.extract_all_files(file_dir_path, depth+1)
    
    def logger(self):
        seperator = "-"*50 + "\n"
        with open(self.log_file_path, 'w') as file:
            for dir_path, file_list in self.log_string:
                file.write(dir_path+"\n")
                for i, file_name in enumerate(file_list):
                    file_name = file_name.replace(dir_path, "")
                    file.write('\t'+ str(i+1) +". " + file_name+"\n")
                
                file.write(seperator)
            

    def run(self):
        self.extract_all_files()
        self.logger()


if __name__ == "__main__":
    zipper = UnZipper()
    zipper.run()
    # g = glob.glob('/home/kamikaze/Documents/GitHub/Projects/UnZipper/files/main/f2/*.zip')
    # print(g)
    # extract_all_files(path,ext)
