### Used to compile main.py ###
# Not needed to run floppy bird without compiling #

from distutils.core import setup
import py2exe
import os

# Copy the file structure of assets
files = []

for (folderpath, foldernames, filenames) in os.walk("assets"):
    if filenames != []:
        temp = (folderpath, [])
        for file in filenames:
            temp[1].append(folderpath + "\\" + file)
        files.append(temp)
    

setup(
    options = {'py2exe': {'bundle_files': 1}},
    name="Floppy Bird",
    version='1.0',
    author='samh366',
    console=['main.py'],
    zipfile = None,

    data_files = files,

    windows = [{
            "script": "main.py",
            "icon_resources": [(1, "assets/icons/icon_256.ico")],
            "dest_base":"Floppy Bird",
            }],
    
    
)