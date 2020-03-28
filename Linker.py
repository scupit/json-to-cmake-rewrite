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

# TODO: Clean up these two link functions. The can probably be combined of outputs and output groups inherit linking and type checking functions
# toLinkName may be different from output item name if the output item is in a group. Ex: "groupName.outputName" vs "outputName"
def linkToIndividualOutput(linkedLibNames, outputGroups, outputItems, importedLibraries, outputItemLinkingTo: OutputItem, toLinkName: str):
  for linkedLibName in linkedLibNames:
    libLinking = getOutputByName(outputGroups, outputItems, linkedLibName)
    groupLinking = getOutputGroupByName(outputGroups, linkedLibName)
    importedLibLinking = getImportedLibByName(importedLibraries, linkedLibName)

    if not libLinking is None:
      if libLinking.isExe:
        Logger.logIssueThenQuit(f"Cannot link executable type {linkedLibName} to {toLinkName}")
      elif outputItemLinkingTo.isOfLibraryType():
        Logger.logIssueThenQuit(f"Please don't link output library \"{linkedLibName}\" to another output library ({toLinkName})")
      else:
        outputItemLinkingTo.linkedLibs.append(libLinking)
    elif not groupLinking is None:
      if groupLinking.isExeType:
        Logger.logIssueThenQuit(f"Cannot link exe type group {linkedLibName} to {toLinkName}")
      elif outputItemLinkingTo.isOfLibraryType():
        Logger.logIssueThenQuit(f"Please don't link output library group \"{linkedLibName}\" to another output library ({toLinkName})")
      else:
        for lib in groupLinking.outputs:
          outputItemLinkingTo.linkedLibs.append(lib)
    elif not importedLibLinking is None:
      outputItemLinkingTo.linkedLibs.append(importedLibLinking)
    else:
      Logger.logIssueThenQuit(f"Cannot link nonexistent library or group {linkedLibName} to {toLinkName}")

def linkToOutputGroup(linkedLibNames, outputGroups, outputItems, importedLibraries, outputGroupLinkingTo: OutputGroup, toLinkName: str):
  for linkedLibName in linkedLibNames:
    libLinking = getOutputByName(outputGroups, outputItems, linkedLibName)
    groupLinking = getOutputGroupByName(outputGroups, linkedLibName)
    importedLibLinking = getImportedLibByName(importedLibraries, linkedLibName)

    if not libLinking is None:
      if libLinking.isExe:
        Logger.logIssueThenQuit(f"Cannot link executable type {linkedLibName} to {toLinkName}")
      elif outputGroupLinkingTo.isLibraryType():
        Logger.logIssueThenQuit(f"Please don't link output library \"{linkedLibName}\" to an output library group ({toLinkName})")
      else:
        outputGroupLinkingTo.linkedLibs.append(libLinking)
    elif not groupLinking is None:
      if groupLinking.isExeType:
        Logger.logIssueThenQuit(f"Cannot link exe type group {linkedLibName} to {toLinkName}")
      elif outputGroupLinkingTo.isLibraryType():
        Logger.logIssueThenQuit(f"Please don't link output library group \"{linkedLibName}\" to another output library group ({toLinkName})")
      else:
        for lib in groupLinking.outputs:
          outputGroupLinkingTo.linkedLibs.append(lib)
    elif not importedLibLinking is None:
      outputGroupLinkingTo.linkedLibs.append(importedLibLinking)
    else:
      Logger.logIssueThenQuit(f"Cannot link nonexistent library or group {linkedLibName} to {toLinkName}")

# This is the main linking function
def linkLibrariesToOutputs(linkData, outputGroups, outputItems, importedLibraries):
  for nameLinkingTo, linkedLibNames in linkData:
    # TODO: Determine whether the name refers to a group or individual output, then link from there
    outputLinkingTo = getOutputByName(nameLinkingTo)
    groupLinkingTo = getOutputGroupByName(nameLinkingTo)

    if not outputLinkingTo is None:
      linkToIndividualOutput(linkedLibNames, outputGroups, outputItems, importedLibraries, outputLinkingTo, nameLinkingTo)
    elif not groupLinkingTo is None:
      linkToOutputGroup(linkedLibNames, outputGroups, outputItems, importedLibraries, groupLinkingTo, nameLinkingTo)
    else:
      Logger.logIssueThenQuit(f"Tried linking to output or group \"{nameLinkingTo}\", which does not exist")