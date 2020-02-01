import json
from Globals import JSON_FILE_NAME
from OutputItem import OutputItem
from Tags import OUTPUT
from FileHelper import getAbsolutePath

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
    with open(getAbsolutePath(JSON_FILE_NAME)) as jsonFile:
      jsonData = json.load(jsonFile)

      self.loadOutputs(jsonData)

  def loadOutputs(self, jsonData):
    for name, outputData in jsonData[OUTPUT].items():
      self.outputs.append(OutputItem(name, outputData))