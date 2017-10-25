jutge\_cli: a command line interface for `jutge.org <https://jutge.org>`_
========================================================================

#. `Intro`_
#. `Installation`_

    #. `Archlinux PKGBUILD`_
    #. `Installation using virtualenv (no root)`_

#. `Usage`_
#. `Configuration`_
#. `Login`_
#. `Commands`_
#. `License`_


Intro
-----

``jutge_cli`` is a python3 console application that aims to automate common
tasks when working with `jutge.org <https://jutge.org>`_ problems. Those tasks
include:

* Creating new files named after problem title given the problem code
* Displaying statement and public test cases of a given problem
* Compiling and testing a program against public test cases
* Uploading program solutions to `jutge.org <https://jutge.org>`_
* Checking `jutge.org <https://jutge.org>`_ results for last submissions or
for a specific problem.
* Adding ant testing against custom test cases to a problem
* Batch uploading problems from a given problem set
* Batch creating new files of a given problem set
* Extract and rename problem solutions from a `jutge.org <https://jute.org>`_
zip file export to a specific folder.


Installation
------------

``jutge_cli`` is packed as python3 package and as such, it can be installed
through ``setup.py``.


Global installation (root)
~~~~~~~~~~~~~~~~~~~~~~~~~~

To install python module run:

.. code:: sh

    sudo python3 setup.py install

This should install all dependencies and create an executable named
``jutge`` in ``/usr/bin/jutge``.


Archlinux PKGBUILD
~~~~~~~~~~~~~~~~~~

There is also a ``PKGBUILD`` included in the repository for arch linux users.


Installation using virtualenv (no root)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can install this program inside of a python3 
`virtualenv <https://virtualenv.pypa.io/>`_:

.. code:: sh

    virtualenv jutge_cli_venv && cd !$
    source bin/activate
    git clone https://github.com/leixb/jutge_cli
    python3 jutge_cli/setup.py install && cd -

Once the above commands complete successfully, the ``jutge`` will be installed
inside the ``bin`` folder of the virtualenv. It is recommended to link it to
the user ``bin`` folder and add it to your ``$PATH``.

.. code:: sh

    mkdir ~/bin
    ln -s bin/jutge ~/bin/jutge

Remember to add bin to your path by adding the following line to ``.bashrc``
or equivalent:

.. code:: sh

    export PATH=$PATH:~/bin


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
language although it is not mandatory).


Configuration
-------------

You can configure default parameters through the YAML configuration file:
``~/.jutge_cli.yaml``.

Basic options
~~~~~~~~~~~~~

The following example lists all the basic options and
their default values:

.. code:: yaml

    database : ~/Documents/jutge/DB
    regex : '[PGQX]\d{5}_(ca|en|es)'
    diff-prog : diff
    diff-flags : -y
    inp-suffix : inp
    cor-suffix : cor
    folder : ~/Documents/jutge/Done

Those options can also be specified using the flags with the same name.

Although you can change the regex it is not recommended to do so since bad
regex may break correct functionality.


Problem sets
~~~~~~~~~~~~

You can also add problem sets with the ``problem_sets`` group. These will
make the commands ``new``, ``archive`` and ``update`` classify problems into
folders:

.. code:: yaml

    problem_sets:
        P1: [P19724, P34279, P37297, P37469, P42042, P51126, P51352, P61634, P66529, P67171, P70955, P82374, P89265, P92351, P98960, P99182, X54725, X59678, X64734, X89070]
        P2: [P27341, P28754, P29448, P32046, P34451, P35547, P37500, P55622, P59539, P59875, P60816, P64976, P65171, P74398, P79784, P85370, P97156, X30229, X32391, X80452]
        P3: [P13623, P19991, P29973, P32533, P61061, P79817, P80660, P87323, P96767, X01646, X08783, X26853, X29759, X59091, X84338, X98097]

The above configuration file will save problems ``P19724, P34279...`` into
folder ``P1``, problems ``P27341, P28754...`` into ``P2`` and so on.


Login information
~~~~~~~~~~~~~~~~~

You can also provide login credentials in the configuration file inside
the group ``login``:

.. code:: yaml

    login:
        email: myemail@mydomain.com
        password: mypassword

You can omit either email, password or both and the login command will
prompt the user for input when issued.


