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
import sys
import glob
from datetime import date
from typing import List

class UnZipper:

    RECURSION_DEPTH_LIMIT = 3

    def __init__(self) -> None:
        self.root_dir_path = sys.path[0] + "/"
        self.log_string = []
        self.file_extension = ".zip"
        self.log_file_path = self.root_dir_path + \
            str(date.today()) + '_log.txt'

    def set_directory(self, dir_path: str) -> None:
        self.root_dir_path = dir_path

    def set_file_extension(self, file_extension: str) -> None:
        self.file_extension = file_extension

    def __str__(self)->str:
        return self.cur_dir_path

    def __get_file_list(self, dir_path)->List[str]:
        """ 
            Returns a list of files in current directory

        Args:
            dir_path (str): path of the current directory

        Returns:
            List[str]: list of file paths
        """
        # generate the complete path pattern to obtain the list of files
        # with given extension in currrent directory
        # e.g., /Documents/GitHub/Projects/UnZipper/*.zip
        extended_path = dir_path + "*" + self.file_extension
        # obtain the file list
        file_list = glob.glob(extended_path)
        return file_list

    def __unzip_file(self, file, dir_path)->str:
        """Unzip the file into the given directory

        Args:
            file (str): path of the zip file
            dir_path (str): path of the current directory

        Returns:
            str: path of the unzipped directory
        """
        # extract the path of the directory that file decompressed into
        file_dir_path = file.strip(self.file_extension) + "/"
        # decompress the file using zipfile module
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(dir_path)
        return file_dir_path

    def extract_all_files(self, dir_path="", depth=0)->None:
        """ 
            Extract all the compressed files found in the current directory. 
            This is a recursive function that traverse into multi-levels of 
            the compressed file.

        Args:
            dir_path (str, optional): path of current directory. Defaults to "".
            depth (int, optional): recursion depth. Defaults to 0.
        """
        # decompress until current recursive depth does not exceeds the limit
        if depth < self.RECURSION_DEPTH_LIMIT:
            dir_path = self.root_dir_path if not dir_path else dir_path
            file_list = self.__get_file_list(dir_path)
            # save directory path and list of compressed files to include in log file
            self.log_string.append([dir_path, file_list])
            # only if compressed files exist in current directory
            if len(file_list):
                for file in file_list:
                    print("-->", file)
                    file_dir_path = self.__unzip_file(file, dir_path)
                    # recursively move to next level of compression
                    self.extract_all_files(file_dir_path, depth+1)

    def __logger(self):
        """
            Log directory paths along with the decompressed file names
        """
        seperator = "-"*50 + "\n"

        with open(self.log_file_path, 'w') as file:
            for dir_path, file_list in self.log_string:
                file.write(dir_path+"\n")
                for i, file_name in enumerate(file_list):
                    file_name = file_name.replace(dir_path, "")
                    file.write('\t' + str(i+1) + ". " + file_name+"\n")

                file.write(seperator)

    def run(self):
        self.extract_all_files()
        self.__logger()


if __name__ == "__main__":
    zipper = UnZipper()
    zipper.run()
