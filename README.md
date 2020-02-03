# Json to CMakeLists.txt converter
This project aims to make creating CMake project much easier by generating the CMakeLists.txt file
in your project directory. What is generated in the file depends on the contents of the *cmake_data.json*
file you write.

## Why this is useful
* The json file is much more concise, so you write less
* When files are specified by directory, running this script adds new files to the CMakeLists.txt automatically
* Makes generating new projects much nicer and quicker

# Usage
* **NOTE:** Requires python 3
Run `python main.py <projectRoot>`, where projectRoot is the directory containing *cmake_data.json*.
A CMakeLists.txt file will be generated in that same directory if your json file is valid.

If you are currently in your project's root dir, you can also just run `python path/to/main.py`.
No need to specify the root directory in this case since you are already in it.
* It is recommended to wrap the python call in a batch or shell script for easy access. I call mine **gcmake** for "gen cmake"

# cmake_data.json

## What is it?
*cmake_data.json* is the file in which you specify data for your project, including its outputs, build
targets (such as *Debug* and *Release* builds), which files should be compiled into the outputs, etc.

## Options:
**TODO**

# TODO
- [ ] Write a proper README
- [ ] Create an example project in github and link it in this README
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

- [ ] Change default C standard to C99
- [ ] If a default language standard is specified and no supported language standards were specified, use that as the single supported language standard
- [ ] Add attributes *cStandard* and *cppStandard* for the above purpose. They will act exactly the same as the default language standard attributes, and will only be available for clarity reasons