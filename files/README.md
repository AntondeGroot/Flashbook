# The structure of the files.

The main file is `flashbook.py`

This file contains 4 different programs `Flashbook` / `Flashcard` / `Print` / `Synchronization`

The key events are redirected to the `class_` files for the appropriate program. This way the main file remains orderly.

The elementary building blocks are found in the `_functions.py` files, these contain instructions such as "load page" / "save userdata" / ... and which are used a lot in the `_modules.py` files.

The lay-out of the GUI is entirely determined by the file `gui_flashbook.py` but the buttons are redefined in the `class_` files.









