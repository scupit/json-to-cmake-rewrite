# Json to CMakeLists.txt converter
*json-to-cmake* is a CMakeLists.txt file generator which takes a handwritten json file as input. The json file
(called **cmake_data.json**) 

## Goals of the project
1. Providing a concise and easily readable way to detail build data
2. Work over top of CMake, a popular buildsystem generator, so that devs can keep using the same tool
3. Make creating new practice projects much easier, especially for beginners
4. Make linking simpler to visualize

# Usage
As long as your C/C++ project contains a valid cmake_data.json file, this script can be used.
See the [gcmake example project](https://github.com/scupit/gcmake-example-project) for a somewhat complete example
of cmake_data.json in a complex project.

## Prerequisites
* Python 3

## Running
Run `python main.py <projectRoot>`, where projectRoot is the directory containing *cmake_data.json*.
A CMakeLists.txt file will be generated in that same directory if your json file is valid.

If you are currently in your project's root dir, you can also just run `python path/to/main.py`.
No need to specify the root directory in this case since you are already in it.

# cmake_data.json
**cmake_data.json** is the data file where you will specify how your project should be built. More specifically it
tells this script what should be written to CMakeLists.txt. It defines the project's outputs, compiler flags,
imported libraries, links to outputs, language standards, and more.

All file names and directory paths will be relative to the cmake_data.json file.

## Defining an output
**Tag:** `"output": {...}`.

Outputs include executables, static libraries, and shared libraries.
Each ouptut item is required to have a defined type and headers and/or sources. However, these can be
inherited in various ways.

Here's an example of the output most common use case:
``` json
{
  "output": {
    "some-output": {
      "type": "executable",
      "mainFile": "main.cpp",
      "rHeaderDirs": [ "include" ],
      "rSourceDirs": [ "src" ],
      "includeDirs": [ "include" ]
    }
  }
}
```

### Name
Output name is determined by the key of the object it's defined in. In the example above, *some-output* is the
name of that executable. When compiled, the executable will be called *some-output*.

### Type
**Tag:** `"type": "..."`

Defines the type of output. Allowed values are:
  * `"executable"`for an executable
  * `"staticLib"` for a static library
  * `"sharedLib"` for a shared library

Type is a required attribute. However, it is not required when the output is defined inside an output group.
More on that later.

### Files
There are several ways to add header and source files.

#### Adding Headers
* `"rHeaderDirs": [...]` recurses through the given directories and gets all header files in each.
* `"headerDirs": [...]` gets all header files in the given directories, but does not recurse through them.
* `"headers": [...]` gets all the given header files.

#### Adding Sources
* `"rSourceDirs": [...]` recurses through the given directories and gets all source files in each.
* `"sourceDirs": [...]` get all source files in the given directories, but does not recurse through them.
* `"sources": [...]` gets all the given source files

#### Main File
If the output is an `executable` type, it can also be given a main file. The main file is just added to sources in
the CMakeLists, but defining it this way helps with clarity.

`"mainFile": "example.cpp"`

### Include Directories
Include directories are similar to system PATH, in that they provide more root directories for the compiler
to look for files. For example, with the project structure:
```
include/
  \-- HeaderFile.hpp
src/
  \-- SourceFile.cpp
cmake_data.json
main.cpp
```
main.cpp would normally have to #include "include/HeaderFile.hpp". But by adding *include* as an "include directory",
now the header can just be included as "HeaderFile.hpp".

* `"rIncludeDirs": [...]` Recurses through the given directories and adds them all to the output's include dirs.
* `"includeDirs": [...]` Adds all the given include directories as include dirs.

# TODO
- [ ] Write a proper README
- [X] Retrieve imported libraries from a specified git link
- [X] Change default C standard to C99
- [X] If a default language standard is specified and no supported language standards were specified, use that as the single supported language standard
- [X] Allow imported libraries to be imported from outside the project tree. **NOTE** that header files must still be in the project tree
- [X] Create an example project in github and link it in this README
- [ ] Add "debuggable" flag for executables to flag whether or not a debugger configuration should be build for them. This config does nothing for CMake, but could be helpful if you create a tool to generate debug configurations for your IDE (or vscode, for example)
- [ ] Add "optional" boolean option for outputs, which determines whether or not the output should be built. Note that this option should be ignore if it is set to 'true' on a library which is a dependency of an execuatable being built.
- [ ] Add "canToggleType" boolean option for output libraries, which can switch whether the library is build as static or shared.
- [ ] Add a checkbox at the bottom which allows you to turn library copy commands off.
- [ ] Use a cmake custom function for copy commands
- [X] Add "outputGroups", which is just output items grouped under a common name. This will make grouping optional outputs much easier, especially when creating several test execuatables. **Each output in the output group should be same type (either executable or library)**

**Ex:**
``` json
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