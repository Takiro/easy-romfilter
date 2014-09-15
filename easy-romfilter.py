import re
import argparse
from shutil import copy2
from os import listdir, makedirs
from os.path import join, isdir, isfile


class RomFilter:

    version = '1.1.0-beta'

    def __init__(self, args):
        self.rom_folder_path = args.rom_folder_path
        self.output_directory = args.output_directory
        self.verbosity = args.v
        self.simulate = args.simulate
        self.extension = args.extension
        self.ignorePrefix = args.ignore_super
        self.create_subfolder = args.create_subfolder

        self.fatal = -1
        self.warn = 0
        self.info = 1
        self.debug = 2
        self.trace = 3

        # check for user defined region string
        if args.regions:
            self.region = {}
            rtags = args.regions.upper().split(',')
            l = len(rtags)

            for k, v in enumerate(rtags):
                # create score for each region
                # we assume that regions are ordered descending by priority
                self.region[v] = float(l - k)
        else:
            # default
            self.region = {'U': 4.0, 'UK': 3.0, 'E': 2.0, 'J': 1.0}

        # matches:
     #   1   name                         (.*)
     #   2   language flag                   (([G|E|U|J])\)
     #   3   optional: multi language with language count (\(M[0-9]\))?
     #   4   optional: version info             (\(V([0-9]\.[0-9])\))?
     #   5      version number X.X             ([0-9]\.[0-9])
     #   6   optional: verified good dump       (\[!\])?
        pattern = r'(.*)\(([A-Z]{1,2})\).?(\(M[0-9]\))?.?(\(V([0-9]\.[0-9])\))?.?(\[!\])?\.'
        pattern += self.extension

        self.regex = re.compile(pattern)

    def _output(self, string, level=0):
        if (level <= self.verbosity):
            print(string)
        return

    def _rateFile(self, file_name):

        match = self.regex.match(file_name)

        if match:

            # check language
            if match.group(2):                   # was there a match
                # and is the region in our dict
                if match.group(2) in self.region:
                    x = self.region[match.group(2)]
                else:
                    return -1.0  # no match
            else:
                x = 0.0  # XXX this still allows roms without language flag
                                # maybe a strict flag would come in handy

            # check for good dump
            if match.group(6):
                x += 0.9
            else:
                x += 0.5

            # check version
            if match.group(5):
                x += float(match.group(5)) / 100.0

            return x
        else:
            return -1.0

    def copyRomFiles(self, path):
        self._output("Checking path " + path, self.debug)
        files = listdir(path)

        self._output("Path contains:", self.trace)
        self._output(files, self.trace)

        most_rated = ''
        rating = -1

        for f in files:

            rom = join(path, f)
            if isdir(rom):
                self._output('Path ' + rom + ' is a directory', self.debug)
                self.copyRomFiles(rom)
            else:
                if isfile(rom):

                    self._output(rom + 'is a file', self.debug)
                    r = self._rateFile(f)
                    self._output(f + ' rated ' + str(r), self.debug)

                    if rating < r:
                        self._output('replacing ' + most_rated +
                                     ' with ' + f, self.debug)
                        most_rated = f
                        rating = r
                else:
                    self._output(
                        'Could not determine file type of ' + f, self.warn)

        if most_rated != '':

            stripedname = most_rated.lower()

            # Remove the first Super that lots of Super Nintendo
            # games have in their name
            # So "Super Game Name" is sorted into g/ga/gam/
            # instead of /s/su/sup
            # with lots of other games stating with 'Super '
            if self.ignorePrefix:
                stripedname = re.sub('super ', '', stripedname, 1)

            stripedname = re.sub('[^A-Za-z]+', '', stripedname)

            # copy most rated into new folder
            targetDir = join(self.output_directory, stripedname[:1],
                             stripedname[:2], stripedname[:3])
            if self.create_subfolder:
                res = self.regex.match(most_rated)
                targetDir = join(targetDir,  res.group(1))

            if not isdir(targetDir):
                self._output('Creating non existing directory ' +
                             targetDir, self.info)

                if not self.simulate:
                    makedirs(targetDir, mode=0o775)

            src = join(path, most_rated)
            self._output('Copying ' + most_rated + ' from ' + src +
                         ' to ' + targetDir, self.info)

            if not self.simulate:
                copy2(src, targetDir)
        else:
            # XXX this could rise a lot of warnings if regions are very
            # restrictive. maybe a suppress-warnings or a quiet flag is a good
            # idea
            self._output('Found no rom in ' + path +
                         'that matches any pattern. Nothing copied.',
                         self.warn)
        return
    # end copyRomFiles
# end class


def show_help():
    parser = argparse.ArgumentParser(
        description='Filter game roms in a directory and copy files into new one.')
    parser.add_argument('rom_folder_path', help='Directory to the rom folders')
    parser.add_argument('output_directory',
                        help='Directory where to copy filtered files.')
    parser.add_argument('-v', action='count', default=0,
                        help='Increase verbosity level')
    parser.add_argument('-s', '--simulate', action='store_true', default=False,
                        help="Only output what would happen but do not actually copy files or create directories.")
    parser.add_argument('-e', '--extension', metavar="file_extension",
                        required=True,
                        help="File extension of rom files. Like z64 or smc")
    parser.add_argument('-r', '--regions', metavar="region_tags",
                        help="Comma separated list of regions or language ordered by priority. Dfault is U,UK,E,J")
    parser.add_argument('--version', action='version',
                        version=RomFilter.version)
    parser.add_argument('--ignore-super', action='store_true', default=False,
                        help='If set the Super prefix lots of SNES games have in their name will be ignored.')
    parser.add_argument('--create-subfolder', action='store_true', default=False,
                        help='Creates a sub-folder for every Game. Useful for keeping rom and save files together.')
    args = parser.parse_args()
    return args
# end help


def main():

    args = show_help()

    if args:
        rom_path = args.rom_folder_path
        rf = RomFilter(args)
        rf.copyRomFiles(rom_path)

    return 0
# end main

if __name__ == "__main__":
    main()
