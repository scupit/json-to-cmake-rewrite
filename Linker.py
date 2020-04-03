import Logger
import Tags
from OutputGroup import OutputGroup
from OutputItem import OutputItem
from ImportedLibrary import ImportedLibrary

# groupName gets an output group
def getOutputGroupByName(outputGroups, groupName: str) -> OutputGroup:
  if not '.' in groupName:
    for group in outputGroups:
      if group.name == groupName:
        return group
  return None

# groupName.outputName gets an output in a group
# outputName just gets an individual output item
def getOutputByName(outputGroups, outputItems, outputName: str) -> OutputItem:
  if '.' in outputName:
    groupName, actualOutputName = outputName.split('.')
    
    group = getOutputGroupByName(outputGroups, groupName)
    if not group is None:
      for output in group.outputs:
        if output.name == actualOutputName:
          return output
  else:
    for output in outputItems:
      if output.name == outputName:
        return output

  return None

def getImportedLibByName(importedLibs, importedLibName: str) -> ImportedLibrary:
  for importedLib in importedLibs:
    if importedLib.name == importedLibName:
      return importedLib
  return None

def linkToOutput(linkedLibNames, outputGroups, outputItems, importedLibraries, outputItemLinkingTo: OutputItem, toLinkName: str, itemTypeString: str):
  for linkedLibName in linkedLibNames:
    libLinking = getOutputByName(outputGroups, outputItems, linkedLibName)
    groupLinking = getOutputGroupByName(outputGroups, linkedLibName)
    importedLibLinking = getImportedLibByName(importedLibraries, linkedLibName)

    if not libLinking is None:
      if libLinking.isExeType:
        Logger.logIssueThenQuit(f"Cannot link executable type {linkedLibName} to {toLinkName}")
      elif outputItemLinkingTo.isLibraryType():
        Logger.logIssueThenQuit(f"Please don't link output library \"{linkedLibName}\" to another {itemTypeString} ({toLinkName})")
      else:
        outputItemLinkingTo.linkLib(libLinking)
    elif not groupLinking is None:
      if groupLinking.isExeType:
        Logger.logIssueThenQuit(f"Cannot link exe type group {linkedLibName} to {toLinkName}")
      elif outputItemLinkingTo.isLibraryType():
        Logger.logIssueThenQuit(f"Please don't link output library group \"{linkedLibName}\" to another {itemTypeString} ({toLinkName})")
      else:
        outputItemLinkingTo.linkGroup(groupLinking)
    elif not importedLibLinking is None:
      outputItemLinkingTo.linkLib(importedLibLinking)
    else:
      Logger.logIssueThenQuit(f"Cannot link nonexistent library or group {linkedLibName} to {toLinkName}")

# This is the main linking function
def linkLibrariesToOutputs(linkData, outputGroups, outputItems, importedLibraries):
  for nameLinkingTo, linkedLibNames in linkData.items():
    outputLinkingTo = getOutputByName(outputGroups, outputItems, nameLinkingTo)
    groupLinkingTo = getOutputGroupByName(outputGroups, nameLinkingTo)

    if not outputLinkingTo is None:
      linkToOutput(linkedLibNames, outputGroups, outputItems, importedLibraries, outputLinkingTo, nameLinkingTo, "output library")
    elif not groupLinkingTo is None:
      linkToOutput(linkedLibNames, outputGroups, outputItems, importedLibraries, groupLinkingTo, nameLinkingTo, "output library group")
    else:
      Logger.logIssueThenQuit(f"Tried linking to output or group \"{nameLinkingTo}\", which does not exist")