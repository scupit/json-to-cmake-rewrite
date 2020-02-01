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

def getAbsolutePath(filePath: str) -> str:
  return str((rootPathObject / filePath).resolve())

def getDirRetrievalRegex(dirToSearch):
  return str(rootPathObject / dirToSearch / "**")

def getProjectName() -> str:
  pathString = str(rootPathObject)
  return pathString[pathString.rfind(os.path.pathsep) + 1:]

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
    dirs.append(getRelativePath(dirName))
  return dirs

def normalizePath(filePath: str) -> str:
  return getRelativePath(getAbsolutePath(filePath))
