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
* Git (if imported libraries clone repos)

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

## Defining general project data
This section is for optional project data, such as C/C++ language standards, and project name.

### Project name (optional)
**Tag:** `"projectName": "string"`
This is **optional**. If project name is omitted, the name of the project root directory is used in the CMakeLists.

### C Language standard (optional)
Only *std* standards are supported. No C extensions are allowed. This sets the standard for the entire project.

`"defaultCStandard": "string"` sets the project's default C standard. If unchanged in CMake cache (easier to see in CMake
gui), this is the standard which will be used to compile.  
`"supportedCStandards": [strings]` sets a list of standards allowed in the project. This will be selectable in a dropdown
in the CMake GUI.

**Both are optional**. If only a default standard is specified, that will be used as the project standard. If only an
array of supported standards is supplied, then the first standard in the array will be used as the default. If both
are specified, the default standard must exist in the list of supported standards.

### C++ Language standard (optional)
Same as C, no language extensions are allowed. Only *std* standards are supported. This sets the standard for the
entire project.

`"defaultCppStandard": "string"` sets the project's default C++ standard. Same rules as C apply.
`"supportedCppStandards": [strings]` sets a list of standards allowed in the project. This will be selectable in
a dropdown in the CMake GUI.

**Both are optional**. If only a default standard is specified, that will be used as the project standard. If only an
array of supported standards is supplied, then the first standard in the array will be used as the default. If both
are specified, the default standard must exist in the list of supported standards.

## Defining an output
**Tag:** `"output": {objects}`.

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
**Tag:** `"type": "string"`

Defines the type of output. Allowed values are:
  * `"executable"`for an executable
  * `"staticLib"` for a static library
  * `"sharedLib"` for a shared library

Type is a required attribute. However, it is not required when the output is defined inside an output group.
More on that later.

### Files
There are several ways to add header and source files.

#### Adding Headers
* `"rHeaderDirs": [strings]` recurses through the given directories and gets all header files in each.
* `"headerDirs": [strings]` gets all header files in the given directories, but does not recurse through them.
* `"headers": [strings]` gets all the given header files.

#### Adding Sources
* `"rSourceDirs": [strings]` recurses through the given directories and gets all source files in each.
* `"sourceDirs": [strings]` get all source files in the given directories, but does not recurse through them.
* `"sources": [strings]` gets all the given source files

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

* `"rIncludeDirs": [strings]` Recurses through the given directories and adds them all to the output's include dirs.
* `"includeDirs": [strings]` Adds all the given include directories as include dirs.

## Defining a group of outputs
**Tag:** `"outputGroups": {ouptut objects}`
Outputs can also be defined in a group. Defining Here is what this might look like:

``` json
{
  "outputGroups": {
    "first-group": {
      "type": "executable",
      "rHeaderDirs": [ "include" ],
      "rSourceDirs": [ "src" ],
      "includeDirs": [ "include" ],
      "outputs": {
        "an-output": {
          "mainFile": "a-main.cpp"
        },
        "other-output": {
          "mainFile": "other-files/other-main.cpp",
          "headerDirs": [ "other-files/include" ],
          "sourceDirs": [ "other-files/src" ]
        }
      }
    }
  }
}
```

There are a few advantages to defining outputs in a group.
1. All files and include dirs given to the group propagate to each of the group's outputs.
2. Linking to/from groups will involve every file in the group. More on that later.

#### Name
As when defining an output, an output group's name is the key of the object it's defined in. In the example above,
*"first-group"* is the name of the output group.

### Type
**Tag:** `"type": "string"`
Each group must be given an output type. Available types are the same as individual outputs. See outputs section
for more details and valid types.

There are a few *type* relating things you should keep in mind when creating an output group.
1. All outputs in the group must have the same "function" type as the group. This means that an *executable* group can only contain executables. But a group with type *staticLib* can only contain library outputs, whether static or shared.
2. Each outputs will inherit the group's `type` if the output does not define a type. Therefore **the `type` attribute is not required for ouptuts defined in a group**

