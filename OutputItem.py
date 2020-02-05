import Extensions
import FileRetriever
import Logger
import Tags

def hasAnySourceTags(outputData):
  return Tags.R_SOURCE_DIRS in outputData\
    or Tags.SOURCE_DIRS in outputData\
    or Tags.INDIVIDUAL_SOURCES in outputData

def hasAnyHeaderTags(outputData):
  return Tags.R_HEADER_DIRS in outputData\
    or Tags.HEADER_DIRS in outputData\
    or Tags.INDIVIDUAL_HEADERS in outputData

class OutputItem:
  name = ""

  sources = [ ]
  headers = [ ]
  includeDirs = [ ]

  # List of references to ImportedLibs and OutputItems which are libraries
  # These are not loaded in initially. They are added at a later phase by the
  # BuildData class
  linkedLibs = [ ]

  isExe = False
  isStaticLib = False
  isSharedLib = False

  exeOutputDir = "bin"
  libOutputDir = "lib"
  archiveOutputDir = "lib"

  mainFile = None

  def __init__(self, name, outputData):
    self.name = name
    self.linkedLibs = [ ]

    self.loadType(outputData)
    self.loadMainFile(outputData)
    self.loadSources(outputData)
    self.loadHeaders(outputData)
    self.loadIncludeDirs(outputData)

  # UTILS
  
  def hasSources(self):
    for linkedLib in self.linkedLibs:
      if isinstance(linkedLib, OutputItem) and linkedLib.hasSources():
        return True
    return len(self.sources) > 0
  
  def hasHeaders(self):
    for linkedLib in self.linkedLibs:
      if linkedLib.hasHeaders():
        return True
    return len(self.headers) > 0

  def hasIncludeDirs(self):
    for linkedLib in self.linkedLibs:
      if linkedLib.hasIncludeDirs():
        return True
    return len(self.includeDirs) > 0

  def hasMainFile(self):
    return not self.mainFile is None

  def hasLinkedLibs(self):
    return len(self.linkedLibs) > 0

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
  
  def loadSources(self, outputData):
    self.sources = FileRetriever.getSourceFiles(outputData)

  def loadHeaders(self, outputData):
    self.headers = FileRetriever.getHeaderFiles(outputData)

  def loadIncludeDirs(self, outputData):
    self.includeDirs = FileRetriever.getIncludeDirs(outputData)