Login
-----

To upload problem solutions or to access private problems (the ones which code
starts with ``X``) you must be logged in into `jutge.org <https://jutge.org>`_.
The preferred method to login is through the ``jutge login`` command although
there are 2 more methods involving cookies.


login command
~~~~~~~~~~~~~

Issuing the command ``jutge login`` will prompt the user for their email and
password and save the session cookie for next use. If username or
password are already provided in `Login information`_ it will not prompt the
user to input them.


cookie command
~~~~~~~~~~~~~~

The command ``jutge cookie`` accepts a cookie as a parameter and will
store it for next use.

cookie flag
~~~~~~~~~~~

You can also explicitly provide a cookie to each subcommand call through the
``--cookie`` flag:

.. code:: sh

    jutge --cookie MY_COOKIE download -c X00000


Global flags
------------

Most of the flags depend on the subcommands, but there are some global
flags that effect all subcommands. Those are:

-  ``--regex MY_REGEX`` Regex used to extract codes from filenames
-  ``--cookie MY_COOKIE`` Cookie used to connect to `jutge.org <https://jutge.org>`_
-  ``--database FOLDER`` Change database location
-  ``--no-download`` Do not attempt to download anything when not found
   in database

Commands
--------

Add cases (add-cases|add)
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

Archive (archive)
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

Download (download|down)
~~~~~~~~

This command will attempt to download the html page and zip file corresponding
to the given problem from `jutge.org <https://jutge.org>`_ and add them to the
database. Either a code flag (``-c``) or a program file (``-p``) must be
provided.

Note that other commands that depend on the database files will
automatically try to download them if they don't exist and therefore
this command is only useful when populating the database in advance.

Example
^^^^^^^

This command will populate the local database for problem ``P00001_en``:

::

    jutge download P00001_en

New (new)
~~~~~~~~~

This command must be followed by a code. It will fetch the problem title
from the code and create a new file whose name is the code followed by
the title. The ``--extension`` or ``-e`` flag can be used to specify the
extension of the file.

If flag ``--problem-set`` is provided, all programs in the specified problem
set will be created

Example
^^^^^^^

This command will populate create a new python file named
``P87523_ca_-_Hola-adéu.py``

::

    jutge new P87523_ca --extension py

Show (show)
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

    jutge show cases P87523_ca

Test (test)
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

Import (import)
~~~~~~

This command extracts all accepted submissions from a `jutge.org
<https://jutge.org>`_ zip file, renames them according to their title and adds
them to the ``Done`` folder. Note that the zip file must be the one downloaded
from your `jutge.org <https://jutge.org>`_ profile.

::

    jutge import problems.zip

Upload (up)
~~~~~~

This command uploads a file to `jutge.org <https://jutge.org>`_ to be
evaluated. Note that you must have a valid cookie previously saved by ``jutge
cookie PHPSSID`` or you can provide it through the ``--cookie`` flag. As of
now, the program cannot report if the upload was successful so you will have to
check your submissions page manually. The compiler to use will be determined by
the filename extension but you can specify another one through the
``--compiler`` flag.

::

    jutge upload P00001_ca_prog.cpp --compiler 'G++'

If the flag ``--problem-set`` the command will upload all problems from the
specified set found in the current working directory or in the set folder in
the current working directory. (Keep in mind that `jutge.org
<https://jutge.org>`_ limits the number of submissions to 20 per hour so it is
discouraged to use this flag with large problem sets)

By default upload will test all problems against public test cases in the
database (not including custom ones). You can skip those checks with the flag
``--skip-check``

If you want to check the submitted problem verdict directly after upload, use
the flag ``--check`` which will wait for the jutge verdict and output it.

Check-submissions (check)
~~~~~~~~~~~~~~~~~

This command checks the last submissions to `jutge.org <https://jutge.org>`_
and displays them in the terminal. The program will return 0 if the last
submission's veredict is ``AC`` and 1 otherwise. This subcommand accept
2 flags: ``--last`` that tells it to show only the last submission and
``--reverse`` that shows the last submission on top of the list:

::

    jutge check --last

You can also check the status of a problem by using the flag ``--code``

License
-------

This software is licensed under the `GPL v3 license <http://www.gnu.org/copyleft/gpl.html>`_.
