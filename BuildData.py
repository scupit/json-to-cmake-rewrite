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

  projectName = ""

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

      self.loadOutputs(jsonData)
      self.loadImportedLibs(jsonData)
      self.loadBuildTargets(jsonData)

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