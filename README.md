# Flashbook

GUIs that:

  1) facilitate taking notes of PDFs of study books

  2) a flash card program to study them.
  
  3) print the notes you took as a A4 pdf
  
I created these two GUIs to ease the arduous task of reading (physics) study books, make notes of important formulas and then to study them. Flashbook requires that you convert a PDF to jpg files and put them in the corresponding `%localappdata%/Flashbook/books` folder. This folder can be opened in the app.

You can take notes by simply selecting an area with your mouse, a rectangle will be drawn, you can do this multiple times and they will be combined to a single question or answer card. In addition to this you can type an additional question or answer in a textbox that will be combined with the selected areas. In this textbox you can include regular text but also LaTeX code, e.g. `$\partial\beta$` to show `∂β`. In addition you can also add LaTeX macros so that you can almost ask any (mathematical) question.
# NB
- In the ‘files’ subfolder you can define your own LaTeX macros
-	LaTeX environments like matrices are not included

# Needs to be added or changed:
- taken notes are saved as images in the format "bookname_page_XXXX" with a 4 digit random number, although unlikely it may overwrite a previous taken note.
