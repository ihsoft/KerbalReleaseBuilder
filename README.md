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
* Update `release_setup.json` file.
  * At the very least you have to adjust `PACKAGE_NAME` value.
  * In case of your project doesn't fit definition "standard" you also need to adjust release structure.

## Simple building release structure

Run script in the default mode to have it creating the release folders structure:
```
make_release.py
````

The structure will be created in folder `DEST` relative to the current folder (which is usually the folder where the script is located).

## Creating release archive

In order to create a release archive provide option `-p`:
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

Release script can work with almost any setup but if your mod source files are organized in a standard way then you may use template
`.json` file with little or no changes. Here is how usual source structure looks like:

* `\` - project root.
  * _Optional_. `README.md` or `README.txt` files that describe the mod.
  * _Optional_. `LICENSE.md` or `LICENSE.txt` files that describe mod's license.
  * _Optional_. `Binaries` - various third-party libraries needed for the mod (e.g. `MiniAVC`).
  * _Optional_. `PluginData` - mod configs that don't need to be indexed by the game.
  * _Optional_. `Parts` - part definitions.
  * _Optional_. `Patches` - `ModuleManager` configs that update game database.
  * _Required_. `Source` - C# sources.
  * _Optional_. `Tools` - folder for various tools like a release script.

Given your mod's structure is as above (not all folders/files need to be existing) you may use template
[release_setup.json](https://github.com/ihsoft/KerbalReleaseBuilder/blob/master/release_setup.json) to make a release.
You only need to change release version in your `AssemblyInfo.cs` file and run the script.

Default template will result in the following structure in `<project root>/Release`:

* `GameData`
  * `{PACKAGE_NAME}`
    * `README.md` and/or `README.txt` if there were ones in the project's root.
    * `LICENSE.md` and/or `LICENSE.txt` if there were ones in the project's root.
    * `Parts` - will only exist if there are actual folders and files inside.
    * `Patches` - will only exist if there are actual folders and files inside.
    * `Plugins` - will have all `DLL`, `TXT`, and `MD` files located in `Source/Binaries`.
      * `{PACKAGE_NAME}.dll` - main mod's DLL.
      * `{PACKAGE_NAME}.version` - this file will be updated with the proper version information.
        * `PluginData` - will have all files and sub-folders from the source. Won't be created if no real content found.

Note that `{PACKAGE_NAME}.version` file will also be updated in the source so what you could commit it back to Guthub.
        

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
| `ARCHIVE_DEST` | A path to the folder where release archive will be stored. |
| `STRUCTURE` | It's a dictionary where _key_ defines destination and _value_ defines a list of source patterns. Destination is relative to `{DEST}/GameData` if key starts with `/` and relative to `{DEST}/GameData/{PACKAGE_NAME}` otheriwse. Source pattern is relative to `SRC` and by the syntax requirement must always start with either `/` or a pattern modifier (see below). When source patterns match nothing the destination folder is not created. |

## Patterns

Pattern is a usual [Unix pathname pattern](http://pubs.opengroup.org/onlinepubs/000095399/utilities/xcu_chap02.html#tag_02_13)
which allows matching files and folders againts the specified condition(s). In the simplest case pattern is just a path to the file or directory which matches exactly one entry.

If pattern matched a directory then the entire directory tree will be copied. E.g. pattern `/test/folder` will copy directory
`{SRC}/test/folder` and all its subfolders into `{DEST}/{KEY}/folder`. A little change to this pattern will result in completely
different behavior: for pattern `/test/folder/*` all files and directories from `{SRC}/test/folder` will be copied into `{DEST}/{KEY}`.

## Pattern modifiers

`KerbalReleaseBuilder` supports modifiers that change pattern interpretation. Modifier is a first symbol of the patter:
* `/` means a regular pattern which _must_ return at least one element. E.g. if pattern is `/Source/*.asc` and nothing has matched then
  an error will be thrown.
* `?` means a regular pattern which is _not_ required to match anything. E.g. if pattern is `?/Source/DISCLAIMER.md` and the file is
  not found then script reports it but doesn't abort.
* `-` means it's a cleanup pattern. It will be applied against the _destination_, and everything that is found will be deleted. E.g.
  with destination `{DEST}/Test` and pattern `-Subfolders/*` the following files and folders will be deleted: 
  `{DEST}/Test/Subfolders/*`. Note that `Subfolders` directory will not be dropped in this case.
  
  If cleanup pattern matches a directory then the entire directory with all its content will be deleted. Macros are not expanded
  for the cleanup patterns.

## Macros in patterns

When defining a value for pattern in `STRUCTURE` defintion a macro substitution can be used. "Macro" is a name of
`KspReleaseBuilder.Builder` field which is enclosed in `{}`. There can be any number of macros in the pattern, they will be
handled right before accessing the filesystem. E.g. when version file is stored in a non-standard location the following pattern can
be used:
```
"/My/Custom/Location/{PACKAGE_NAME}.version"
```

Note that some values get initialized to the default values during JSON file loading (see 
`KspReleaseBuilder.Builder.SetupDefaultLayout`). So you may use them thru macros in `STRUCTURE` definition:
```
  "STRUCTURE" : {
    "Plugins" : [
      "{SRC_COMPILED_BINARY}",
      "{SRC_REPOSITORY_VERSION_FILE}",
    ]
  }
```
