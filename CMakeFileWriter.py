import FileHelper
import FileWriteUtils
from FileWriteUtils import inBraces, inQuotes, headersVariable, sourcesVariable, includeDirsVariable
import Globals

from BuildData import BuildData
from ImportedLibrary import ImportedLibrary
from OutputItem import OutputItem
from OutputGroup import OutputGroup

def conditionalNoneText(x: bool) -> str:
  return "" if x else "(none)"

# ////////////////////////////////////////////////////////////////////////////////
# GENERAL WRITE FUNCTIONS
# ////////////////////////////////////////////////////////////////////////////////

def headerComment(cmakeLists, title: str, newlinesAfter=True):
  cmakeLists.write("# ////////////////////////////////////////////////////////////////////////////////")
  cmakeLists.write(f"\n# {title}")
  cmakeLists.write("\n# ////////////////////////////////////////////////////////////////////////////////")
  if newlinesAfter:
    newlines(cmakeLists, 2)

def itemLabel(cmakeLists, label: str):
  cmakeLists.write(f"# {label}")
  newlines(cmakeLists)

def newlines(cmakeLists, numNewlines: int = 1):
  for i in range(0, numNewlines):
    cmakeLists.write('\n')

def writeOutputDirs(outputData: OutputItem, cmakeLists):
  cmakeLists.write(f"set_target_properties( {outputData.name} PROPERTIES")

  if outputData.isStaticLib or outputData.isSharedLib:
    cmakeLists.write(f"\n\tARCHIVE_OUTPUT_DIRECTORY {FileWriteUtils.getOutputDir(outputData.libOutputDir)}")
    cmakeLists.write(f"\n\tLIBRARY_OUTPUT_DIRECTORY {FileWriteUtils.getOutputDir(outputData.libOutputDir)}")

  if outputData.isExe or outputData.isSharedLib:
    cmakeLists.write(f"\n\tRUNTIME_OUTPUT_DIRECTORY {FileWriteUtils.getOutputDir(outputData.exeOutputDir)}")

  cmakeLists.write('\n)')

# ////////////////////////////////////////////////////////////////////////////////
# DATA WRITE FUNCTIONS
# ////////////////////////////////////////////////////////////////////////////////

def writeWatermark(cmakeLists):
  cmakeLists.write("################################################################################")
  cmakeLists.write("\n# Generated with Skylar Cupit's json-to-cmake tool                             #")
  cmakeLists.write("\n# GitHub: https://github.com/scupit/json-to-cmake-rewrite                      #")
  cmakeLists.write("\n################################################################################")
  newlines(cmakeLists, 2)

def writeCmakeVersion(data: BuildData, cmakeLists):
  cmakeLists.write(f"cmake_minimum_required( VERSION {data.cmakeVersion} )")

def writeProjectName(data: BuildData, cmakeLists):
  cmakeLists.write(f"project( {data.projectName } )")

def writeImportedLibs(data: BuildData, cmakeLists):
  headerComment(cmakeLists, f"IMPORTED LIBRARIES {conditionalNoneText(data.hasImportedLibraries())}")

  for importedLib in data.importedLibs:
    itemLabel(cmakeLists, f"Imported lib: {importedLib.name}")

    if importedLib.hasIncludeDirs():
      # Write include dirs variable
      importedLib.includeDirs.sort()
      cmakeLists.write(f"set( {includeDirsVariable(importedLib.name)}")

      for includeDir in importedLib.includeDirs:
        cmakeLists.write(f"\n\t{FileWriteUtils.projectSourceDir}/{includeDir}")
      cmakeLists.write('\n)')
      newlines(cmakeLists, 2)

    if importedLib.hasHeaders():
      # Write headers variable
      importedLib.headers.sort()
      cmakeLists.write(f"set( {headersVariable(importedLib.name)}")

      for headerFile in importedLib.headers:
        cmakeLists.write(f"\n\t{FileWriteUtils.projectSourceDir}/{headerFile}")
      cmakeLists.write('\n)')

    # Write library files
    for i in range(0, len(importedLib.libraryFiles)):
      newlines(cmakeLists, 2)
      cmakeLists.write(f"find_library( {FileWriteUtils.mangleLibName(importedLib.name, i)}")
      cmakeLists.write(f"\n\tNAMES {importedLib.libraryFiles[i]}")

      if importedLib.isExternalWithRoot() or not importedLib.isOutsideProjectTree:
        pathPrefix = "" if importedLib.isOutsideProjectTree else FileWriteUtils.projectSourceDir + '/'
        cmakeLists.write(f"\n\tPATHS {pathPrefix}{importedLib.dirContainingLibraryFiles}")

      cmakeLists.write('\n)')

    newlines(cmakeLists, 2)

