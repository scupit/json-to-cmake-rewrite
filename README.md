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
- [X] Retrieve imported libraries from a specified git link
- [X] Change default C standard to C99
- [X] If a default language standard is specified and no supported language standards were specified, use that as the single supported language standard
- [X] Allow imported libraries to be imported from outside the project tree. **NOTE** that header files must still be in the project tree
- [ ] Create an example project in github and link it in this README
- [ ] Add "debuggable" flag for executables to flag whether or not a debugger configuration should be build for them. This config does nothing for CMake, but could be helpful if you create a tool to generate debug configurations for your IDE (or vscode, for example)
- [ ] Add "optional" boolean option for outputs, which determines whether or not the output should be built. Note that this option should be ignore if it is set to 'true' on a library which is a dependency of an execuatable being built.
- [ ] Add "canToggleType" boolean option for output libraries, which can switch whether the library is build as static or shared.
- [ ] Add a checkbox at the bottom which allows you to turn library copy commands off.
- [X] Add "outputGroups", which is just output items grouped under a common name. This will make grouping optional outputs much easier, especially when creating several test execuatables. **Each output in the output group should be same type (either executable or library)**

**Ex:**
```json
{
  "outputGroups": {
    "tests": {
      "outputs": {
        "test_1": { "define-output-1": "..." },
        "test_2": { "define-output-2": "..." }
      },
      "optional": true
    }
  }
}
```

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