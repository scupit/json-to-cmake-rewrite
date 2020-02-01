import Extensions
import FileRetriever
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
  sources = [ ]
  headers = [ ]
  includeDirs = [ ]

  isExe = False
  isStaticLib = False
  isSharedLib = False

  exeOutputDir = "bin"
  libOutputDir = "lib"
  archiveOutputDir = "lib"

  mainFile = None

  def __init__(self, name, outputData):
    self.name = name

    self.loadType(outputData)
    self.loadMainFile(outputData)
    self.loadOutputDirs(outputData)
    self.loadSources(outputData)
    self.loadHeaders(outputData)
    self.loadIncludeDirs(outputData)

  def loadType(self, outputData):
    if not Tags.TYPE in outputData:
      raise KeyError(f"{Tags.TYPE} must be specified in output: {self.name}")

    if outputData[Tags.TYPE] == Tags.EXE:
      self.isExe = True
    elif outputData[Tags.TYPE] == Tags.SHARED_LIB:
      self.isSharedLib = True
    elif outputData[Tags.TYPE] == Tags.STATIC_LIB:
      self.isStaticLib = True
    else:
      raise KeyError(f"Invalid {Tags.TYPE} given to output: {self.name}")

  def loadMainFile(self, outputData):
    if self.isExe and Tags.MAIN_FILE in outputData:
      self.mainFile = outputData[Tags.MAIN_FILE]
  
  def loadOutputDirs(self, outputData):
    if self.isExe and Tags.EXE_OUTPUT_DIR in outputData:
        self.exeOutputDir = outputData[Tags.EXE_OUTPUT_DIR]
    elif Tags.LIB_OUTPUT_DIR in outputData:
      self.libOutputDir = outputData[Tags.LIB_OUTPUT_DIR]

  def loadSources(self, outputData):
    self.sources = FileRetriever.getSourceFiles(outputData)

  def loadHeaders(self, outputData):
    self.headers = FileRetriever.getHeaderFiles(outputData)

  def loadIncludeDirs(self, outputData):
    self.includeDirs = FileRetriever.getIncludeDirs(outputData)