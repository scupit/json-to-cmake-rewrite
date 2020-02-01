import json
from Globals import JSON_FILE_NAME
from OutputItem import OutputItem
from Tags import OUTPUT
from FileHelper import getAbsolutePath


with open(getAbsolutePath(JSON_FILE_NAME)) as jsonFile:
  jsonData = json.load(jsonFile)

  outputs = [ ]
  for name, output in jsonData[OUTPUT].items():
    outputs.append(OutputItem(name, output))

  print(outputs[0].isSharedLib)
