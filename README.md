Topics applied: TCP networks / WMI SQL queries / win32 processes / OOP / multithreading / JSON / traceback logging

# Flashbook : PDF reader & study tool, a summary:

for a more in depth guide see the [wiki](https://github.com/AntondeGroot/Flashbook/wiki)

**The program can do the following:**

  1) Take notes while you read PDFs of study books.

  2) Flash card program to study your notes.
  
  3) Print the notes you took as a PDF.
  
  4) Synchronize multiple devices.
  
I created this GUI to ease the arduous task of reading physics study books that contain a lot of formulas and long derivations of said formulas.

You can take notes by simply selecting an area with your mouse, a rectangle will be drawn, you can do this multiple times and they will be combined to a single question or answer card. In addition to this you can type an additional question or answer in a textbox that will be combined with the selected areas. In this textbox you can include regular text but also LaTeX code, e.g. `$\partial\beta$` to show `∂β`.


# The program explained

The program will open with the following menu.

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/main2.png)
## Flashbook


You can create your own Q&A cards by selecting areas with you mouse. It will draw a box around your selection. Which can easily be undone by clicking your right mouse button.

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb_selection2.png)

You can choose how the selections are stitched together, for example:

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb_selection_entered21.png)


or

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb_selection_entered22.png)


It is possible to combine multiple notes and then use that to rehearse or to print it as a PDF, for example if you want to combine lecture notes with homework assignments.


## Flashbook: LaTeX
It is also possible to enter LaTeX code 

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb_latex2.png) ![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb_latex.png) 

## Flashbook: add webpage screenshots
You can also add a printscreen you took. For example to add extra info or graphics you want to include.

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/prtscr2.png)

## Flashcard

When you open Flashcard and open a book for which you have taken notes - you'll see a pop up window with the settings

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fc.png)

Your progress will be saved after each answer given. Although, the 'continue last session' overrides any other setting and uses the last used settings and score, continuing exactly where you left off.

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fc3.png)

Then you can either use your mouse or your arrow keys to: flip the card, indicate your answer is correct / wrong.

Only when you use Flashcard can you press on the 'flashcard' button in the menubar. You can then chose to edit or delete the current flashcard, and it also allows you to skip back to the previous flashcard so you could edit or delete that one too.

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fc4.png)

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fc5.png)

## User data

The program will also keep track of your progress and indicate how many minutes you've spend learning and reading the past N days. It will first list all Flashcards times in ascending order and then the Flashbook times in ascending order. This way you can instantly see which Flashcard you need to learn first.
![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/statsgraph2.png)
## Print

When you click on the 'print' button you get to the following preview window:

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/print5.png)

where you can modify it to your liking. You add lines between Q&A cards (if present) and between each horizontal row of cards. You can also change the color and thickness of these lines. If you press 'apply' a pdf will be made. The location of this folder can be opened via the menubar.

#### Edit the cards
You can edit a card by clicking on it and entering the Question and/or Answer. You also have the option to add a topic to a card. Topics will be the page wide black bar with text as you can see in the above image. When the very first card does not contain a topic it will automatically create the title of the book.

## Synchronizing Devices

You can also sync two devices. It will automatically display the IP address of the device the app is running on. Then you only need to add the other device's IP address. Right now it can only be used on a local wifi network. 


![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/sync_gui2.png)



### NB
- In the ‘files’ subfolder you can define your own LaTeX macros
-	LaTeX environments like matrices are not included

### TODO
#### To add:
- Clean up code: make it PEP-8 compliant, add clear docstrings to the functions, perhaps move more code from modules to functions in order to make the modules clearer and shorter. 
- Use more Classes and methods instead of functions from different files: all initialization files could then be removed and incorporated in the respective classes.
- Customizable colors for Flashbook: the user should be able to choose the color of the temporary and permanent borders. 
- Sync: sync should indicate it is working. This can be implemented by a stopable thread and custom events to trigger actions outside the thread to display loading dots (...). But also it says "starting client" but not that it is sending data, when it is actually sending data.
- sync should be optimized: when a lot of files need to be transfered it might take quite a while (~20 minutes). But when most of the files have been updated it'll be very quick. Perhaps 
- some Dialog windows are unnecessary. Just use the Dialogs with 2 bitmaps and when there is only 1 picture to be shown then the second bitmap can just be an empty bitmap. 

#### Possible Issues:
- pdf conversion may not be supported: pdftoppm.exe is called on laptop via miktex. Explicit import needed in spec file? Now this is hopefully accounted for by including poppler.rar in the executables and adding it as 'path variable' if there is no 'pdftoppm.exe' already available. 
- the statsgraph might not show the time spend in Flashbook if the bookname also occurs in Flashcard. Only seen this error occur once.

#### Bugs:
- currently no known bugs
