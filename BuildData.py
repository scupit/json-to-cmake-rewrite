import json

import FileHelper
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

  def loadProjectName(self, jsonData):
    if Tags.PROJECT_NAME in jsonData:
      self.projectName = jsonData[Tags.PROJECT_NAME]

  def loadDefaultBuildTarget(self, jsonData):
    if Tags.DEFAULT_BUILD_TARGET in jsonData:
      targetExists = False
      for target in self.buildTargets:
        if target.name == jsonData[Tags.DEFAULT_BUILD_TARGET]
          targetExists = True
          break
      
      if targetExists:
        self.defaultBuildTarget = jsonData[Tags.DEFAULT_BUILD_TARGET]
      else:
        Logger.logIssueThenQuit(f"{Tags.DEFAULT_BUILD_TARGET} must exist in {Tags.BUILD_TARGETS}")

  # Call inside loadStandards(...)
  def loadDefaultStandards(self, jsonData):
    if Tags.DEFAULT_C_STANDARD in jsonData:
      if jsonData[Tags.DEFAULT_C_STANDARD] in self.supportedCStandards:
        self.defaultCStandard = jsonData[Tags.C_STANDARDS]
      else
        Logger.logIssueThenQuit(f"{Tags.DEFAULT_C_STANDARD} must be present in {Tags.C_STANDARDS}")
    
    if Tags.DEFAULT_CPP_STANDARD in jsonData:
      if jsonData[Tags.DEFAULT_CPP_STANDARD] in self.supportedCppStandards:
        self.defaultCppStandard = jsonData[Tags.CPP_STANDARDS]
      else:
        Logger.logIssueThenQuit(f"{Tags.DEFAULT_CPP_STANDARD} must be present in {Tags.CPP_STANDARDS}")

  def loadStandards(self, jsonData):
    if Tags.C_STANDARDS in jsonData:
      self.supportedCStandards = jsonData[Tags.C_STANDARDS]

    if Tags.CPP_STANDARDS in jsonData:
      self.supportedCppStandards = jsonData[Tags.CPP_STANDARDS]

    self.loadDefaultStandards(jsonData)

  def loadOutputs(self, jsonData):
    if not Tags.OUTPUT in jsonData or len(jsonData[Tags.OUTPUT]) == 0:
      Logger.logIssueThenQuit(f"Must define at least one {Tags.OUTPUT}")

    for name, outputData in jsonData[Tags.OUTPUT].items():
      self.outputs.append(OutputItem(name, outputData))

  def loadImportedLibs(self, jsonData):
    if Tags.IMPORTED_LIBRARIES in jsonData:
      for name, importedLibData in jsonData[Tags.IMPORTED_LIBRARIES].items():
        self.importedLibs.append(ImportedLibrary(name, importedLibData))

  def loadBuildTargets(self, jsonData):
    if not Tags.BUILD_TARGETS in jsonData or len(jsonData[Tags.BUILD_TARGETS]) == 0:
      Logger.logIssueThenQuit(f"Must define at least one {Tags.BUILD_TARGETS}")

    for name, buildTargetData in jsonData[Tags.BUILD_TARGETS].items():
      self.buildTargets.append(BuildTarget(name, buildTargetData))

    self.loadDefaultBuildTarget(jsonData)