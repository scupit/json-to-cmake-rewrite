import subprocess
from pathlib import Path

from FileHelper import getAbsolutePath, createDirPath, isDirectory
import Globals

def removeGitExtension(gitRepo: str) -> str:
  gitExtensionIndex = gitRepo.rfind('.git')
  return gitRepo if gitExtensionIndex == -1 else gitRepo[0:gitExtensionIndex]

def getRepoName(gitRepo: str) -> str:
  lastDirSeparator = gitRepo.rfind('/')
  return removeGitExtension(gitRepo if lastDirSeparator == -1 else gitRepo[lastDirSeparator + 1:])

def cloneRepoIfNonexistent(gitRepo: str, importedLibName: str = ""):
  # Create the imported repo git directory
  # Create the imported repo builds directory
  createDirPath(f"{Globals.EXTERNAL_GIT_REPO_DIR}/{Globals.EXTERNAL_BUILD_REPO_DIR}/{importedLibName}")

  # Normally this isn't necessary because the repo knows its own name, and when cloning into the
  # current directory the name is set for you. However we are cloning from an external directory
  # but still want the repo to keep its same name, and only clone if the repo is not already
  # there. Getting the repo name manually makes these checks consistent.
  repoPath = f"{Globals.EXTERNAL_GIT_REPO_DIR}/{getRepoName(gitRepo)}"

  if not isDirectory(repoPath):
    createDirPath(repoPath)
    print(f"Cloning {getRepoName(gitRepo)}\n")
    subprocess.run(["git", "clone", gitRepo, getAbsolutePath(repoPath)])