Topics applied: TCP networks / minor SQL queries / win32 processes / OOP / multithreading / JSON / 

# Flashbook 

GUI that:

  1) facilitate taking notes of PDFs of study books

  2) a flash card program to study them.
  
  3) print the notes you took as a A4 pdf
  
I created this GUI to ease the arduous task of reading (physics) study books, make notes of important formulas and then to study them. Flashbook requires that you convert a PDF to jpg files and put them in the corresponding `%localappdata%/Flashbook/books` folder. This folder can be opened in the menubar of the program.

You can take notes by simply selecting an area with your mouse, a rectangle will be drawn, you can do this multiple times and they will be combined to a single question or answer card. In addition to this you can type an additional question or answer in a textbox that will be combined with the selected areas. In this textbox you can include regular text but also LaTeX code, e.g. `$\partial\beta$` to show `∂β`. In addition you can also add LaTeX macros so that you can almost ask any (mathematical) question.
### NB
- In the ‘files’ subfolder you can define your own LaTeX macros
-	LaTeX environments like matrices are not included

### TODO
- Perhaps use SQLite for data, currently everything is stored as .tex, .txt, .json files in %localappdata%. Although, now it is easy to alter questions by opening .tex files in Wordpad or TeXnicCenter.
- Add option to convert pdf to jpg files. This will speed up the syncing of books between devices.
- Customizable colors for Flashbook's 
- Clean up code: make it PEP-8 compliant, add clear docstrings to the functions.

# The program explained

The program will open with the following menu, allowing you to chose between one of the programs. You can always return to this menu once you opened one of the programs.

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/main1.png)
## Flashbook
![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb.png)

Open a book by pressing on the `browse` button. You can then create your own Q&A cards by selecting areas with you mouse. It will draw a box around your selection. Which can easily be undone by clicking your right mouse button.

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb_selection.png)

Once you entered your selection a pop up window will appear, showing you your selection. The pop up will disappear once you move with your cursor over it.

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb_selection_entered.png)

You can also create a 'mozaic' by simply clicking on the arrow at the bottom of the page. The direction the arrow is pointing is the direction in which the notes are stitched together. Mind you, not all in the same direction. When the arrow points down it just goes to a new 'row'.

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb_selection_entered2.png)

There doesn't have to be an answer card, for example when you just want to take notes. In that case once you entered your 'selection' or lack thereof, it will be made permanent. The borders will now be colored black.

It is also possible to enter LaTeX code ![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb_latex.png) 

which will be displayed as 

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb_latex2.png)

It's even possible to add your own LaTeX macros so that you can avoid typing long sequences of code.

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb_latex3.png)

will then give you:

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/fb_latex4.png)

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

You can also sync two devices. It will automatically display the IP address of the device the app is running on. Then you only need to add the other device's IP address. Right now it can only be used on a local wifi network. Synching books is optional as it can be a very slow process since it needs to transfer hundreds of jpg files. I plan to add a PDF -> jpg converter so that this transfer will be much faster. (laptop <-> PC is not a commutative process one direction may take 45 minutes while the other only takes 3 minutes)

![alt text](https://github.com/AntondeGroot/Flashbook/blob/master/readme%20images/sync.png)