def writeGeneralOutputData(outputData: OutputItem, data, cmakeLists, containingGroup: OutputGroup = None):
  if outputData.isExe:
    itemLabel(cmakeLists, f"Output executable: {outputData.name}")
  elif outputData.isSharedLib:
    itemLabel(cmakeLists, f"Output shared library: {outputData.name} ")
  elif outputData.isStaticLib:
    itemLabel(cmakeLists, f"Output static library: {outputData.name}")

  # Write headers
  outputData.headers.sort()
  cmakeLists.write(f"set( {headersVariable(outputData.name)}")
  if not containingGroup is None:
    cmakeLists.write(f"\n\t{inBraces(headersVariable(containingGroup.getPrefixedName()))}")
  for linkedLib in outputData.linkedLibs:
    if linkedLib.hasHeaders():
      cmakeLists.write(f"\n\t{inBraces(headersVariable(linkedLib.name))}")
  for headerFile in outputData.headers:
    cmakeLists.write(f"\n\t{FileWriteUtils.projectSourceDir}/{headerFile}")
  cmakeLists.write('\n)')

  newlines(cmakeLists, 2)

  # Write sources, which include the item's headers
  outputData.sources.sort()
  cmakeLists.write(f"set( {sourcesVariable(outputData.name)}")
  if outputData.hasHeaders():
    cmakeLists.write(f"\n\t{inBraces(headersVariable(outputData.name))}")
  if not containingGroup is None:
    cmakeLists.write(f"\n\t{inBraces(sourcesVariable(containingGroup.getPrefixedName()))}")
  if outputData.isExe and outputData.hasMainFile():
    cmakeLists.write(f"\n\t{FileWriteUtils.projectSourceDir}/{outputData.mainFile}")
  for sourceFile in outputData.sources:
    cmakeLists.write(f"\n\t{FileWriteUtils.projectSourceDir}/{sourceFile}")
  cmakeLists.write('\n)')

  newlines(cmakeLists, 2)

  # Write include dirs
  outputData.includeDirs.sort()
  cmakeLists.write(f"set( {includeDirsVariable(outputData.name)}")
  if not containingGroup is None:
    cmakeLists.write(f"\n\t{inBraces(includeDirsVariable(containingGroup.getPrefixedName()))}")
  for linkedLib in outputData.linkedLibs:
    if linkedLib.hasIncludeDirs():
      cmakeLists.write(f"\n\t{inBraces(includeDirsVariable(linkedLib.name))}")
  for includeDir in outputData.includeDirs:
    cmakeLists.write(f"\n\t{FileWriteUtils.projectSourceDir}/{includeDir}")
  cmakeLists.write('\n)')

def writeSharedLib(sharedLib: OutputItem, allData: BuildData, cmakeLists, containingGroup: OutputGroup = None):
  writeGeneralOutputData(sharedLib, allData, cmakeLists, containingGroup)
  newlines(cmakeLists, 2)

  cmakeLists.write(f"add_library( {sharedLib.name} SHARED {inBraces(sourcesVariable(sharedLib.name))} )")
  if sharedLib.hasIncludeDirs():
    cmakeLists.write(f"\ntarget_include_directories( {sharedLib.name} PRIVATE {inBraces(includeDirsVariable(sharedLib.name))} )")

  newlines(cmakeLists, 2)
  writeOutputDirs(sharedLib, cmakeLists)

def writeStaticLib(staticLib: OutputItem, allData: BuildData, cmakeLists, containingGroup: OutputGroup = None):
  writeGeneralOutputData(staticLib, allData, cmakeLists, containingGroup)
  newlines(cmakeLists, 2)

  cmakeLists.write(f"add_library( {staticLib.name} STATIC {inBraces(sourcesVariable(staticLib.name))} )")
  if staticLib.hasIncludeDirs():
    cmakeLists.write(f"\ntarget_include_directories( {staticLib.name} PRIVATE {inBraces(includeDirsVariable(staticLib.name))} )")

  newlines(cmakeLists, 2)
  writeOutputDirs(staticLib, cmakeLists)

