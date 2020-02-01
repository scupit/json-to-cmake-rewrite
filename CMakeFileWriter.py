import FileHelper
import FileWriteUtils
import Globals

from BuildData import BuildData

def newlines(cmakeLists, numNewlines: int = 1):
  for i in range(0, numNewlines):
    cmakeLists.write('\n')

def writeWatermark(cmakeLists):
  cmakeLists.write("################################################################################")
  newlines(cmakeLists)
  cmakeLists.write("# Generated with Skylar Cupit's json-to-cmake tool")
  newlines(cmakeLists)
  # TODO: Add github link
  cmakeLists.write("################################################################################")

def writeCmakeVersion(data: BuildData, cmakeLists):
  cmakeLists.write(f"cmake_minimum_required( VERSION {data.cmakeVersion} )")

def writeProjectName(data: BuildData, cmakeLists):
  cmakeLists.write(f"project( {data.projectName } )")

def printImportedLibs(data: BuildData, cmakeLists):
  for importedLib in data.importedLibs:

    if len(importedLib.includeDirs) > 0:
      # Write include dirs variable
      importedLib.includeDirs.sort()
      cmakeLists.write(f"set( {FileWriteUtils.includeDirsVariable(importedLib.name)}")

      for includeDir in importedLib.includeDirs:
        cmakeLists.write(f"\n\t{FileWriteUtils.projectSourceDir}/{includeDir}")
      cmakeLists.write(')')

    newlines(cmakeLists, 2)

    if len(importedLib.headers) > 0:
      # Write headers variable
      importedLib.headers.sort()
      cmakeLists.write(f"set( {FileWriteUtils.headersVariable(importedLib.name)}")

      for headerFile in importedLib.headers:
        cmakeLists.write(f"\n\t{FileWriteUtils.projectSourceDir}/{headerFile}")
      cmakeLists.write(')')

    # Write library files
    for i in range(0, len(importedLib.libraryFiles)):
      newlines(cmakeLists, 2)
      cmakeLists.write(f"find_library( {FileWriteUtils.mangleLibName(importedLib.name, i)}")
      cmakeLists.write(f"\n\tNAMES {importedLib.libraryFiles[i]}")
      cmakeLists.write(f"\n\tPATHS {importedLib.dirContainingLibraryFiles}")
    cmakeLists.write(')')

def writeFile():
  with open(FileHelper.getAbsolutePath(Globals.CMAKE_FILE_NAME), 'w') as cmakeLists:
    data = BuildData()

    writeWatermark(cmakeLists)
    newlines(cmakeLists, 2)

    writeCmakeVersion(data, cmakeLists)
    newlines(cmakeLists)
    writeProjectName(data, cmakeLists)
    newlines(cmakeLists, 2)

    printImportedLibs(data, cmakeLists)
    newlines(cmakeLists, 2)
    