the files were created with Wxformbuilder and can be modified by it.

- When you opened Wxformbuilder you can copy paste the generated Python code to the `gui_flashbook.py` file. Beware that you do not replace the first lines which import modules and define paths. 
- Add the variable `data` to the lines `def __init__( self, parent):` i.e. `def __init__( self, parent, data ):` for the 'Dialog' and 'Dialog2' windows
- Then run `WXpython gui Edit.py` in the same folder as where the `gui_flashbook.py` file is located, this replaces some deprecated methods and replaces some faulty code.
