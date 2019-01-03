the files were created with Wxformbuilder and can be modified by it.

### Using Wxformbuilder
- When you opened Wxformbuilder you can copy paste the generated Python code to the `gui_flashbook.py` file. Beware that you do not replace the first lines which import modules and define paths. 
- Add the variable `data` to the lines `def __init__( self, parent):` i.e. `def __init__( self, parent, data ):` for the 'Dialog' and 'Dialog2' windows
- Then run `WXpython gui Edit.py` in the same folder as where the `gui_flashbook.py` file is located, this replaces some deprecated methods and replaces some faulty code.


### warning
- `gui_flashbook.fbp` creates a directory that depends on where the file is located. This means that in `/files/WXpython gui Edit.py` the line `r'u"D:\\Anton\\Documents\\path_min"','path_min',` needs to be changed in order to change every single occurance of the directory to the variable `path_min`.
