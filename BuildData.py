import json

import FileHelper
import GitHelper
import Globals
import Linker
import Logger
import Tags

from BuildTarget import BuildTarget
from ImportedLibrary import ImportedLibrary
from OutputItem import OutputItem
from OutputGroup import OutputGroup

class BuildData:
  def __init__(self):
    self.cmakeVersion = Globals.CMAKE_VERSION

    self.projectName = FileHelper.getProjectName()

    self.defaultCppStandard = None
    self.defaultCStandard = None

    self.supportedCppStandards = [ ]
    self.supportedCStandards = [ ]

    self.outputs = [ ]
    self.outputGroups = [ ]
    self.importedLibs = [ ]
    self.buildTargets = [ ]

    self.defaultBuildTarget = None

    with open(FileHelper.getAbsolutePath(Globals.JSON_FILE_NAME)) as jsonFile:
      jsonData = json.load(jsonFile)

      self.loadProjectName(jsonData)

      self.loadOutputs(jsonData)
      self.loadOutputGroups(jsonData)
      self.validateOutputs()

      self.loadImportedLibs(jsonData)

      self.loadBuildTargets(jsonData)
      self.loadStandards(jsonData)

      if Tags.LINKS in jsonData:
        Linker.linkLibrariesToOutputs(jsonData[Tags.LINKS], self.outputGroups, self.outputs, self.importedLibs)

  # UTILS

  def anyOutputsDefined(self):
    return len(self.outputs) > 0 or len(self.outputGroups) > 0

  # Call at the end of loadImportedLibs
  def createImportedLibraryDirs(self):
    for importedLib in self.importedLibs:
      if not importedLib.isOutsideProjectTree:
        FileHelper.createDirPath(f"{Globals.DEPENDENCY_DIR}/{Globals.DEPENDENCY_LIB_DIR}/{importedLib.generatedDepDirname}")
      FileHelper.createDirPath(f"{Globals.DEPENDENCY_DIR}/{Globals.DEPENDENCY_INCLUDE_DIR}/{importedLib.generatedDepDirname}")

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

  def hasExeOutputGroups(self) -> bool:
    for group in self.outputGroups:
      if group.isExeType:
        return True
    return False

  def hasLibOutputGroups(self) -> bool:
    for group in self.outputGroups:
      if group.isLibraryType():
        return True
    return False

  def hasImportedLibraries(self) -> bool:
    return len(self.importedLibs) > 0

  def hasLinks(self) -> bool:
    for output in self.outputs:
      if output.hasLinks():
        return True
    
    for group in self.outputGroups:
      if group.hasLinkes():
        return True
      
      for ouptut in group.outputs:
        if output.hasLinks():
          return True
    return False

  def hasCopiableImportedLibs(self) -> bool:
    for importedLib in self.importedLibs:
      if importedLib.isExternalWithRoot() or not importedLib.isOutsideProjectTree:
        return True
    return False

  def hasLibraryThatCanBeToggled(self) -> bool:
    for group in self.outputGroups:
      if group.hasLibraryThatCanBeToggled():
        return True
    
    for output in self.outputs:
      if output.canToggleLibraryType:
        return True
    return False

  def getExesPartOfLinkTree(self, linkedLibSearchingFor) -> list:
    exesLinkedTo = [ ]

    for output in self.outputs:
      if output.isExe and output.isPartOfLinkTree(linkedLibSearchingFor):
        exesLinkedTo.append(output)

    for group in self.outputGroups:
      for output in group.outputs:
        if output.isExe and output.isPartOfLinkTree(linkedLibSearchingFor):
          exesLinkedTo.append(output)
    return exesLinkedTo

  # LOAD FUNCTIONS

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
    if Tags.OUTPUT in jsonData:
      for name, outputData in jsonData[Tags.OUTPUT].items():
        self.outputs.append(OutputItem(name, outputData))

  def loadOutputGroups(self, jsonData):
    if Tags.OUTPUT_GROUPS in jsonData:
      for name, outputGroupData in jsonData[Tags.OUTPUT_GROUPS].items():
        self.outputGroups.append(OutputGroup(name, outputGroupData))

  def loadImportedLibs(self, jsonData):
    if Tags.IMPORTED_LIBRARIES in jsonData:
      for name, importedLibData in jsonData[Tags.IMPORTED_LIBRARIES].items():
        importedLib = ImportedLibrary(name, importedLibData)
        self.importedLibs.append(importedLib)

        if importedLib.shouldCloneRepo and not importedLib.gitRepoToClone is None:
          GitHelper.cloneRepoIfNonexistent(importedLib.gitRepoToClone, importedLib.generatedDepDirname)
    
    self.createImportedLibraryDirs()

  def loadBuildTargets(self, jsonData):
    if not Tags.BUILD_TARGETS in jsonData or len(jsonData[Tags.BUILD_TARGETS]) == 0:
      Logger.logIssueThenQuit(f"Must define at least one {Tags.BUILD_TARGETS}")

    for name, buildTargetData in jsonData[Tags.BUILD_TARGETS].items():
      self.buildTargets.append(BuildTarget(name, buildTargetData))

    self.loadDefaultBuildTarget(jsonData)

  # Call only after loading all outputs and outputGroups
  def validateOutputs(self):
    if not self.anyOutputsDefined():
      Logger.logIssueThenQuit(f"Must define at least one {Tags.OUTPUT} or {Tags.OUTPUT_GROUPS}")

    # Since outputs can now be defined in groups (outside of the single outputs object),
    # we now need to check for name collisions. Check both group names and output names
    outputNames = dict()

    # self.outputs values come from a json object, so it's already guaranteed to have no duplicates
    for output in self.outputs:
      outputNames[output.name] = True

    for group in self.outputGroups:
      if group.name in outputNames:
        Logger.logIssueThenQuit(f"Group name {group.name} collides with an output name")
      for output in group.outputs:
        if output.name in outputNames:
          Logger.logIssueThenQuit(f"Colliding output name \"{output.name}\" found in Output Group \"{group.name}\"")

    for importedLib in self.importedLibs:
      if importedLib.name in outputNames:
        Logger.logIssueThenQuit(f"Imported Library name \"{importedLib.name}\" collides with an existing output or group name")
    