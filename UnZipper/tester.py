"""
    This program (UnZipper) can decompress a compressed directory with 
    multiple files/directories and mutil-levels of depth without altering 
    the directory tree of the commpressed file. Decompression is done at 
    each level for all avaibale diretories and move into the next level 
    recursively.

    Supports both ZIP and RAR file formats.
"""

from datetime import date
t = date.today()
print(str(t))