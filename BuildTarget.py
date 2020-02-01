import Logger
import Tags

class BuildTarget:
  name = ""
  compilerFlags = [ ]

  def __init__(self, name, buildTargetData):
    self.name = name
    self.loadCompilerFlags(buildTargetData)

  # UTILS

  def hasCompilerFlags(self):
    return len(self.compilerFlags) > 0

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
