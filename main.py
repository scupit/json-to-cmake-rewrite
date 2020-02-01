import Extensions
import FileHelper

testDirname = "testing-sfml/dep"
# testDirname = "testing-sfml/include"

print(FileHelper.getFilesByExtension(testDirname, Extensions.headers, False))