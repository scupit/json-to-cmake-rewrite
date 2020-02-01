import json
from Globals import JSON_FILE_NAME
import Tags
import FileHelper

from ImportedLibrary import ImportedLibrary
from OutputItem import OutputItem

class BuildData:
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
    with open(FileHelper.getAbsolutePath(JSON_FILE_NAME)) as jsonFile:
      jsonData = json.load(jsonFile)

      self.loadOutputs(jsonData)
      self.loadImportedLibs(jsonData)

  def loadOutputs(self, jsonData):
    for name, outputData in jsonData[Tags.OUTPUT].items():
      self.outputs.append(OutputItem(name, outputData))

  def loadImportedLibs(self, jsonData):
    for name, importedLibData in jsonData[Tags.IMPORTED_LIBRARIES].items():
      self.importedLibs.append(ImportedLibrary(name, importedLibData))