import FileRetriever
import FileHelper
import Globals
import Logger
import Tags

class ImportedLibrary:

  def __init__(self, name, importedLibData):
    self.name = name

    self.headers = [ ]
    self.includeDirs = [ ]

    self.generatedDepDirname = self.name

    self.gitRepoToClone = None
    # Clone imported repos by default
    self.shouldCloneRepo = True
    self.downloadLink = None

    self.dirContainingLibraryFiles = ""
    self.libraryFiles = [ ]

    # Assume the imported library is contained in the project tree by default
    self.isOutsideProjectTree = False

    self.loadHeaders(importedLibData)
    self.loadIncludeDirs(importedLibData)
    self.loadRootDir(importedLibData)
    self.loadLibraryFiles(importedLibData)
    self.loadGitRepoToClone(importedLibData)
    self.loadDownloadLink(importedLibData)
    self.loadGeneratedDirname(importedLibData)

  # UTILS
  def hasHeaders(self):
    return len(self.headers) > 0

  def hasIncludeDirs(self):
    return len(self.includeDirs) > 0

  def isExternalWithRoot(self) -> bool:
    return self.isOutsideProjectTree and not self.dirContainingLibraryFiles == ""

  # LOAD FUNCTIONS
  def loadHeaders(self, importedLibData):
    self.headers = FileRetriever.getHeaderFiles(importedLibData)

  def loadIncludeDirs(self, importedLibData):
    self.includeDirs = FileRetriever.getIncludeDirs(importedLibData)

  def loadRootDir(self, importedLibData):
    # Must be called before loading root dir, otherwise the root dir will not be resolved properly
    self.loadIsOutsideProjectTree(importedLibData)

    if Tags.IMPORT_ROOT_DIR in importedLibData:
      if self.isOutsideProjectTree:
        self.dirContainingLibraryFiles = FileHelper.getAbsoluteExternalPath(importedLibData[Tags.IMPORT_ROOT_DIR])
      else:
        self.dirContainingLibraryFiles = FileHelper.normalizePath(importedLibData[Tags.IMPORT_ROOT_DIR])
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
  
  def loadGitRepoToClone(self, importedLibData):
    if Tags.IMPORT_GIT_REPO in importedLibData:
      self.gitRepoToClone = importedLibData[Tags.IMPORT_GIT_REPO]

    if Tags.IMPORT_SHOULD_CLONE_REPO in importedLibData:
      self.shouldCloneRepo = importedLibData[Tags.IMPORT_SHOULD_CLONE_REPO]

  def loadDownloadLink(self, importedLibData):
    if Tags.IMPORT_DOWNLOAD_LINK in importedLibData:
      self.downloadLink = importedLibData[Tags.IMPORT_GIT_REPO]

  # Called before loading root dir
  def loadIsOutsideProjectTree(self, importedLibData):
    if Tags.IMPORT_IS_OUTSIDE_PROJECT in importedLibData:
      self.isOutsideProjectTree = importedLibData[Tags.IMPORT_IS_OUTSIDE_PROJECT]

  def loadGeneratedDirname(self, importedLibData):
    if Tags.IMPORT_GENERATED_DIRNAME in importedLibData:
      self.generatedDepDirname = importedLibData[Tags.IMPORT_GENERATED_DIRNAME]