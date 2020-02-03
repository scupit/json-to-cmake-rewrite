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

- [ ] Distribute CMakeLists.txt files throughout the project tree per good practice
- [ ] Condense file and directory names where possible (use my file tree)

**Ex:** if I have a bunch of header files like this:
* ${PROJECT_SOURCE_DIR}/dep/include/SFML/Something.hpp
* ${PROJECT_SOURCE_DIR}/dep/include/SFML/Something_Else.hpp
* ${PROJECT_SOURCE_DIR}/dep/include/SFML/Something_Or_Another.hpp
* ${PROJECT_SOURCE_DIR}/dep/include/SFML/Another_File.hpp

Then they should be condensed with a variable:
`set( SFML_HEADER_ROOT ${PROJECT_SOURCE_DIR}/dep/include/SFML )`

And then the file list should look like this instead:
* ${SFML_HEADER_ROOT}/Something.hpp
* ${SFML_HEADER_ROOT}/Something_Else.hpp
* ${SFML_HEADER_ROOT}/Something_Or_Another.hpp
* ${SFML_HEADER_ROOT}/Another_File.hpp