### Files
Header and source files are added to groups almost exactly the same way they are added to individual outputs (see
*defining outputs* section for details). The only difference is that a `mainFile` cannot be given to a group. Also,
every file added to the group will be propagated to each of the group's outputs

### Include Dirs
Include dirs are added to the group exactly the same way they are added to outputs. These propagate to all the group's
outputs as well.

### Outputs
**Tag:** `"outputs": {output objects}`
Outputs in a group are defined the same as individual outputs. However, `type` is no longer required. When no type is
defined for the output, it inherits the same type as its containing group. Also, any files and include dirs given to
the group will automatically be added to the output. *No need to define them for each output in that case*.

## Imported Libraries
**Tag:** `"importedLibs": {imported library objects}`
Libraries can be imported into the project as well. Imported libraries are libraries which are already built. They should
be linked to output libraries/executables. See how that is done in the **Linking** section.

Imported libraries in this script should be thought of as "packages". Each one contains one or more library files to
link, but when linking the name of the library "package" is used. More on that later.

Here's an example of an imported library:

``` json
{
  "importedLibs": {
    "matrix-library": {
        "gitRepo": "https://github.com/scupit/basic-matrices.git",
        "cloneRepo": true,
        "includeDirs": [ "dep/include" ],
        "rHeaderDirs": [ "dep/include" ],
        "rootDir": "dep/lib/matrices",
        "libFiles": [ "matrices" ]
    }
  }
}
```

### Name
The name of an imported library, same as outputs, is the key of the object it's defined in. In the example above,
the imported library "package" name is *"matrix-library"*.

### Files and Include Dirs
Header files and include directories are given to imported libraries exactly the same way they are given to outputs.
See **Defining an Output** for details.
**Note** that all the imported library's headers and include dirs will propagate to any output item/group it links to.

### Set the import root directory
**Tag:** `"rootDir": "string"`
You must specify the directory which contains each of the library files. It is recommended for this to be
*inside the project tree*, however it can also be outside the project tree.

**Tag:** `"outsideProjectTree": boolean`
In the case that the rootDir is
outside the project tree, you must set `"outsideProjectTree"` to `true` in the importedLib. Otherwise it is
assumed to be in the project tree.

### Imported Library Files
**Tag:** `"libFiles": [strings]`
This is the list of library files to import. All you need to specify is the name of each library, no prefix or suffix.
CMake will automatically resolve the library and whether it is static or shared. For example, if adding
*libmatrices.a*, use **"matrices"** as the libFile.

Each of these library files will be linked to every output and/or group this "imported library package" is linked to.

### Git repos
**Tag:** `"gitRepo": "string"`
Imported libraries can also be cloned from git repos!
To specify a git repo for the imported library, set its `"gitRepo"` to the remote repo URL. When running this script,
the repo will be cloned into **dep/*libraryName*>** where *libraryName* is the name of the imported library "package".
If the repo already exists in that location, no cloning occurs. 

Repos are cloned into **external/*repoName***. The directory **external/_builds** will also be there to hold local
builds.

#### Optional Cloning
**Tag:** `"cloneRepo": boolean`
Repos are cloned by default, however you can turn off cloning completely per imported lib by setting its `"cloneRepo"`
to `false`. Setting it to `true` will cause the repo to be cloned. That is the default behavior, but it also helps
readability.

### Generated "dep" directory
**Tag:** `"generatedDepDir": "string"`
When running this script, the directories **dep/include/*libGenName*** and **dep/lib/*libGenName*** 
will be generated for each imported library. *libGenName* this case is the name of the library by default,
however the `"generatedDepDir"` attribute can optionally be specified to overwrite this.

### Download Link
**Tag:** `"downloadLink": "string"`
The download link attribute is not required and does nothing in the actual script. However, it is useful for reference
if anyone reading cmake_data.json needs to build or download the library ahead of time. It's mainly just for saving time
and a place to store a link to the library is applicable.

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