def writeExe(exeItem: OutputItem, allData: BuildData, cmakeLists, containingGroup: OutputGroup = None):
  writeGeneralOutputData(exeItem, allData, cmakeLists, containingGroup)
  newlines(cmakeLists, 2)

  cmakeLists.write(f"add_executable( {exeItem.name} {inBraces(sourcesVariable(exeItem.name))} )")
  if exeItem.hasIncludeDirs():
    cmakeLists.write(f"\ntarget_include_directories( {exeItem.name} PRIVATE {inBraces(includeDirsVariable(exeItem.name))} )")

  newlines(cmakeLists, 2)
  writeOutputDirs(exeItem, cmakeLists)

def writeGeneralGroupData(group: OutputGroup, allData: BuildData, cmakeLists):
  groupName = group.getPrefixedName()
  itemLabel(f"Output Group {groupName}")

  # Write headers
  group.headers.sort()
  cmakeLists.write(f"set( {headersVariable(groupName)}")
  for linkedLib in group.linkedLibs:
    if linkedLib.hasHeaders():
      cmakeLists.write(f"\n\t{inBraces(headersVariable(linkedLib.name))}")
  for headerFile in group.headers:
    cmakeLists.write(f"\n\t{FileWriteUtils.projectSourceDir}/{headerFile}")
  cmakeLists.write('\n)')

  newlines(cmakeLists, 2)

  # Write sources, which include the item's headers
  group.sources.sort()
  cmakeLists.write(f"set( {sourcesVariable(groupName)}")
  if group.hasHeaders():
    cmakeLists.write(f"\n\t{inBraces(headersVariable(groupName))}")
  for sourceFile in group.sources:
    cmakeLists.write(f"\n\t{FileWriteUtils.projectSourceDir}/{sourceFile}")
  cmakeLists.write('\n)')

  newlines(cmakeLists, 2)

  # Write include dirs
  group.includeDirs.sort()
  cmakeLists.write(f"set( {includeDirsVariable(groupName)}")
  for linkedLib in group.linkedLibs:
    if linkedLib.hasIncludeDirs():
      cmakeLists.write(f"\n\t{inBraces(includeDirsVariable(linkedLib.name))}")
  for includeDir in group.includeDirs:
    cmakeLists.write(f"\n\t{FileWriteUtils.projectSourceDir}/{includeDir}")
  cmakeLists.write('\n)')

def writeLibraryGroup(group: OutputGroup, allData: BuildData, cmakeLists):
  writeGeneralGroupData(group, allData, cmakeLists)
  newlines(cmakeLists, 2)

  for output in group.outputs:
    if output.isStaticLib:
      writeStaticLib(output, allData, cmakeLists, group)
    else:
      writeSharedLib(output, allData, cmakeLists, group)

def writeExeGroup(group: OutputGroup, allData: BuildData, cmakeLists):
  writeGeneralGroupData(group, allData, cmakeLists)
  newlines(cmakeLists, 2)

  for output in group.outputs:
    writeExe(output, allData, cmakeLists, group)

def writeOutputGroups(data: BuildData, cmakeLists):
  headerComment(cmakeLists, f"LIBRARY OUTPUT GROUPS {conditionalNoneText(data.hasLibOutputGroups())}")
  for libGroup in data.outputGroups:
    if libGroup.isLibraryType():
      writeLibraryGroup(libGroup, data, cmakeLists)

  headerComment(cmakeLists, f"EXECUTABLE OUTPUT GROUPS {conditionalNoneText(data.hasExeOutputGroups())}")
  for exeGroup in data.outputGroups:
    if exeGroup.isExeType:
      writeExeGroup(exeGroup, data, cmakeLists)

