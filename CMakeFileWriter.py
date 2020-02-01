import FileHelper
import FileWriteUtils
from FileWriteUtils import inBraces, headersVariable, sourcesVariable, includeDirsVariable
import Globals

from BuildData import BuildData
from OutputItem import OutputItem

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

    if importedLib.hasIncludeDirs()
      # Write include dirs variable
      importedLib.includeDirs.sort()
      cmakeLists.write(f"set( {includeDirsVariable(importedLib.name)}")

      for includeDir in importedLib.includeDirs:
        cmakeLists.write(f"\n\t{FileWriteUtils.projectSourceDir}/{includeDir}")
      cmakeLists.write(')')

    newlines(cmakeLists, 2)

    if importedLib.hasHeaders()
      # Write headers variable
      importedLib.headers.sort()
      cmakeLists.write(f"set( {headersVariable(importedLib.name)}")

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

def printGeneralOutputData(outputData: OutputItem, data, cmakeLists):
  # Write headers
  outputData.headers.sort()
  cmakeLists.write(f"set( {headersVariable(outputData.name)}")
  for linkedLib in outputData.linkedLibs:
    if linkedLib.hasHeaders():
      cmakeLists.write(f"\n\t{inBraces(headersVariable(linkedImportedLib.name))}")
  for headerFile in outputData.headers:
    cmakeLists.write(f"\n\t{FileWriteUtils.projectSourceDir}/{headerFile}")
  cmakeLists.write(')')

  newlines(cmakeLists, 2)

  # Write sources, which include the item's headers
  outputData.sources.sort()
  cmakeLists.write(f"set( {sourcesVariable(outputData.name)}")
  if outputData.hasHeaders():
    cmakeLists.write(f"\n\t{inBraces(headersVariable(outputData.name))}")
  if outputData.isExe and outputData.hasMainFile():
    cmakeLists.write(f"\n\t{FileWriteUtils.projectSourceDir}/{outputData.mainFile}")
  for sourceFile in outputData.sources:
    cmakeLists.write(f"\n\t{FileWriteUtils.projectSourceDir}/{sourceFile}")
  cmakeLists.write(')')

  # Write include dirs
  outputData.includeDirs.sort()
  cmakeLists.write(f"set( {includeDirsVariable(outputData.name)}")
  for linkedLib in outputData.linkedLibs:
    if linkedLib.hasIncludeDirs():
      cmakeLists.write(f"\n\t{inBraces(includeDirsVariable(linkedLib.name))}")
  for includeDir in outputData.includeDirs:
    cmakeLists.write(f"\n\t{FileWriteUtils.projectSourceDir}/{includeDir}")
  cmakeLists.write(')')

def printSharedLib(sharedLib: OutputItem, allData: BuildData, cmakeLists):
  printGeneralOutputData(sharedLib, allData, cmakeLists)
  newlines(cmakeLists, 2)

  cmakeLists.write(f"add_library( {sharedLib.name} SHARED {inBraces(sourcesVariable(sharedLib.name))} )")
  if sharedLib.hasIncludeDirs():
    cmakeLists.write(f"\ntarget_include_directories( {sharedLib.name} PRIVATE {inBraces(includeDirsVariable(sharedLib.name))} )")

def printStaticLib(staticLib: OutputItem, allData: BuildData, cmakeLists):
  printGeneralOutputData(staticLib, allData, cmakeLists)
  newlines(cmakeLists, 2)

  cmakeLists.write(f"add_library( {staticLib.name} STATIC {inBraces(sourcesVariable(staticLib.name))} )")
  if staticLib.hasIncludeDirs():
    cmakeLists.write(f"\ntarget_include_directories( {staticLib.name} PRIVATE {inBraces(includeDirsVariable(staticLib.name))} )")

def printExe(exeItem: OutputItem, allData: BuildData, cmakeLists):
  printGeneralOutputData(exeItem, allData, cmakeLists)
  newlines(cmakeLists, 2)

  cmakeLists.write(f"add_execuatable( {exeItem.name} {inBraces(sourcesVariable(exeItem.name))} )")
  if exeItem.hasIncludeDirs():
    cmakeLists.write(f"\ntarget_include_directories( {exeItem.name} PRIVATE {inBraces(includeDirsVariable(exeItem.name))} )")

def printOutputs(data, cmakeLists):
  # Print shared libs
  for sharedLibOutput in data.outputs:
    if sharedLibOutput.isSharedLib:
      printSharedLib(sharedLibOutput, data, cmakeLists)
      newlines(cmakeLists, 2)

  # Print static libs
  for staticLibOutput in data.outputs:
    if staticLibOutput.isStaticLib:
      printStaticLib(staticLibOutput, data, cmakeLists)
      newlines(cmakeLists, 2)

  # Print executables
  for exeOutput in data.outputs:
    if exeOutput.isExe:
      printExe(exeOutput, data, cmakeLists)
      newlines(cmakeLists, 2)

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

    # Already ends in two newlines due to how outputs are printed from 'for' loops
    printOutputs(data, cmakeLists)
    