import FileRetriever
import Logger
import Tags
from OutputItem import OutputItem
from Globals import OUTPUT_GROUP_NAME_PREFIX

class OutputGroup:
  def __init__(self, name, outputGroupItem):
    self.name = name

    self.areLinkedLibsMerged = False

    self.linkedLibs = [ ]
    self.linkedGroups = [ ]
    self.outputs = [ ]

    self.canToggleLibraryType = False

    self.isExeType = False
    self.isSharedLibType = False
    self.isStaticLibType = False

    self.headers = FileRetriever.getHeaderFiles(outputGroupItem)
    self.sources = FileRetriever.getSourceFiles(outputGroupItem)
    self.includeDirs = FileRetriever.getIncludeDirs(outputGroupItem)

    self.loadType(outputGroupItem)
    self.loadCanToggleType(outputGroupItem)
    self.loadOutputs(outputGroupItem)
  
  def getPrefixedName(self):
    return OUTPUT_GROUP_NAME_PREFIX + self.name

  def getFlattenedGroupLinkedLibs(self) -> list:
    groupOutputs = []
    for group in self.linkedGroups:
      if group.isLibraryType():
        groupOutputs += group.outputs
    return groupOutputs

  def getAllLinkedLibs(self) -> set:
    return set(self.linkedLibs + self.getFlattenedGroupLinkedLibs())

  def hasHeaders(self):
    for linkedLib in self.linkedLibs:
      if linkedLib.hasHeaders():
        return True

    for group in self.linkedGroups:
      for output in group.outputs:
        if output.hasHeaders():
          return True
      if group.hasHeaders():
        return True
    return len(self.headers) > 0
  
  def hasIncludeDirs(self):
    for linkedLib in self.linkedLibs:
      if linkedLib.hasIncludeDirs():
        return True

    for linkedGroup in self.linkedGroups:
      for output in linkedGroup.outputs:
        if output.hasIncludeDirs():
          return True

      if linkedGroup.hasIncludeDirs():
        return True
    return len(self.includeDirs) > 0

  def isLibraryType(self):
    return self.isStaticLibType or self.isSharedLibType

  def hasLinkedLibs(self):
    return len(self.linkedGroups) > 0 or len(self.linkedLibs) > 0

  def hasLibraryThatCanBeToggled(self):
    if not self.isLibraryType():
      return False

    for output in self.outputs:
      if output.canToggleLibraryType:
        return True
    return False

  def isOutputTypeCompatible(self, outputItem: OutputItem) -> bool:
    return self.isExeType and outputItem.isExe or self.isLibraryType() and outputItem.isOfLibraryType()

  def getTypeString(self) -> str:
    if self.isExeType:
      return Tags.EXE
    elif self.isSharedLibType:
      return Tags.SHARED_LIB
    else:
      return Tags.STATIC_LIB

  def linkLib(self, libToLink: OutputItem):
    self.linkedLibs.append(libToLink)
  
  # groupToLink is OutputGruop type
  def linkGroup(self, groupToLink):
    self.linkedGroups.append(groupToLink)

  def isPartOfLinkTree(self, importedLib) -> bool:
    for lib in self.linkedLibs:
      if lib.name == importedLib.name:
        return True
    
    for group in self.linkedGroups:
      if group.isPartOfLinkTree(importedLib):
        return True
      
      for output in group.outputs:
        if output.isPartOfLinkTree(importedLib):
          return True
    return False

  # Call before other load functions in constructor
  def loadType(self, outputGroupItem):
    if not Tags.TYPE in outputGroupItem:
      Logger.logIssueThenQuit(f"{Tags.TYPE} missing from Output Group {self.name}")

    if outputGroupItem[Tags.TYPE] == Tags.EXE:
      self.isExeType = True
    elif outputGroupItem[Tags.TYPE] == Tags.SHARED_LIB:
      self.isSharedLibType = True
    elif outputGroupItem[Tags.TYPE] == Tags.STATIC_LIB:
      self.isStaticLibType = True
    else:
      Logger.logIssueThenQuit(f"Invalid {Tags.TYPE} given to Output Group {self.name}")

  def loadCanToggleType(self, outputGroupItem):
    if self.isLibraryType() and Tags.LIB_TYPE_TOGGLE_POSSIBLE in outputGroupItem:
      self.canToggleLibraryType = outputGroupItem[Tags.LIB_TYPE_TOGGLE_POSSIBLE]

  def loadOutputs(self, outputGroupItem):
    if not Tags.GROUP_OUTPUTS in outputGroupItem:
      Logger.logIssueThenQuit(f"Output group {self.name} missing {Tags.GROUP_OUTPUTS}")

    for name, outputData in outputGroupItem[Tags.GROUP_OUTPUTS].items():
      # Give each output the group's type if one is not present.
      # NOTE: Also avoids OutputItem construction error
      if not Tags.TYPE in outputData:
        outputData[Tags.TYPE] = self.getTypeString()

      # Outputs in the group will match the group's type toggleability if the output does
      # not specify. However, it is not overwritten.
      if not Tags.LIB_TYPE_TOGGLE_POSSIBLE in outputData:
        outputData[Tags.LIB_TYPE_TOGGLE_POSSIBLE] = self.canToggleLibraryType

      self.outputs.append(OutputItem(name, outputData, self))

    if len(self.outputs) == 0:
      Logger.logIssueThenQuit(f"No outputs are defined for Output Group {self.name}")

    for outputItem in self.outputs:
      if not self.isOutputTypeCompatible(outputItem):
        Logger.logIssueThenQuit(f"Output \"{outputItem.name}\" in Output Group {self.name} has incompatible type")