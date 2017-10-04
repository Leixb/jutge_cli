jutge\_cli: a command line client for jutge.org
===============================================

Disclaimer
----------

This is a work in progress. I will not take any responsibility if things
break.

Installation
------------

To install python module run:

.. code:: sh

    sudo python3 setup.py install

This should install all dependencies and create an executable named
``jutge`` in your ``$PATH``.

Usage
-----

To use ``jutge_cli`` run the command ``jutge`` followed by the
subcommand you want to execute:

::

    jutge [SUBCOMMAND] [SUBCOMMAND_OPTIONS]

For the program to work you will have to either specify the code of the
problem you want to test (``-c`` flag) or rename the program file so
that it begins with the code. The code must match the following regular
expression: ``[PGQX]\d{5}_(ca|en|es)`` (note that the code includes the
language). You can provide a custom regular expression through the
``--regex`` flag.

Configuration
-------------

You can configure default parameters through the YAML configuration file:
``~/.jutge_cli.yaml``. The following example lists all the options and
their default values:

.. code:: yaml

    database : ~/Documents/jutge/DB
    regex : '[PGQX]\d{5}_(ca|en|es)'
    diff-prog : diff
    diff-flags : -y
    inp-suffix : inp
    cor-suffix : cor
    folder : ~/Documents/jutge/Done

You can also add problem sets with the ``problem_sets`` setting. These will
make the commands ``new``, ``archive`` and ``update`` classify problems into
folders:

.. code:: yaml

    problem_sets:
        P1: [P19724, P34279, P37297, P37469, P42042, P51126, P51352, P61634, P66529, P67171, P70955, P82374, P89265, P92351, P98960, P99182, X54725, X59678, X64734, X89070]
        P2: [P27341, P28754, P29448, P32046, P34451, P35547, P37500, P55622, P59539, P59875, P60816, P64976, P65171, P74398, P79784, P85370, P97156, X30229, X32391, X80452]
        P3: [P13623, P19991, P29973, P32533, P61061, P79817, P80660, P87323, P96767, X01646, X08783, X26853, X29759, X59091, X84338, X98097]

The above configuration file will save problems ``P19724``, ``P34279``... into
folder ``P1`` and so on.

Cookie handling
---------------

Some problem from jutge.org (the ones which code starts with X) are only
accessible to logged users and therefore if you want to download the
required information from jutge.org of those problems you'll have to
provide a valid PHPSSID cookie through the ``--cookie`` flag. This flag
must appear before the command:

.. code:: sh

    jutge --cookie MY_COOKIE download -c X00000

Alternatively you can issue the command:

.. code:: sh

    jutge cookie MY_COOKIE

Which will save the cookie in a temporary file and will be used in all
other commands. Please note that this is not ideal since the file and
therefore the cookie is accessible in plain text by any user till next
reboot.

Global flags
------------

Most of the flags depend on the subcommands, but there are some global
flags that effect all subcommands. Those are:

-  ``--regex MY_REGEX`` Regex used to extract codes from filenames
-  ``--cookie MY_COOKIE`` Cookie used to connect to jutge.org
-  ``--database FOLDER`` Change database location
-  ``--no-download`` Do not attempt to download anything when not found
   in database

Commands
--------

``jutge_cli`` consists of different commands that achieve different
things.

Add cases
~~~~~~~~~

This command adds a custom test case into the database. The case can be
provided through the flags ``-i`` (input) and ``-o`` (expected output)
or through stdin.

Example
^^^^^^^

This command will add the contents of files ``inp`` and ``cor`` to the
database as test cases for the problem ``P00001_ca``

::

    jutge add_cases -i inp -o cor P00001_ca_prog.cpp

Archive
~~~~~~~

This command moves a file to the ``Done`` folder. This folder can be
changed through the ``-f`` flag. To override files already in the folder
use the ``--overwrite`` flag.

Example
^^^^^^^

This command will move the file ``P00001_ca_prog.cpp`` to the folder
``Accepted`` and overwrite if necessary.

::

    jutge archive --folder Accepted/ P00001_ca_prog.cpp --overwrite

Download
~~~~~~~~

This command will attempt to download the html page and zip file
corresponding to the given problem from jutge.org and add them to the
database. Either a code flag (``-c``) or a program file (``-p``) must be
provided.

Note that other commands that depend on the database files will
automatically try to download them if they don't exist and therefore
this command is only useful when populating the database in advance.

Example
^^^^^^^

This command will populate the local database for problem ``P00001_en``:

::

    jutge download -c P00001_en

New
~~~

This command must be followed by a code. It will fetch the problem title
from the code and create a new file whose name is the code followed by
the title. The ``-p`` flag can be used to specify the extension of the
file.

Example
^^^^^^^

This command will populate create a new python file named
``P87523_ca_-_Hola-adéu.py``

::

    jutge new P87523_ca -p py

Print
~~~~~

This command provides 3 sub commands to print to stdout information
about the problem. Those are:

-  ``title``
-  ``stat``
-  ``cases``

Example
^^^^^^^

This command will print all cases in the database for the problem
``P87523_ca`` (if any).

::

    jutge print cases -c P87523_ca

Test
~~~~

This is the most useful command in the tool set. It allows to test your
code against all the test cases found in the database and output side by
side differences using ``diff``.

The command takes an executable file as parameter and tests it against
the test cases in the database folder. You can specify an alternate diff
program to use and its flags (separated by commas) through
``--diff-prog`` and ``--diff-flags``.

Example
^^^^^^^

This command will test the executable ``P87523_ca_prog.x`` against the
test cases for problem P87523\_ca. The expected output and the output of
the program will be shown side by side using ``colordiff``.

::

    jutge test P87523_ca_prog.x --diff-prog colordiff

Update
~~~~~~

This command extracts all accepted submissions from a jutge.org zip
file, renames them according to their title and adds them to the
``Done`` folder. Note that the zip file must be the one downloaded from
your jutge.org profile.

::

    jutge update problems.zip

Upload
~~~~~~

This command uploads a file to jutge.org to be evaluated. Note that you must
have a valid cookie previously saved by ``jutge cookie PHPSSID`` or you
can provide it through the ``--cookie`` flag. As of now, the program cannot
report if the upload was successful so you will have to check your submissions
page manually. The compiler to use will be determined by the filename extension
but you can specify another one through the ``--compiler`` flag.

::

    jutge upload P00001_ca_prog.cpp --compiler 'G++'

Check-submissions
~~~~~~~~~~~~~~~~~

This command checks the last submissions to jutge.org and displays them in the
terminal. The program will return 0 if the last submission's veredict is ``AC``
and 1 otherwise. This subcommand accept 2 flags: ``--last`` that tells it to
show only the last submission and ``--reverse`` that shows the last submission 
on top of the list:

::
    
    jutge check-submissions --last
