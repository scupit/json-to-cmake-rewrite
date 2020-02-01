from CMakeFileWriter import writeFile
from FileHelper import getAbsolutePath
from Globals import CMAKE_FILE_NAME

with open(getAbsolutePath(CMAKE_FILE_NAME), 'w') as cmakeLists:
  writeFile(cmakeLists)
  print(CMAKE_FILE_NAME, "written successfully!")