import FileRetriever
import Logger
import Tags
from OutputItem import OutputItem
from OutputBase import OutputBase
from Globals import OUTPUT_GROUP_NAME_PREFIX

class OutputGroup(OutputBase):
  def __init__(self, name, outputGroupItem):
    super().__init__(name, outputGroupItem)
    self.outputs = [ ]
    self.loadOutputs(outputGroupItem)
  
  def getPrefixedName(self):
    return OUTPUT_GROUP_NAME_PREFIX + self.name

  def getAllLinkedLibs(self) -> set:
    return set(self.linkedLibs + self.getFlattenedGroupLinkedLibs())

  def hasLibraryThatCanBeToggled(self):
    if not self.isLibraryType():
      return False

    for output in self.outputs:
      if output.canToggleLibraryType:
        return True
    return False

  def isOutputTypeCompatible(self, outputItem: OutputItem) -> bool:
    return self.isExeType and outputItem.isExeType or self.isLibraryType() and outputItem.isLibraryType()

  def getTypeString(self) -> str:
    if self.isExeType:
      return Tags.EXE
    elif self.isSharedLibType:
      return Tags.SHARED_LIB
    else:
      return Tags.STATIC_LIB

  def loadType(self, outputItemData):
    super().loadType(outputItemData, "Output Group")

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