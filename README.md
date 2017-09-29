jutge_cli: a command line client for jutge.org
==============================================

Intro
-----

`jutge_cli` provides different commands to speed up the organization and
test of jutge.org problems.

Installation
------------

Clone the repository and install the dependencies.

### Dependencies ###

This program is build in python3 and depends on the following libraries:

```bash
requests
zipfile
bs4
pypandoc # optional, only used with print command
```

Usage
-----

To use `jutge_cli` run the main file `jutge.py` with the command you want
to execute:

```
python3 jutge.py [COMMAND] [COMMAND_OPTIONS]
```

For the program to work you will have to either specify the code of the
problem you want to test (`-c` flag) or rename the program file so that it
begins with the code. The code must match the following regular expression:
`[PGQX]\d{5}_(ca|en|es)` (note that the code includes the language). You can
provide a custom regular expression through the `--regex` flag.

Configuration
-------------

You can configure default parameters through the configuration file:
`~/.jutge_cli.conf`. The following example lists all the options and their
default values:

```ini
[DEFAULT]
database = ~/Documents/jutge/DB
regex = [PGQX]\d{5}_(ca|en|es)
diff-prog = diff
diff-flags = -y
inp-suffix = inp
cor-suffix = cor
folder = ~/Documents/jutge/Done
```

Cookie handling
---------------

Some problem from jutge.org (the ones which code starts with X) are only
accessible to logged users and therefore if you want to download the required
information from jutge.org of those problems you'll have to provide a valid
PHPSSID cookie through the `--cookie` flag. This flag must appear before the
command:

```sh
jutge.py --cookie MY_COOKIE download -c X00000
```

Global flags
------------

Most of the flags depend on the subcommands, but there are some global flags
that effect all subcommands. Those are:

- `--regex MY_REGEX` Regex used to extract codes from filenames
- `--cookie MY_COOKIE` Cookie used to connect to jutge.org
- `--database FOLDER` Change database location
- `--no-download` Do not attempt to download anything when not found in
  database

Commands
--------

`jutge_cli` consists of different commands that achieve different things.

### Add cases ###

This command adds a custom test case into the database. The case can be
provided through the flags `-i` (input) and `-o` (expected output) or
through stdin.

#### Example

This command will add the contents of files `inp` and `cor` to the
database as test cases for the problem `P00001_ca`

```
jutge.py add_cases -i inp -o cor P00001_ca_prog.cpp
```

### Archive ###

This command moves a file to the `Done` folder. This folder can be
changed through the `-f` flag. To override files already in the folder
use the `--overwrite` flag.

#### Example

This command will move the file `P00001_ca_prog.cpp` to the folder `Accepted` and overwrite if necessary.

```
jutge.py archive --folder Accepted/ P00001_ca_prog.cpp --overwrite
```

### Download ###

This command will attempt to download the html page and zip file
corresponding to the given problem from jutge.org and add them to
the database. Either a code flag (`-c`) or a program file (`-p`) must
be provided.

Note that other commands that depend on the database files will automatically
try to download them if they don't exist and therefore this command is only
useful when populating the database in advance.

#### Example

This command will populate the local database for problem `P00001_en`:

```
jutge.py download -c P00001_en
```


### New ###

This command must be followed by a code. It will fetch the problem title
from the code and create a new file whose name is the code followed by
the title. The `-p` flag can be used to specify the extension of the file.

#### Example

This command will populate create a new python file named
`P87523_ca_-_Hola-adéu.py`

```
jutge.py new P87523_ca -p py
```

### Print ###

This command provides 3 sub commands to print to stdout information about the problem.
Those are:

- `title`
- `stat`
- `cases`

#### Example

This command will print all cases in the database for the problem `P87523_ca` (if any).

```
jutge.py print cases -c P87523_ca
```

### Test ###

This is the most useful command in the tool set. It allows to test your code
against all the test cases found in the database and output side by side
differences using `diff`.

The command takes an executable file as parameter and tests it against
the test cases in the database folder. You can specify an alternate diff program
to use and its flags (separated by commas) through `--diff-prog` and
`--diff-flags`.

#### Example

This command will test the executable `P87523_ca_prog.x` against the test
cases for problem P87523_ca. The expected output and the output of the
program will be shown side by side using `colordiff`.

```
jutge.py test P87523_ca_prog.x --diff-prog colordiff
```

### Update ###

This command extracts all accepted submissions from a jutge.org zip file,
renames them according to their title and adds them to the `Done` folder.
Note that the zip file must be the one downloaded from your jutge.org
profile.

```
jutge.py update problems.zip
```

TODO
----

- Improve cookie handling
- `jutge upload`

