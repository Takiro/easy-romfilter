### Is this for me?

If you have downloaded a huge rom collection from your favorite source and you want to automatically filter for just the languages you want and store them in an easy to search manner, than this is definitely for you.

### What is this?

easy-romfilter traverses your collection of tagged rom files and only copies the most useful roms into a new collection.
The Program checks each file for specific tags like language/region, version and if its a verified good dump. It ignores all rom files that are tagged as hack, bad dump, trained and other files you usually don't want for your emulators rom library. Each selected rom file will be copied into a three level alphabetic directory tree. This means that a game like "AAAAH! Real Monsters" would be in `/a/aa/aaa` whereas "Super Mario World" would be copied to `s/su/sup/`. This directory structure should ensure that you find any game quickly even if you have a massive collection.  

### Installation

The program itself needs no installation. Just download the file easy-romfilter and run it. Since it is written in python it should run without an issue on any Operation System with python support. A lot of Linux distributions already ship with python installed. You probably need to install python on Windows, Mac OS and other Operating Systems, first.  

### Usage

If you already have a python installation on your System you can start the program from the command line.  

easy-romfilter can take up several command line arguments  
		
		easy-romfilter.py	[-h] [-v] [-s] -e file_extension [-r region_tags]
        					[--version] [--ignore-super]
                         	rom_folder_path output_directory  

On Linux with minimum required arguments:  
$ `python easy-romfilter.py -e smc rom_folder_path output_directory`  

`-e file_extension`, `--extension file_extension` takes a rom file extension as an argument like smc for SNES or z64 for Nintendo 64 roms.  

`rom_folder_path` is a relative or absolute path to your previous library.  

`output_directory` is a relative or absolute path to the directory where the filtered library should be copied to. If the directory does not exist already it will be created.  

These tree arguments are the only required ones.  

#### Other Options

As you can see above the program has a few optional parameters.  

`-s`, `--simulate`		Only output what would happen but do not actually copy files or create directories. Very useful if you just want try out if everything works fine.  

`-r tags`, `--regions tags` Takes a comma separated list of region/language tags and assumes it is ordered descending by priority. Example `-r U,UK,E`,... would try to find a US version of a game, and use UK in case there is no US version available. If there is no UK version it uses the European and so on. Default is `U,UK,E,J`  

`-v`					Increase how much output the program should generate. You can use it up to three times by just adding one to another. `-vvv`  

`--ignore-super`		The "Super " prefix lots of Super Nintendo games have is ignored for sorting. A game like "Super Mario World" would be sorted into m/ma/mar instead of /s/su/sup with lots of other games beginning with "Super "

`--version`				Prints the programs version info and exits.  

`-h`, `--help`			print a help that shows useful informations for each argument.  

#### Examples

Copy smc files from a directory called roms in your home directory to another one and output the filenames and directories of the files:  

$ `python easy-romfilter.py -v -e smc /home/user/roms snes_filtered/`  

**Note** that the output directory is a path relative to easy-romfilter.py  
You can of course use relative paths for in- and output directories  


Copy only files that are tagged as US or UK region to a mounted drive like a external hard drive.  

