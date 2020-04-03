import Logger
import Tags

class BuildTarget:
  def __init__(self, name, buildTargetData):
    self.name = name

    self.compilerFlags = [ ]
    self.compilerDefinitions = [ ]

    self.loadCompilerFlags(buildTargetData)
    self.loadCompilerDefinitions(buildTargetData)

  # UTILS

  def hasCompilerFlags(self):
    return len(self.compilerFlags) > 0

  def hasCompilerDefinitions(self):
    return len(self.compilerDefinitions) > 0

  # LOAD FUNCTIONS

  # TODO: Ensure cFlags is actually a list of compiler flags
  def loadCompilerFlags(self, buildTargetData):
    if Tags.COMPILER_FLAGS in buildTargetData:
      self.compilerFlags = buildTargetData[Tags.COMPILER_FLAGS]

      # Ensure the dash is present, since it is optional
      for i in range(0, len(self.compilerFlags)):
        self.compilerFlags[i] = self.compilerFlags[i].strip()

        if self.compilerFlags[i][0] != '-':
          self.compilerFlags[i] = '-' + self.compilerFlags[i]

  def loadCompilerDefinitions(self, buildTargetData):
    if Tags.COMPILER_DEFINES in buildTargetData:
      self.compilerDefinitions = buildTargetData[Tags.COMPILER_DEFINES]
