# The structure of the files.

The main file is `flashbook.py`, all the key events are processed here.

The lay-out of the GUI is entirely determined by the file `gui_flashbook.py`

This file contains 4 different programs `Flashbook` / `Flashcard` / `Print` / `Synchronization`

What happens in the selection menu is determined by the file `program.py` this will start 1 of the 4 programs.

The elementary building blocks are found in the `_functions.py` files, these contain instructions such as "load page" / "save userdata" / ...

The combinations of these building blocks can be found in the `_modules.py` files. These contain instructions for when directories are changed or certain key events trigger complicated operations.



