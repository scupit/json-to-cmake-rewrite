# String Utils
def inBraces(variableName: str) -> str:
  return "${" + variableName + "}"

def inQuotes(text: str) -> str:
  return '"' + test + '"'

def mangleLibName(libName: str, index: int) -> str:
  return libName + '_' + index

# Variable functions
def includeDirsVariable(variableName: str) -> str:
  return variableName + "_INCLUDE_DIRS"

def headersVariable(variableName: str) -> str:
  return variableName + "_HEADERS"

def sourcesVariable(variableName: str) -> str:
  return variableName + "_SOURCES"

# Preset Strings
projectSourceDir = inBraces("PROJECT_SOURCE_DIR")
cmakeBinaryDir = inBraces("CMAKE_BINARY_DIR")
cmakeBuildType = inBraces("CMAKE_BUILD_TYPE")

emptyQuotes = '""'

# Misc functions
def getOutputDir(dirname: str) -> str:
  return f"{cmakeBinaryDir}/{dirname}/{cmakeBuildType}"