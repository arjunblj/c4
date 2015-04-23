
The only dependency other than Python is numpy which is most easily installable
via the pip package manager.

You can check to see if numpy is installed very simply, by entering the Python
shell (`python`) and typing in `import numpy` -- that should import without a
hassle.

If you're having issues with that, you'll need to acquire numpy. The easiest way
is to simply `pip install numpy` (sudo may be required). This can also be done
in a virtualenv (indeed, that's what I'd recommend).

Once installed, launching the terminal version of the game is as simple as
`python play.py`. In that file, the different players are defined and are pretty
self explanatory to change and extend.