$ `python easy-romfilter.py -r U,UK -e smc /home/user/roms /media/somedrive/somefolder/  

**Note** that regions are evaluated in Order. This means that the program tries to find a rom tagged as U and only uses the next one if it cannot find the previous region tag.  


Do not actually copy anything but show everything that would happen:  

$ `python easy-romfilter.py -vvv --simulate -e z64 roms/ n64_filtered/`  

Of course you can use the short option `-s` instead of `--simulate if` you want, its the same wit `-e`  


*If you are not sure if you have done everything right, you should use `-s`.*  

### Input and Output

easy-romfilter assumes that all the rom files that belong to one game reside in one folder even if there is just one version of the rom available.  
This means your source directory should look like this. After the first level you can introduce as many subdirectories as long as thy group files of the same game.  

		.
		├── 2020 Super Baseball
		│   ├── 2020 Super Baseball (J) [a1][hI].smc
		│   ├── 2020 Super Baseball (J) [h1C].smc
		│   ├── 2020 Super Baseball (J) [hI].smc
		│   ├── 2020 Super Baseball (J).smc
		│   ├── 2020 Super Baseball (U) [b1].smc
		│   └── 2020 Super Baseball (U).smc
		├── 3ji no Wide Shou
		│   ├── BS 3ji no Wide Shou (J) [h1].smc
		│   └── BS 3ji no Wide Shou (J).smc
		├── 3 Ninjas Kick Back
		│   ├── 3 Ninjas Kick Back (U).smc
		│   ├── 3 Ninjas Kick Back (U) [T+Fre1.00_GenerationIX].smc
		│   └── 3 Ninjas Kick Back (U) [T+Ger1.00_Star].smc
		├── 3x3 Eyes - Juuma Houkan
		│   ├── 3x3 Eyes - Juuma Houkan (J) [b1].smc
		│   ├── 3x3 Eyes - Juuma Houkan (J) [f1].smc
		│   ├── 3x3 Eyes - Juuma Houkan (J) [h1C].smc
		│   ├── 3x3 Eyes - Juuma Houkan (J) [h2C].smc
		...	...	....
		...	...	....
		...	...	....

		├── Brawl Brothers 
		│   └── Brawl Brothers (U) [!].smc
		├── BreakThru!
		│   ├── BreakThru! (U) [h1C].smc
		... ... ...
		... ... ...
		... ... ...
		│   ├── Zool (U).smc
		│   └── Zool (U) [t1].smc
		├── Zoop
		│   ├── Zoop (E) [!].smc
		│   ├── Zoop (U) [b1].smc
		│   ├── Zoop (U) [b2].smc
		│   ├── Zoop (U) [f1].smc
		│   ├── Zoop (U) [h1C].smc
		│   └── Zoop (U) [!].smc
		└── Zootto Mahjong!
		    ├── BS Zootto Mahjong! Event Version (J) [h1].smc
		    ├── BS Zootto Mahjong! Event Version (J).smc
		    ├── BS Zootto Mahjong! Preview Version (J) [h1].smc
		    ├── BS Zootto Mahjong! Preview Version (J).smc
		    └── Zoo-tto Mahjong! (J) (NP).smc

The Program then produces a directory tree that looks like this.  

		.
		├── 2
		│   └── 20
		│       └── 202
		│           └── 2020 Super Baseball (U).smc
		├── 3
		│   ├── 3n
		│   │   └── 3ni
		│   │       └── 3 Ninjas Kick Back (U).smc
		│   └── 3x
		│       └── 3x3
		│           ├── 3x3 Eyes - Juuma Houkan (J).smc
		│           └── 3x3 Eyes - Seima Kourinden (J).smc
		├── 4
		│   └── 4n
		│       └── 4ni
		│           └── 4 Nin Shougi (J).smc
		... ... ... ... ...
		... ... ... ... ...
		... ... ... ... ...
		└── z
		    ├── za
		    │   ├── zak
		    │   │   └── Zakuro no Aji (J).smc
		    │   └── zan
		    │       ├── Zan III Spirits (J).smc
		    │       └── Zan II Spirits (J).smc
		    ├── ze
		    │   ├── zen
		    │   │   ├── Zenkoku Juudan - Ultra Shinri Game (J).smc
			... ... ...
			... ... ...
			... ... ...
		    ├── zi
		    │   ├── zic
		    │   │   └── Zico Soccer (J) [!].smc
		    │   └── zig
		    │       └── Zig Zag Cat - Ostrich Club mo Oosawagi da (J).smc
		    └── zo
		        ├── zom
		        │   └── Zombies (E).smc
		        └── zoo
		            ├── Zool (E).smc
		            └── Zoop (E) [!].smc
