import Extensions
import FileRetriever
import Logger
import Tags

class OutputItem:
  def __init__(self, name, outputData):
    self.name = name

    # List of references to ImportedLibs and OutputItems which are libraries
    # These are not loaded in initially. They are added at a later phase by the
    # BuildData class
    self.linkedLibs = [ ]

    self.linkedGroups = [ ]

    self.isExe = False
    self.isStaticLib = False
    self.isSharedLib = False

    self.exeOutputDir = "bin"
    self.libOutputDir = "lib"
    self.archiveOutputDir = "lib"

    self.mainFile = None

    self.loadType(outputData)
    self.loadMainFile(outputData)

    self.sources = FileRetriever.getSourceFiles(outputData)
    self.headers = FileRetriever.getHeaderFiles(outputData)
    self.includeDirs = FileRetriever.getIncludeDirs(outputData)

  # UTILS
  
  def hasHeaders(self):
    for linkedLib in self.linkedLibs:
      if linkedLib.hasHeaders():
        return True

    for linkedGroup in self.linkedGroups:
      for output in linkedGroup.outputs:
        if output.hasHeaders():
          return True
      if linkedGroup.hasHeaders():
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

  def hasMainFile(self):
    return not self.mainFile is None

  def hasLinkedLibs(self):
    return len(self.linkedGroups) > 0 or len(self.linkedLibs) > 0

  def isOfLibraryType(self) -> bool:
    return self.isSharedLib or self.isStaticLib

  # libToLink is OutputItem type
  def linkLib(self, libToLink):
    self.linkedLibs.append(libToLink)

  # groupToLink is OutputGroup type
  def linkGroup(self, groupToLink):
    self.linkedGroups.append(groupToLink)
    # for libToLink in groupToLink.outputs:
    #   self.linkLib(libToLink)

  # LOAD FUNCTIONS

  def loadType(self, outputData):
    if not Tags.TYPE in outputData:
      Logger.logIssueThenQuit(f"{Tags.TYPE} must be specified in output: {self.name}")

    if outputData[Tags.TYPE] == Tags.EXE:
      self.isExe = True
    elif outputData[Tags.TYPE] == Tags.SHARED_LIB:
      self.isSharedLib = True
    elif outputData[Tags.TYPE] == Tags.STATIC_LIB:
      self.isStaticLib = True
    else:
      Logger.logIssueThenQuit(f"Invalid {Tags.TYPE} given to output: {self.name}")

  def loadMainFile(self, outputData):
    if self.isExe and Tags.MAIN_FILE in outputData:
      self.mainFile = outputData[Tags.MAIN_FILE]