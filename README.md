# Flashbook

GUI that:

  1) facilitate taking notes of PDFs of study books

  2) a flash card program to study them.
  
  3) print the notes you took as a A4 pdf
  
I created this GUI to ease the arduous task of reading (physics) study books, make notes of important formulas and then to study them. Flashbook requires that you convert a PDF to jpg files and put them in the corresponding `%localappdata%/Flashbook/books` folder. This folder can be opened in the menubar of the program.

You can take notes by simply selecting an area with your mouse, a rectangle will be drawn, you can do this multiple times and they will be combined to a single question or answer card. In addition to this you can type an additional question or answer in a textbox that will be combined with the selected areas. In this textbox you can include regular text but also LaTeX code, e.g. `$\partial\beta$` to show `∂β`. In addition you can also add LaTeX macros so that you can almost ask any (mathematical) question.
# NB
- In the ‘files’ subfolder you can define your own LaTeX macros
-	LaTeX environments like matrices are not included

# The program
![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/main.png)
### Flashbook
![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb.png)

You can then create your own Q&A cards by selecting areas with you mouse. 

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb_selection.png)

Once you entered your selection a pop up window will appear, showing you your selection.

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb_selection_entered.png)

You can also create a 'mozaic' by simply clicking on the arrow at the bottom of the page. The direction the arrow is pointing is the direction in which the notes are stitched together. 

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb_selection_entered2.png)

There doesn't have to be a question card, for example when you just want to take notes. In that case once you entered your 'selection' or lack thereof again it will be made permanent. The borders will now be colored black.

It is also possible to enter LaTeX code ![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb_latex.png) 

which will be displayed as 

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb_latex2.png)

It's even possible to add your own LaTeX macros so that you can avoid typing long sequences of code.

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb_latex3.png)

will then give you:

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb_latex4.png)

### Flashcard

