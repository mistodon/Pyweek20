Datapawn
========

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

Quick Notes
-----------
We spent a lot less time on this than we would have liked to, so it's more of a demo than a game.


How to Play the Game
--------------------

The Datapawns traverse the junkyard, fleeing the wicked light of the Magenta Moon.

Hit the arrow keys in time with the music to send commands to the Datapawns.

The commands are made of four symbols, where each symbol is one of:

1.  Up:     "Data" (or "D")
2.  Right:  "1"
3.  Down:   "0"
4.  Left:   "-"

The commands you will need are:

### Commands
Everybody move right:   D, D, D, 1
Everybody move left:    D, D, D, -
Everybody attack:       D, D, -, 1

When the frame of the screen pulses white, that's when you should hit the keys. When it pulses grey, just wait. When it pulses yellow, get ready because the next beat will be white again.

If for some reason you want to explore the mechanic we never got around to using, you can change the first symbol of any command to "1" or "0".

Changing it to a "1" sends the command only to the leader.
Changing it to a "0" sends the command to everyone except the leader.


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

