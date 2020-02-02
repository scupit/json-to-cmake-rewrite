from CMakeFileWriter import writeFile
from FileHelper import getAbsolutePath
from Globals import CMAKE_FILE_NAME, JSON_FILE_NAME

from os import path

if path.exists(getAbsolutePath(JSON_FILE_NAME)):
  with open(getAbsolutePath(CMAKE_FILE_NAME), 'w') as cmakeLists:
      writeFile(cmakeLists)
      print(CMAKE_FILE_NAME, "written successfully!")
else:
  print(f"{getAbsolutePath(JSON_FILE_NAME)} does not exist")