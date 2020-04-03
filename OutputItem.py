import Extensions
import FileRetriever
import Logger
import Tags

from OutputBase import OutputBase

class OutputItem(OutputBase):
  def __init__(self, name, outputData, groupContainedIn = None):
    super().__init__(name, outputData)
    self.groupContainedIn = groupContainedIn

    self.exeOutputDir = "bin"
    self.libOutputDir = "lib"
    self.archiveOutputDir = "lib"

    self.mainFile = None
    self.loadMainFile(outputData)

  # UTILS

  def getAllLinkedLibs(self) -> set:
    return set(self.linkedLibs + self.getFlattenedGroupLinkedLibs())

  def isContainedInGroup(self) -> bool:
    return not self.groupContainedIn is None

  def parentGroupHasHeaders(self) -> bool:
    return self.isContainedInGroup() and self.groupContainedIn.hasHeaders()

  def parentGroupHasIncludeDirs(self) -> bool:
    return self.isContainedInGroup() and self.groupContainedIn.hasIncludeDirs()

  def hasHeaders(self):
    return super().hasHeaders() or len(self.headers) > 0 or self.parentGroupHasHeaders()

  def hasIncludeDirs(self):
    return super().hasIncludeDirs() or len(self.includeDirs) > 0 or self.parentGroupHasIncludeDirs()

  def hasMainFile(self):
    return not self.mainFile is None

  # libToLink is OutputItem type
  def linkLib(self, libToLink):
    self.linkedLibs.append(libToLink)

  # groupToLink is OutputGroup type
  def linkGroup(self, groupToLink):
    self.linkedGroups.append(groupToLink)

  def isPartOfLinkTree(self, importedLib) -> bool:
    return super().isPartOfLinkTree(importedLib) or (self.isContainedInGroup() and self.groupContainedIn.isPartOfLinkTree(importedLib))

  # LOAD FUNCTIONS

  def loadType(self, outputItemData):
    super().loadType(outputItemData, "Output")

  def loadMainFile(self, outputData):
    if self.isExeType and Tags.MAIN_FILE in outputData:
      self.mainFile = outputData[Tags.MAIN_FILE]