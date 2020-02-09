import json

import FileHelper
import GitHelper
import Globals
import Logger
import Tags

from BuildTarget import BuildTarget
from ImportedLibrary import ImportedLibrary
from OutputItem import OutputItem

class BuildData:
  cmakeVersion = Globals.CMAKE_VERSION

  projectName = FileHelper.getProjectName()

  defaultCppStandard = None
  defaultCStandard = None

  supportedCppStandards = [ ]
  supportedCStandards = [ ]

  outputs = [ ]
  importedLibs = [ ]
  buildTargets = [ ]

  defaultBuildTarget = None

  def __init__(self):
    with open(FileHelper.getAbsolutePath(Globals.JSON_FILE_NAME)) as jsonFile:
      jsonData = json.load(jsonFile)

      self.loadProjectName(jsonData)

      self.loadOutputs(jsonData)
      self.loadImportedLibs(jsonData)

      self.loadBuildTargets(jsonData)
      self.loadStandards(jsonData)

      self.linkLibsToOutputs(jsonData)

  # UTILS

  # Call at the end of loadImportedLibs
  def createImportedLibraryDirs(self):
    for importedLib in self.importedLibs:
      if not importedLib.isOutsideProjectTree:
        FileHelper.createDirPath(f"{Globals.DEPENDENCY_DIR}/{Globals.DEPENDENCY_LIB_DIR}/{importedLib.name}")
      FileHelper.createDirPath(f"{Globals.DEPENDENCY_DIR}/{Globals.DEPENDENCY_INCLUDE_DIR}/{importedLib.name}")

  def hasSharedLibOutputs(self) -> bool:
    for output in self.outputs:
      if output.isSharedLib:
        return True
    return False

  def hasStaticLibOutputs(self) -> bool:
    for output in self.outputs:
      if output.isStaticLib:
        return True
    return False

  def hasExecutableOutputs(self) -> bool:
    for output in self.outputs:
      if output.isExe:
        return True
    return False

  def hasImportedLibraries(self) -> bool:
    return len(self.importedLibs) > 0

  def hasCopiableImportedLibs(self) -> bool:
    for importedLib in self.importedLibs:
      if importedLib.isExternalWithRoot() or not importedLib.isOutsideProjectTree:
        return True
    return False

  def getOutputByName(self, outputName: str) -> OutputItem:
    for output in self.outputs:
      if output.name == outputName:
        return output
    return None

  def getImportedLibByName(self, importedLibName: str) -> ImportedLibrary:
    for importedLib in self.importedLibs:
      if importedLib.name == importedLibName:
        return importedLib
    return None

  def getOutputContainingLinkedLib(self, linkedLibSearchingFor) -> OutputItem:
    for output in self.outputs:
      for linkedLib in output.linkedLibs:
        if linkedLib.name == linkedLibSearchingFor.name:
          return output
    return none

  # LOAD FUNCTIONS

  def linkLibsToOutputs(self, jsonData):
    if Tags.LINKS in jsonData:
      for outputName, linkedLibs in jsonData[Tags.LINKS].items():
        outputLinkingTo = self.getOutputByName(outputName)

        if outputLinkingTo is None:
          Logger.logIssueThenQuit(f"Tried linking to output {outputName} which does not exist")

        for linkedLibName in linkedLibs:
          outputLibLinking = self.getOutputByName(linkedLibName)
          importedLibLinking = self.getImportedLibByName(linkedLibName)

          if not outputLibLinking is None:
            if outputLibLinking.isSharedLib or outputLibLinking.isStaticLib:
              if outputLinkingTo.isSharedLib or outputLinkingTo.isStaticLib:
                Logger.logIssueThenQuit(f"Please don't link output library {linkedLibName} to {outputName}, as this could cause issues")
              else:
                outputLinkingTo.linkedLibs.append(outputLibLinking)
            else:
              Logger.logIssueThenQuit(f"Cannot link non-library output {linkedLibName} to {outputName}")
          elif not importedLibLinking is None:
            outputLinkingTo.linkedLibs.append(importedLibLinking)
          else:
            Logger.logIssueThenQuit(f"Cannot link nonexistent library {linkedLibName} to {outputName}")

  def loadProjectName(self, jsonData):
    if Tags.PROJECT_NAME in jsonData:
      self.projectName = jsonData[Tags.PROJECT_NAME]

  def loadDefaultBuildTarget(self, jsonData):
    if Tags.DEFAULT_BUILD_TARGET in jsonData:
      targetExists = False
      for target in self.buildTargets:
        if target.name == jsonData[Tags.DEFAULT_BUILD_TARGET]:
          targetExists = True
          break
      
      if targetExists:
        self.defaultBuildTarget = jsonData[Tags.DEFAULT_BUILD_TARGET]
      else:
        Logger.logIssueThenQuit(f"{Tags.DEFAULT_BUILD_TARGET} must exist in {Tags.BUILD_TARGETS}")
    else:
      self.defaultBuildTarget = self.buildTargets[0].name

  # Call inside loadStandards(...)
  def loadDefaultStandards(self, jsonData):
    if Tags.DEFAULT_C_STANDARD in jsonData:
      if not self.cStandardsDefinedByUser:
        self.supportedCStandards = [ jsonData[Tags.DEFAULT_C_STANDARD] ]

      if jsonData[Tags.DEFAULT_C_STANDARD] in self.supportedCStandards:
        self.defaultCStandard = jsonData[Tags.DEFAULT_C_STANDARD]
      else:
        Logger.logIssueThenQuit(f"{Tags.DEFAULT_C_STANDARD} must be present in {Tags.C_STANDARDS}")
    else:
      # Ensure a default C standard exists
      self.defaultCStandard = self.supportedCStandards[0]
    
    if Tags.DEFAULT_CPP_STANDARD in jsonData:
      if not self.cppStandardsDefinedByUser:
        self.supportedCppStandards = [ jsonData[Tags.DEFAULT_CPP_STANDARD] ]

      if jsonData[Tags.DEFAULT_CPP_STANDARD] in self.supportedCppStandards:
        self.defaultCppStandard = jsonData[Tags.DEFAULT_CPP_STANDARD]
      else:
        Logger.logIssueThenQuit(f"{Tags.DEFAULT_CPP_STANDARD} must be present in {Tags.CPP_STANDARDS}")
    else:
      # Ensure a default C++ standard exists
      self.defaultCppStandard = self.supportedCppStandards[0]

  def loadStandards(self, jsonData):
    if Tags.C_STANDARDS in jsonData:
      self.supportedCStandards = jsonData[Tags.C_STANDARDS]
      self.cStandardsDefinedByUser = True
    else:
      # Ensure there is always at least one C standard
      self.supportedCStandards.append(Globals.DEFAULT_C_STANDARD)
      self.cStandardsDefinedByUser = False

    if Tags.CPP_STANDARDS in jsonData:
      self.supportedCppStandards = jsonData[Tags.CPP_STANDARDS]
      self.cppStandardsDefinedByUser = True
    else:
      # Ensure there is always at least one C++ standard
      self.supportedCppStandards.append(Globals.DEFAULT_CPP_STANDARD)
      self.cppStandardsDefinedByUser = False

    self.loadDefaultStandards(jsonData)

  def loadOutputs(self, jsonData):
    if not Tags.OUTPUT in jsonData or len(jsonData[Tags.OUTPUT]) == 0:
      Logger.logIssueThenQuit(f"Must define at least one {Tags.OUTPUT}")

    for name, outputData in jsonData[Tags.OUTPUT].items():
      self.outputs.append(OutputItem(name, outputData))

  def loadImportedLibs(self, jsonData):
    if Tags.IMPORTED_LIBRARIES in jsonData:
      for name, importedLibData in jsonData[Tags.IMPORTED_LIBRARIES].items():
        importedLib = ImportedLibrary(name, importedLibData)
        self.importedLibs.append(importedLib)

        if importedLib.shouldCloneRepo and not importedLib.gitRepoToClone is None:
          GitHelper.cloneRepoIfNonexistent(importedLib.gitRepoToClone)
    
    self.createImportedLibraryDirs()

  def loadBuildTargets(self, jsonData):
    if not Tags.BUILD_TARGETS in jsonData or len(jsonData[Tags.BUILD_TARGETS]) == 0:
      Logger.logIssueThenQuit(f"Must define at least one {Tags.BUILD_TARGETS}")

    for name, buildTargetData in jsonData[Tags.BUILD_TARGETS].items():
      self.buildTargets.append(BuildTarget(name, buildTargetData))

    self.loadDefaultBuildTarget(jsonData)