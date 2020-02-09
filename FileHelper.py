from glob import iglob
import os
from pathlib import Path
import sys

rootPathObject = Path(os.getcwd()) if len(sys.argv) < 2 else Path(sys.argv[1]).resolve()

def combineExtensions(extensions: list) -> str:
  output = ""
  for i in range(0, len(extensions)):
    output += extensions[i]
    if i != len(extensions) - 1:
      output += '|'
  return output

def createDirPath(dirPath: str):
  dirs = Path(dirPath).as_posix().split('/')

  # Copy the root path object
  currentPath = Path(str(rootPathObject))

  for dirName in dirs:
    currentPath /= dirName
    if not currentPath.exists() or not currentPath.is_dir():
      currentPath.mkdir()

def getAbsolutePath(filePath: str) -> str:
  return str((rootPathObject / filePath).resolve())

def getAbsoluteExternalPath(filePath: str) -> str:
  return Path(filePath).resolve().as_posix()

def getDirRetrievalRegex(dirToSearch):
  return str(rootPathObject / dirToSearch / "**")

def getProjectName() -> str:
  pathString = str(rootPathObject)
  return pathString[pathString.rfind(os.path.sep) + 1:]

def getSearchRegex(dirToSearch, extension, isRecursive):
  return str(rootPathObject / dirToSearch / f"{'**/' if isRecursive else ''}*.{extension}")

def getRelativePath(filePath: str) -> str:
  return Path(filePath[len(str(rootPathObject)) + 1:]).as_posix()

def getFilesByExtension(dirToSearch, extensions, doRecursively):
  files = [ ]
  for extension in extensions:
    for fileName in iglob(getSearchRegex(dirToSearch, extension, doRecursively), recursive=doRecursively):
      files.append(getRelativePath(fileName))
  
  return files

def getDirectories(fromDir, doRecursively):
  dirs = [ ]
  for dirName in iglob(getDirRetrievalRegex(fromDir), recursive=doRecursively):
    if os.path.isdir(dirName):
      dirs.append(getRelativePath(dirName))
  return dirs

def normalizePath(filePath: str) -> str:
  return getRelativePath(getAbsolutePath(filePath))

def isDirectory(dirPath: str) -> bool:
  thePath = Path(getAbsolutePath(dirPath))
  return thePath.exists() and thePath.is_dir()