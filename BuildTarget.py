import Logger
import Tags

class BuildTarget:
  name = ""
  cFlags = [ ]
  cppFlags = [ ]

  def __init__(self, name, buildTargetData):
    self.name = name

    self.loadCFlags(buildTargetData)
    self.loadCppFlags(buildTargetData)

  # TODO: Ensure cFlags is actually a list of compiler flags
  def loadCFlags(self, buildTargetData):
    if Tags.C_FLAGS in buildTargetData:
      self.cFlags = buildTargetData[Tags.C_FLAGS]

  # TODO: Ensure cppFlags is actually a list of compiler flags
  def loadCppFlags(self, buildTargetData):
    if Tags.CPP_FLAGS in buildTargetData:
      self.cppFlags = buildTargetData[Tags.CPP_FLAGS]