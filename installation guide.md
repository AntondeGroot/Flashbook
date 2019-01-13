# Minimum size executable using pyinstaller
When you use python from Anaconda the executable will be around 800MB

But if you use the instructions below it will be around 90MB in size.

basically: (in Windows)
- download the latest python.exe. Install and select 'Add Python to path'
- in cmd: `python -m venv flashbook-env` 
- then: `flashbook-env\Scripts\activate.bat`
- then use: `python -m pip install img2pdf matplotlib numpy pdf2image pillow pybase64 pypiwin32 termcolor wmi wxpython` to install all packages.

**NB:** for pdf2image you also need "Poppler for Windows" and add "\bin" as path variable.


documentation:

- [Stackoverflow: see Esperluette's answer to themself](https://stackoverflow.com/questions/48629486/how-can-i-create-the-minimum-size-executable-with-pyinstaller)
- [Python docs on venv](https://docs.python.org/3/tutorial/venv.html)
poppler:
- [https://stackoverflow.com/questions/1681208/python-platform-independent-way-to-modify-path-environment-variable](https://stackoverflow.com/questions/1681208/python-platform-independent-way-to-modify-path-environment-variable)
- [https://simply-python.com/tag/pdftoimage/](https://simply-python.com/tag/pdftoimage/)


## Installation

1. download all the files in the `files` folder
1. go in command prompt to the relevant folder
1. create a .spec file by typing: `pyi-makespec --noconsole flashbook.py --icon=book.ico`
4. run pyinstaller `pyinstaller flashbook.spec` 

--------------------------------
## Errors: 

1. if it gives any errors like: `"pyqt5 folder cannot be found"` then delete pyqt5 and install it again with `pip3 install pyqt5`

1. if the error reads: `"pyinstaller bincache may be corrupted"` then go to `%appdata%` and delete the entire pyinstaller folder and run pyinstaller again.
