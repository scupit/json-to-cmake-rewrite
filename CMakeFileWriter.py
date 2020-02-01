import FileHelper
import Globals

from BuildData import BuildData

# TODO: Add github link
def writeWatermark(cmakeLists):
  cmakeLists.write("################################################################################")
  cmakeLists.write("\n# Generated with Skylar Cupit's json-to-cmake tool")
  cmakeLists.write("\n################################################################################")

def writeFile():
  with open(FileHelper.getAbsolutePath(Globals.CMAKE_FILE_NAME), 'w') as cmakeLists:
    data = BuildData()

    writeWatermark(cmakeLists)