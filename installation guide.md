## Installation

1. download all the files in the `files` folder
1. go in command prompt to the relevant folder
1. create a .spec file by typing: `pyi-makespec pyinstaller flashbook-1.0.0.py --icon=book.ico`
1. then add to the created .spec file:
```
import sys
sys.setrecursionlimit(5000)
block_cipher = None
```
at the beginning of the file

4. run pyinstaller `"pyinstaller flashbook-1.0.0.spec"`  
5. do the same for the flashcard files

--------------------------------
## Errors: 

1. if it gives any errors like: `"pyqt5 folder cannot be found"` then delete pyqt5 and install it again with `pip3 install pyqt5`

1. if the error reads: `"pyinstaller bincache may be corrupted"` then go to `%appdata%` and delete the entire pyinstaller folder and run pyinstaller again.