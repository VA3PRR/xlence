# XLenCe
A browser-based scoring tool for training exercises using the Winlink email application.
The tool is intended to provide a simple interface for creating, managing, and scoring training exercises.
### Designed for WinlinkTraining.ca by VA3PRR

## Requires
This tool requires python3, as well as the following modules:
 + venv
   + flask
   + bs4
   + lxml

## Running the tool
The following commands assume you are in the directory containing `main.py`

**These steps must be completed before running the program for the first time**

1 enter `python3 -m venv venv`

2 enter `. venv/bin/activate`

3 enter `pip install` `flask` `bs4` `lxml`

4 enter `python3 main.py`

5 visit `http://localhost:5000` in your browser

**After the first time, only the following steps are needed**
1 enter `. venv/bin/activate`

2 enter `python3 main.py`

3 visit `http://localhost:5000` in your browser

Simplifying this process is a development goal.

## Notes
 + Only known to work on Debian Buster and Firefox
 + Requires organization
 + Barely functional
 + Currently packaged with standard form templates, but no mechanism exists to update them
   + standard templates add hundreds of files to the project, many are likely unnecessary
   + Most templates *appear* to work, but most haven't been tested
 + See issues #1 and #2 for further details
 
