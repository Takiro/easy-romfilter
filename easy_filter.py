import re
import argparse
from shutil import copy2
from os import listdir, makedirs
from os.path import join, isdir, isfile 


class RomFilter:

	def __init__(self, args):
		self.rom_folder_path = args.rom_folder_path
		self.output_directory = args.output_directory
		self.verbosity = args.v
		self.simulate = args.simulate
		self.fatal = -1
		self.warn = 0
		self.info = 1
		self.debug = 2
		self.trace = 3
		self.extension = args.extension

		self.lang = lang = {'G':4.0, 'E':3.0, 'U':2.0, 'J':1.0}

	# Suggested verbosity levels
	# 1 info
	# 2 debug
	# 3 trace
	def _output(self, string, level=0):
		if (level <= self.verbosity):
			print string
		return

	def _rateFile(self, file_name):

		 # matches:
		 #	1	name 								(.*)
		 #	2	language flag 						(([G|E|U|J])\)
		 #	3	optional: multilanguage with language count (\(M[0-9]\))?
		 #	4	optional: version info 				(\(V([0-9]\.[0-9])\))?
		 #	5		version number X.X 				([0-9]\.[0-9])
		 #	6	optional: verfied good dump 		(\[!\])?
		pattern = r'(.*)\(([G|E|U|J])\).?(\(M[0-9]\))?.?(\(V([0-9]\.[0-9])\))?.?(\[!\])?\.'
		pattern += self.extension
		match = re.match(pattern, file_name)

		if match:

			# check language
			if match.group(2):
				x = self.lang[match.group(2)]
			else:
				x = 0.0

			# check for good dump
			if match.group(6):
				x += 0.9
			else:
				x += 0.5

			# check version
			if match.group(5):
				x += float(match.group(5))/100.0

			return x
		else:
			return -1.0

	def copyRomFiles(self, path):
		self._output( "Checking path " + path, self.debug)
		files = listdir(path)

		self._output( "Path contains:", self.trace)
		self._output( files, self.trace)

		most_rated = ''
		rating= -1;

		for f in files:

			rom = join(path, f)
			if isdir(rom):
				self._output( 'Path ' + rom +' is a directory', self.debug)
				self.copyRomFiles(rom);
			else:
				if isfile(rom):
					
					self._output( rom + 'is a file', self.debug)
					r = self._rateFile(f)
					self._output( f + ' rated ' + str(r), self.debug)

					if rating < r:
						self._output( 'replacing ' + most_rated + ' with ' + f, self.debug)
						most_rated = f
						rating = r
				else:
					self._output( 'Could not determine filetype of ' + f, self.warn)

		if most_rated != '':

			wrongChar= [".", "-", "'", "#", " "]

			stripedname = most_rated
			for c in wrongChar:
				stripedname = stripedname.replace(c, '')

			# copy most rated into new folder
			targetDir = join(self.output_directory, join(stripedname[:1], stripedname[:2], stripedname[:3]).lower())
			if not isdir(targetDir):
				self._output( 'Creating non existing directory ' + targetDir, self.info)
				
				if not self.simulate:
					makedirs(targetDir, mode=0775)
			
			src =join(path,most_rated)
			self._output( 'Copying '+ most_rated + ' from ' + src + ' to ' + targetDir, self.info)

			if not self.simulate:
				copy2(src, targetDir)
		else:
			self._output( 'Found no rom in ' + path + 'that matches any pattern. Nothing copied.', self.warn)
		return

			
	#end copyRomFiles
#end class

def show_help():
	parser = argparse.ArgumentParser(description='Filter game roms in a directory and copy fieles ito new one.')
	parser.add_argument('rom_folder_path', help='Directory to the rom folders')
	parser.add_argument('output_directory', help='Directory where to copy filtered files.')
	parser.add_argument('-v', action='count', default=0, help='Increase verbosity level')
	parser.add_argument('-s', '--simulate', action='store_true', default=False, help="Only output what would hapen but do not actualy copy files or create directories.")
	parser.add_argument('-e', '--extension', choices=['z64', 'smc'], metavar="file_extension", required=True, help="File extension of rom files. Like z64 or smc")
	args = parser.parse_args()
	#print args
	return args

#end help

def main():

	args = show_help()

	if args:
		rom_path = args.rom_folder_path
		rf = RomFilter(args)
		rf.copyRomFiles(rom_path)

	return 0
#end main

if __name__ == "__main__":
    main()