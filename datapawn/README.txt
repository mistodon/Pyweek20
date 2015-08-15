Datapawns
===============

Entry in PyWeek #20  <http://www.pyweek.org/20/>
URL: https://pyweek.org/e/brunch_massacre/
Team: Brunch Massacre
Members: scav, Strings
License: (MIT) see LICENSE.txt


Running the Game
----------------

On Windows or Mac OS X, locate the "run_game.pyw" file and double-click it.

Otherwise open a terminal / console and "cd" to the game directory and run:

  python run_game.py

You might get an error 'Could not create GL Context'. This is a known pyglet bug
see:  https://bitbucket.org/pyglet/pyglet/commits/0a6857ef0468#chg-pyglet/gl/xlib.py
The error will be intermittent, and it should work after a few tries.

Sorry about that. Would have monkey-patched it, but can't even import the module when it happens.


How to Play the Game
--------------------

The Datapawns are led across the wasteland on a mission

They are controlled by issuing rhythmic commands.


Development notes 
-----------------

Creating a source distribution with::

   python setup.py sdist

You may also generate Windows executables and OS X applications::

   python setup.py py2exe
   python setup.py py2app

Upload files to PyWeek with::

   python pyweek_upload.py

Upload to the Python Package Index with::

   python setup.py register
   python setup.py sdist upload