def writeOutputs(data: BuildData, cmakeLists):
  headerComment(cmakeLists, f"OUTPUT SHARED LIBRARIES {conditionalNoneText(data.hasSharedLibOutputs())}")
  # Print shared libs
  for sharedLibOutput in data.outputs:
    if sharedLibOutput.isSharedLib:
      writeSharedLib(sharedLibOutput, data, cmakeLists)
      newlines(cmakeLists, 2)

  headerComment(cmakeLists, f"OUTPUT STATIC LIBRARIES {conditionalNoneText(data.hasStaticLibOutputs())}")
  # Print static libs
  for staticLibOutput in data.outputs:
    if staticLibOutput.isStaticLib:
      writeStaticLib(staticLibOutput, data, cmakeLists)
      newlines(cmakeLists, 2)

  writeOutputGroups(data, cmakeLists)

  headerComment(cmakeLists, f"OUTPUT EXECUTABLES {conditionalNoneText(data.hasExecutableOutputs())}")
  # Print executables
  for exeOutput in data.outputs:
    if exeOutput.isExe:
      writeExe(exeOutput, data, cmakeLists)
      newlines(cmakeLists, 2)

def writeSingleLink(targetItemName: str, linkedLibs: list, cmakeLists):
  cmakeLists.write(f"target_link_libraries( {targetItemName}")

  for linkedLibrary in linkedLibs:
    if isinstance(linkedLibrary, OutputItem):
      cmakeLists.write(f"\n\t{linkedLibrary.name} ")
    elif isinstance(linkedLibrary, ImportedLibrary):
      for i in range(0, len(linkedLibrary.libraryFiles)):
        cmakeLists.write(f"\n\t{inBraces(FileWriteUtils.mangleLibName(linkedLibrary.name, i))}")

  cmakeLists.write('\n)')
  newlines(cmakeLists, 2)


def writeLinks(allData: BuildData, cmakeLists):
  headerComment(cmakeLists, "LINK LIBRARIES TO OUTPUTS")

  for group in allData.outputGroups:
    for output in group.outputs:
      if group.hasLinkedLibs() or output.hasLinkedLibs():
        writeSingleLink(output.name, group.linkedLibs + output.linkedLibs, cmakeLists)
    
  for outputItem in allData.outputs:
    if outputItem.hasLinkedLibs():
      writeSingleLink(outputItem.name, outputItem.linkedLibs, cmakeLists)

def writeStandards(allData: BuildData, cmakeLists):
  headerComment(cmakeLists, "LANGUAGE STANDARDS")

  usingCStandardMessage = inQuotes(f"Using C compiler standard --std=c{inBraces('CMAKE_C_STANDARD')}")
  usingCppStandardMessage = inQuotes(f"Using CXX compiler standard --std=c++{inBraces('CMAKE_CXX_STANDARD')}")

  # Default C standard
  cmakeLists.write(f"set( CMAKE_C_STANDARD {allData.defaultCStandard} CACHE STRING {inQuotes('C compiler standard year')} )")

  # Supported C standards
  cmakeLists.write("\nset_property( CACHE CMAKE_C_STANDARD PROPERTY STRINGS ")
  for cStandard in allData.supportedCStandards:
    cmakeLists.write(cStandard + ' ')
  cmakeLists.write(')')

  cmakeLists.write(f"\nmessage( {usingCStandardMessage} )")
  newlines(cmakeLists, 2)

  # Default C++ standard
  cmakeLists.write(f"set( CMAKE_CXX_STANDARD {allData.defaultCppStandard} CACHE STRING {inQuotes('CXX compiler standard year')} )")

  # Supported C++ standards
  cmakeLists.write("\nset_property( CACHE CMAKE_CXX_STANDARD PROPERTY STRINGS ")
  for cppStandard in allData.supportedCppStandards:
    cmakeLists.write(cppStandard + ' ')
  cmakeLists.write(')')

  cmakeLists.write(f"\nmessage( {usingCppStandardMessage} )")

  cmakeLists.write(f"\n\nset( CMAKE_C_STANDARD_REQUIRED ON )")
  cmakeLists.write(f"\nset( CMAKE_CXX_STANDARD_REQUIRED ON )")

  cmakeLists.write(f"\n\nset( CMAKE_C_EXTENSIONS OFF )")
  cmakeLists.write(f"\nset( CMAKE_CXX_EXTENSIONS OFF )")

