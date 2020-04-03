import FileRetriever
import Logger
import Tags

class OutputBase:
  def __init__(self, name, outputItemData):
    self.name = name

    # List of references to ImportedLibs and OutputItems which are libraries
    # These are not loaded in initially. They are added at a later phase by the
    # BuildData class
    self.linkedLibs = [ ]
    self.linkedGroups = [ ]

    self.canToggleLibraryType = False

    self.isExeType = False
    self.isStaticLibType = False
    self.isSharedLibType = False

    self.headers = FileRetriever.getHeaderFiles(outputItemData)
    self.sources = FileRetriever.getSourceFiles(outputItemData)
    self.includeDirs = FileRetriever.getIncludeDirs(outputItemData)

    self.loadType(outputItemData)
    self.loadCanToggleType(outputItemData)

  def getFlattenedGroupLinkedLibs(self) -> list:
    groupOutputs = []
    for group in self.linkedGroups:
      if group.isLibraryType():
        groupOutputs += group.outputs
    return groupOutputs

  def hasLinkedLibs(self) -> bool:
    return len(self.linkedGroups) > 0 or len(self.linkedLibs) > 0

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

  def isLibraryType(self) -> bool:
    return self.isSharedLibType or self.isStaticLibType

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
  def loadType(self, outputItemData, itemTypeString: str):
    if not Tags.TYPE in outputItemData:
      Logger.logIssueThenQuit(f"{Tags.TYPE} missing from {itemTypeString} {self.name}")

    if outputItemData[Tags.TYPE] == Tags.EXE:
      self.isExeType = True
    elif outputItemData[Tags.TYPE] == Tags.SHARED_LIB:
      self.isSharedLibType = True
    elif outputItemData[Tags.TYPE] == Tags.STATIC_LIB:
      self.isStaticLibType = True
    else:
      Logger.logIssueThenQuit(f"Invalid {Tags.TYPE} given to {itemTypeString} {self.name}")

  def loadCanToggleType(self, outputItemData):
    if self.isLibraryType() and Tags.LIB_TYPE_TOGGLE_POSSIBLE in outputItemData:
      self.canToggleLibraryType = outputItemData[Tags.LIB_TYPE_TOGGLE_POSSIBLE]