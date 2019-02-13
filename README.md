Topics applied: TCP networks / WMI SQL queries / win32 processes / OOP / multithreading / JSON / traceback logging

# Flashbook : PDF reader & study tool



**The program can do the following:**

  1) Take notes while you read PDFs of study books.

  2) Flash card program to study your notes.
  
  3) Print the notes you took as a PDF.
  
  4) Synchronize multiple devices.
  
I created this GUI to ease the arduous task of reading physics study books that contain a lot of formulas and long derivations of said formulas. I wanted to take notes of important formulas and then afterwards study them. You can put a PDF in the `%localappdata%/Flashbook/PDF books` folder. This folder can be opened in the menubar of the program.

You can take notes by simply selecting an area with your mouse, a rectangle will be drawn, you can do this multiple times and they will be combined to a single question or answer card. In addition to this you can type an additional question or answer in a textbox that will be combined with the selected areas. In this textbox you can include regular text but also LaTeX code, e.g. `$\partial\beta$` to show `∂β`. In addition you can also add LaTeX macros so that you can ask almost any (mathematical) question.


# The program explained

The program will open with the following menu, allowing you to chose between one of the programs. You can always return to this menu once you opened one of the programs.

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/main1.png)
## Flashbook
![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb.png)

Open a book by pressing on the `browse` button. You can then create your own Q&A cards by selecting areas with you mouse. It will draw a box around your selection. Which can easily be undone by clicking your right mouse button.

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb_selection.png)

Once you entered your selection a pop up window will appear, showing you your selection. The pop up will disappear once you move with your cursor over it.

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb_selection_entered.png)


You can also create a 'mozaic' by simply clicking on the arrow at the bottom of the page. The direction the arrow is pointing is the direction in which the new selection gets stitched to the last selection. When the arrow points down it just goes to a new 'row', when it points to the right it adds it to the same row.

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb_selection_entered2.png)

There doesn't have to be an answer card, for example when you just want to take notes. In that case once you entered your 'selection' or lack thereof, it will be made permanent. The borders will now be colored black.

## Flashbook: LaTeX
It is also possible to enter LaTeX code 

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb_latex2.png) ![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb_latex.png) 

It's even possible to add your own LaTeX macros so that you can avoid typing long sequences of code.

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb_latex4.png) ![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb_latex3.png) 

## Flashbook: add webpage screenshots
And finally, you can also add a printscreen you took. For example to add extra info you want to include from the internet.

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/prtscr.png)

you can first crop the image before it is imported. You can then select portions of it to form a Q&A card as if it were a regular page.

## Flashcard

When you open Flashcard and open a book for which you have taken notes - you'll see a pop up window with the settings

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fc.png)

Your progress will be saved after each answer given. Although, the 'continue last session' overrides any other setting and uses the last used settings and score, continuing exactly where you left off.

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fc2.png)

Then you can either use your mouse or your arrow keys to: flip the card, indicate your answer is correct / wrong.

## Print

When you click on the 'print' button you get to the following preview window:

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/print.png)

where you can modify it to your liking. You add lines between Q&A cards (if present) and between each horizontal row of cards. You can also change the color and thickness of these lines. If you press 'apply' a pdf will be made. The location of this folder can be opened via the menubar.

## Synchronizing Devices

You can also sync two devices. It will automatically display the IP address of the device the app is running on. Then you only need to add the other device's IP address. Right now it can only be used on a local wifi network. 

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/sync_gui.png)



### NB
- In the ‘files’ subfolder you can define your own LaTeX macros
-	LaTeX environments like matrices are not included

### TODO
#### To add:
- Clean up code: make it PEP-8 compliant, add clear docstrings to the functions, perhaps move more code from modules to functions in order to make the modules clearer and shorter.
- Perhaps use SQLite for data, currently everything is stored as .tex, .txt, .json files in %localappdata%. Although, now it is easy for users to edit manually, easy to delete etc.
- Customizable colors for Flashbook: the user should be able to choose the color of the temporary and permanent borders.  
- Add ability to combine multiple PDFs for additional information / if a course consists of multiple PDFs: syllabus, book, assignments ...
- Add ability to change a flashcard while you are rehersing: "change current card" which then shows the user input text / the ability to delete the card.
- Improve design: font / colors / borders / icons / ...
#### Issues:

- When you start in Flashcard and then open Flashbook the following occurs: the pages are no longer resized according to the scrollbar (have extra empty space following a page), and you cannot scroll when the mouse is over the image (only when the mouse is next to the image). This also prevents from "scrolling to the next page".

#### Possible Issues:
- pdf conversion may not be supported: pdftoppm.exe is called on laptop via miktex. Explicit import needed in spec file? Now this is hopefully accounted for by including poppler.rar in the executables and adding it as 'path variable' if there is no 'pdftoppm.exe' already available. 

- While working on a laptop flashbook had the following bug: (when only a mousepad was used) taking notes drew borders from the upper left of the screen to the point where the mouse was released. Not starting from the point where the left mouse button was pressed down. After rebooting the laptop this issue vanished. The standard position is (0,0) unless the left button is pressed then it gets updated. So somehow it didn't register the left button click but did register when the button was no longer pressed. 
- Facebook: drawn borders suddenly shifted up and to the left. This does not affect new borders being drawn (or the final selections), or past selections. Perhaps this is caused by a missing self.Layout() where the page should be redrawn. Perhaps the page is rescaled but the borders aren't.
- Python multithreading isn't real multithreading as it just switches rapidly between threads. Perhaps incorporate multiprocessing.

### name changes:
just in case it causes issues further down the line of making things pep8 compliant:
in fc_functions:
- LoadStats => load_stats
- SetStats => set_stats
- RemoveStats = > remove_stats
- SaveStats => save_stats
- SwitchBitmap = >  switch_bitmap
