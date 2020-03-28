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
    self.outputs = [ ]

    self.isExeType = False
    self.isSharedLibType = False
    self.isStaticLibType = False

    self.headers = FileRetriever.getHeaderFiles(outputGroupItem)
    self.sources = FileRetriever.getSourceFiles(outputGroupItem)
    self.includeDirs = FileRetriever.getIncludeDirs(outputGroupItem)

    self.loadType(outputGroupItem)
    self.loadOutputs(outputGroupItem)
  
  def getPrefixedName(self):
    return OUTPUT_GROUP_NAME_PREFIX + self.name

  def hasHeaders(self):
    return len(self.headers) > 0
  
  def hasSources(self):
    return len(self.sources) > 0
  
  def hasIncludeDirs(self):
    return len(self.includeDirs) > 0

  def isLibraryType(self):
    return self.isStaticLibType or self.isSharedLibType

  def hasLinkedLibs(self):
    return len(self.linkedLibs) > 0

  def isOutputTypeCompatible(self, outputItem: OutputItem) -> bool:
    return self.isExeType and outputItem.isExe or self.isLibraryType() and outputItem.isOfLibraryType()

  def getTypeString(self) -> str:
    if self.isExeType:
      return Tags.EXE
    elif self.isSharedLibType:
      return Tags.SHARED_LIB
    else:
      return Tags.STATIC_LIB

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

  def loadOutputs(self, outputGroupItem):
    if not Tags.GROUP_OUTPUTS in outputGroupItem:
      Logger.logIssueThenQuit(f"Output group {self.name} missing {Tags.GROUP_OUTPUTS}")

    for name, outputData in outputGroupItem[Tags.GROUP_OUTPUTS]:
      # Give each output the group's type if one is not present.
      # NOTE: Also avoids OutputItem construction error
      if not Tags.TYPE in outputData:
        outputData[Tags.TYPE] = self.getTypeString()
      self.outputs.append(OutputItem(name, outputData))

    if len(self.outputs) == 0:
      Logger.logIssueThenQuit(f"No outputs are defined for Output Group {self.name}")

    for outputItem in self.outputs:
      if not self.isOutputTypeCompatible(outputItem):
        Logger.logIssueThenQuit(f"Output \"{outputItem.name}\" in Output Group {self.name} has incompatible type")