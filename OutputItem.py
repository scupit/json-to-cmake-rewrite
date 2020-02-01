import Tags

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

  def loadType(self, outputData):
    if not Tags.TYPE in outputData:
      raise KeyError(f"{Tags.TYPE} must be specified in output: {self.name}")

    if outputData[Tags.TYPE] = Tags.EXE:
      self.isExe = True
    elif outputData[Tags.TYPE] = Tags.SHARED_LIB:
      self.isSharedLib = True
    elif outputData[Tags.TYPE] = Tags.STATIC_LIB:
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
    


