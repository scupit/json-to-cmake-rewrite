import FileRetriever
import FileHelper
import Logger
import Tags

class ImportedLibrary:
  name = ""

  headers = [ ]
  includeDirs = [ ]

  dirContainingLibraryFiles = ""
  libraryFiles = [ ]

  def __init__(self, name, importedLibData):
    self.name = name

    self.loadHeaders(importedLibData)
    self.loadIncludeDirs(importedLibData)
    self.loadRootDir(importedLibData)
    self.loadLibraryFiles(importedLibData)

  # UTILS
  def hasHeaders(self):
    return len(self.headers) > 0

  def hasIncludeDirs(self):
    return len(self.includeDirs) > 0

  # LOAD FUNCTIONS
  def loadHeaders(self, importedLibData):
    self.headers = FileRetriever.getHeaderFiles(importedLibData)

  def loadIncludeDirs(self, importedLibData):
    self.includeDirs = FileRetriever.getIncludeDirs(importedLibData)

  def loadRootDir(self, importedLibData):
    if Tags.IMPORT_ROOT_DIR in importedLibData:
      self.dirContainingLibraryFiles = importedLibData[Tags.IMPORT_ROOT_DIR]
    else:
      Logger.logIssueThenQuit(f"Must specify {Tags.IMPORT_ROOT_DIR} in imported lib: {self.name}")

  def loadLibraryFiles(self, importedLibData):
    if Tags.IMPORTED_LIB_FILES in importedLibData:
      # At least one library file must be defined, otherwise there is an issue
      if len(importedLibData[Tags.IMPORTED_LIB_FILES]) > 0:
        for libFileName in importedLibData[Tags.IMPORTED_LIB_FILES]:
          self.libraryFiles.append(FileHelper.normalizePath(libFileName))
      else:
        Logger.logIssueThenQuit(f"Must specify at least one {Tags.IMPORTED_LIB_FILES} for imported lib: {self.name}")
    else:
      Logger.logIssueThenQuit(f"{Tags.IMPORTED_LIB_FILES} are required for imported lib {Tags.IMPORTED_LIB_FILES}")