def writeBuildTargets(allData: BuildData, cmakeLists):
  headerComment(cmakeLists, "BUILD TARGETS")

  cmakeLists.write(f"set_property( CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS ")
  for target in allData.buildTargets:
    cmakeLists.write(inQuotes(target.name) + ' ')
  cmakeLists.write(')')

  newlines(cmakeLists, 2)

  # Default build target
  cmakeLists.write(f"if( {inQuotes(FileWriteUtils.cmakeBuildType)} STREQUAL {FileWriteUtils.emptyQuotes} )")
  cmakeLists.write(f"\n\tset( CMAKE_BUILD_TYPE {inQuotes(allData.defaultBuildTarget)} CACHE STRING \"Project Configuration\" FORCE )")
  cmakeLists.write('\nendif()')

  newlines(cmakeLists)

  i = 0
  for buildTarget in allData.buildTargets:
    if not buildTarget.hasCompilerFlags():
      continue

    newlines(cmakeLists)

    if i == 0:
      cmakeLists.write("if")
    else:
      cmakeLists.write("elseif")
    cmakeLists.write(f"( {inQuotes(FileWriteUtils.cmakeBuildType)} STREQUAL {inQuotes(allData.buildTargets[i].name)} )")

    cmakeLists.write(f"\n\tset( CMAKE_CXX_FLAGS \"")
    for flag in buildTarget.compilerFlags:
      cmakeLists.write(flag + ' ')
    cmakeLists.write("\" )")

    cmakeLists.write(f"\n\tset( CMAKE_C_FLAGS \"")
    for flag in buildTarget.compilerFlags:
      cmakeLists.write(flag + ' ')
    cmakeLists.write('\" )')

    # Increment 'i' so 'elseif' blocks are placed correctly
    i += 1
  cmakeLists.write("\nendif()")

  usingFlagsMessage = inQuotes(f"Using compiler flags: {inBraces('CMAKE_CXX_FLAGS')}")
  buildTypeMessage = inQuotes(f"Building project '{FileWriteUtils.cmakeBuildType}' configuration")

  cmakeLists.write(f"\n\nmessage( {usingFlagsMessage} )")
  cmakeLists.write(f"\nmessage( {buildTypeMessage} )")

def writeImportedLibCopyCommands(allData: BuildData, cmakeLists):
  # TODO: Make this one conditional. Obviously if there are no imported libraries
  # there are also no libraries to copy.
  # TODO: Move this if statement to the main file write function
  if allData.hasImportedLibraries() and allData.hasCopiableImportedLibs():
    headerComment(cmakeLists, "IMPORTED LIBRARY COPY COMMANDS", False)

    for importedLib in allData.importedLibs:
      if importedLib.isExternalWithRoot() or not importedLib.isOutsideProjectTree:
        newlines(cmakeLists, 2)

        # Add command which copies all files from the specified "root directory" of the
        # imported library into the executable directory, so that any shared libraries
        # will be there
        outputLinkedTo = allData.getOutputContainingLinkedLib(importedLib)

        # Try to execute this command when an output which depends on this imported
        # lib is rebuilt
        if outputLinkedTo is None:
          outputLinkedTo = allData.outputs[0].name

        fromPathPrefix = "" if importedLib.isOutsideProjectTree else FileWriteUtils.projectSourceDir + '/'

        itemLabel(cmakeLists, f"Copy libaries imported by {importedLib.name} to executable output dir")
        cmakeLists.write(f"add_custom_command(TARGET {outputLinkedTo.name} POST_BUILD")
        cmakeLists.write(f"\n\tCOMMAND {inBraces('CMAKE_COMMAND')} -E copy_directory")
        cmakeLists.write(f"\n\t\t{fromPathPrefix}{importedLib.dirContainingLibraryFiles}")
        cmakeLists.write(f"\n\t\t{FileWriteUtils.getOutputDir(outputLinkedTo.exeOutputDir)}")
        cmakeLists.write("\n)")

# ////////////////////////////////////////////////////////////////////////////////
# THE MAIN FILE WRITE FUNCTION
# ////////////////////////////////////////////////////////////////////////////////

def writeFile(cmakeLists):
  data = BuildData()

  writeWatermark(cmakeLists)

  writeCmakeVersion(data, cmakeLists)
  newlines(cmakeLists)
  writeProjectName(data, cmakeLists)
  newlines(cmakeLists, 2)

  writeStandards(data, cmakeLists)
  newlines(cmakeLists, 2)

  writeBuildTargets(data, cmakeLists)
  newlines(cmakeLists, 2)

  writeImportedLibs(data, cmakeLists)

  # Already ends in two newlines due to how outputs are written from 'for' loops
  writeOutputs(data, cmakeLists)

  # Already ends in two newlines
  writeLinks(data, cmakeLists)

  writeImportedLibCopyCommands(data, cmakeLists)