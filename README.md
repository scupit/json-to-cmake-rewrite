# Json to CMakeLists.txt converter

# TODO
- [ ] Write a proper README
- [ ] Allow imported libraries to be imported from outside the project tree
- [ ] Retrieve imported libraries from a specified git link into a given directory
- [ ] Allow file names to be specified using a json object.

**Ex:** 
```json
{
  "filePathVariable": [
    "first/path",
    {
      "second": {
        "path": [
          "file_1",
          "file_2",
          "file_3"
        ]
      }
    }
  ]
}
```