# Background

When supporting mods for Kerbal Space Program making a release archive is the most boring task. New binaries need to be build, all
files need to be compiled into a specific file structure, and, eventually, it needs to be archived. Not to mention version control
problem: you need to adjust several files and rename the archive.

This script solves the problem! Thru a `.json` file you define the release files, and then just run the script. It will automatically
build new binaries, update version file (e.g. `.version`), and pack the files into properly named archive.

# Running script

## Prerequisites

Before using release script make sure to do the following:

* Update variable `SHELL_ZIP_BINARY` in `make_release.py` script to point to the right archiver.
  - Best candidate for the archiver is 7-Zip which is _open source_ and _free_.
    Download it from the [official site](http://www.7-zip.org/download.html).  If you install it on drive `C:` into a default folder
    then no updates will be needed in the script.
* Update variable `BUILD_SCRIPT` in `make_release.py` script to point to the right batch script that builds your mod's binary in
  a release mode.
   * You may use
    [template_make_binary.cmd](https://github.com/ihsoft/KerbalReleaseBuilder/blob/master/template_make_binary.cmd) as a template.
* Update `.json` settings file.
  * At the very least you have to adjust `PACKAGE_NAME` value.
  * In case of your project doesn't fit definition "standard" you also need to adjust release structure.

## Simple building release structure

Run script in the default mode to have it creating the release folders structure:
```
make_release.py
````

The structure will be created in folder `DEST` relative to the current folder (which is usually the folder where script is located).

## Creating release archive

In order to create release archive provide option `-p`:
```
make_release.py -p
````

Archive will be created in `ARCHIVE_DEST` folder, which by default is a parent of the script's folder. The name of the archive
will consist of `PACKAGE_NAME` and current mod's version grabbed from `AssemblyInfo.cs`.

In case of the archive already exists the release script will fail to not overwrite previous version. If you're confident you want
overwriting then provide option `-o`:

```
make_release.py -p -o
````

# Simple folder structure

Release script can work with almost any setups but if your mod source files are organized in a standard way then you may use template
`.json` file with little or no changes. Here is how usual source structure looks like:

* `\` - project root.
  * `README.md` or `README.txt` files that describe the mod.
  * `LICENSE.md` or `LICENSE.txt` files that describe mod's license.
  * `Binaries` - various third-party libraries needed for the mod (e.g. `MiniAVC`).
  * `PluginData` - mod configs that don't need to be indexed by the game.
  * `Parts` - part definitions.
  * `Patches` - `ModuleManager` configs that update game database.
  * `Source` - C# sources.
  * `Tools` - folder for various tools like a release script.

Given your mod's structure is as above (not all folders/files need to be existing) you may use template
[release_setup.json](https://github.com/ihsoft/KerbalReleaseBuilder/blob/master/release_setup.json) to make a release.
You only need to change release version in your `AssemblyInfo.cs` file and run the script.

Default template will result in the following structure in `<project root>/Release`:

* `GameData`
  * `<package name>`
    * `README.md` and/or `README.txt` if there were ones in the project's root.
    * `LICENSE.md` and/or `LICENSE.txt` if there were ones in the project's root.
    * `Parts` - will only exist if there are actual folders and files inside.
    * `Patches` - will only exist if there are actual folders and files inside.
    * `Plugins` - will have all `DLL`, `TXT`, and `MD` files located in `Source/Binaries`.
      * `<package name>.dll` - main mod's DLL.
      * `<package name>.version` - this file will be updated with the proper version information.
        * `PluginData` - will have all files and sub-folders from the source. Won't be created if no real content found.

# Settings .json

By default script searches for file `release_setup.json`. Once it's found all the setup data is loaded from it. This file is nothing
more but just a definition of values for the
[`KspReleaseBuilder.Builder`](https://github.com/ihsoft/KerbalReleaseBuilder/blob/master/KspReleaseBuilder.py) class instance.
To get more information about each setting read the docs in the source file. Below are described the most important settings.

| Key | Description |
|-----|-------------|
| `PACKAGE_NAME` | It's a base name for anything: release folder, archive name, version file, etc. E.g. if you set it to "ABC" then resulted archive name will look like `ABC_v1.2.3.zip`. |
| `SRC` | Base folder for the "source" patterns (see `STRUCTURE`). Normally it's a project's root. If release script lives in `/Tools` then relative path to the project's root is `..`. |
| `DEST` | A path to the folder where release structure will be built (see `STRUCTURE`). |
| `STRUCTURE` | TBD |

## Source patterns

TBD

## Pattern modifiers

TBD

## Macros in source patterns

When defining a value for `STRUCTURE` a macro substitution can be used. "Macro" is a name of `KspReleaseBuilder.Builder` field which is
enclosed in `###`. Macro must be the only value of the field, i.e. it cannot be a part of equation:
```
    "Plugins" : [
      "###SRC_COMPILED_BINARY###"
    ]
```

Note that some values get initialized to the default values during JSON file loading. E.g. `SRC_COMPILED_BINARY` get the value once
`PACKAGE_NAME` is loaded. See more details in `KspReleaseBuilder.Builder.LoadSettingsFromJson` method implementation.
