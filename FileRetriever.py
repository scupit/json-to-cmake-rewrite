import Extensions
import FileHelper
import Tags

def getSourceFiles(dataItem) -> list:
  sources = [ ]

  if Tags.R_SOURCE_DIRS in dataItem:
    for givenDirectory in dataItem[Tags.R_SOURCE_DIRS]:
      sources += FileHelper.getFilesByExtension(givenDirectory, Extensions.sources, True)

  if Tags.SOURCE_DIRS in dataItem:
    for givenDirectory in dataItem[Tags.SOURCE_DIRS]:
      sources += FileHelper.getFilesByExtension(givenDirectory, Extensions.sources, False)

  if Tags.INDIVIDUAL_SOURCES in dataItem:
    for sourceFile in dataItem[Tags.INDIVIDUAL_SOURCES]:
      sources.append(FileHelper.normalizePath(sourceFile))

  # Remove duplicates
  sources = list(set(sources))
  sources.sort()
  return sources

def getHeaderFiles(dataItem) -> list:
  headers = [ ]

  if Tags.R_HEADER_DIRS in dataItem:
    for givenDirectory in dataItem[Tags.R_HEADER_DIRS]:
      headers += FileHelper.getFilesByExtension(FileHelper.getAbsolutePath(givenDirectory), Extensions.headers, True)

  if Tags.HEADER_DIRS in dataItem:
    for givenDirectory in dataItem[Tags.HEADER_DIRS]:
      headers += FileHelper.getFilesByExtension(FileHelper.getAbsolutePath(givenDirectory), Extensions.headers, False)

  if Tags.INDIVIDUAL_HEADERS in dataItem:
    for headerFile in dataItem[Tags.INDIVIDUAL_HEADERS]:
      headers.append(FileHelper.normalizePath(headerFile))

  # Remove duplicates
  headers = list(set(headers))
  headers.sort()
  return headers

def getIncludeDirs(dataItem):
  includeDirs = [ ]

  if Tags.R_INCLUDE_DIRS in dataItem:
    for givenDirectory in dataItem[Tags.R_INCLUDE_DIRS]:
      includeDirs += FileHelper.getDirectories(FileHelper.getAbsolutePath(givenDirectory), True)

  if Tags.INCLUDE_DIRS in dataItem:
    for givenDirectory in dataItem[Tags.INCLUDE_DIRS]:
      includeDirs.append(FileHelper.normalizePath(givenDirectory))

  # Remove duplicates
  includeDirs = list(set(includeDirs))
  includeDirs.sort()
  return includeDirs