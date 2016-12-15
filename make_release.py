# Public domain license.
# Author: igor.zavoychinskiy@gmail.com
# Version: 0.1

# Template runner for the builder script.

import collections
import getopt
import sys

import KspReleaseBuilder

SHELL_ZIP_BINARY = 'L:/Program Files/7-Zip/7z.exe'
MOD_NAME = 'EasyVesselSwitch'
BUILD_SCRIPT = 'make_binary.cmd'

def main(argv):
  try:
    opts, _ = getopt.getopt(argv[1:], 'po', )
  except getopt.GetoptError:
    print 'make_release.py [-po]'
    exit(2)
  opts = dict(opts)
  need_package = '-p' in opts
  overwrite_existing  = '-o' in opts


  builder = KspReleaseBuilder.Builder(
      MOD_NAME, BUILD_SCRIPT, SHELL_ZIP_BINARY)
  builder.SetupDefaultLayout()

  builder.SRC = '..'
#  builder.SRC_VERSIONS_FILE = '/Source/Properties/AssemblyInfo.cs'
#  builder.SRC_COMPILED_BINARY = '/Source/bin/Release/' + MOD_NAME + '.dll'
#  builder.SRC_REPOSITORY_VERSION_FILE = '/EasyVesselSwitch.version'
#  builder.DEST = '../Release'
#  builder.ARCHIVE_DEST = '..'
#  builder.STRUCTURE['Patches'] = [
#      '?/Patches/*',
#  ]
  builder.STRUCTURE['/CCK'] = [
      '/LICENSE.md',
      '/README.md',
  ]
  builder.STRUCTURE[''] = [
      '/LICENSE.md',
      '/README.md',
  ]
  builder.STRUCTURE['Plugins'] = [
      builder.SRC_COMPILED_BINARY,
      builder.SRC_REPOSITORY_VERSION_FILE,
      '/Binaries/KSPDev_Utils*.dll',
      '/Binaries/KSPDev_Utils_License.md',
      '/Binaries/MiniAVC.dll',
  ]
  builder.STRUCTURE['Plugins/PluginData'] = [
      '/PluginData/*',
  ]

  # Make the releasse!
  builder.MakeRelease(need_package, overwrite_existing)


main(sys.argv)
