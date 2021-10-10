# Merge QA PDF files in to a book

This project will merge multiple QA documents into one PDF file, and each QA document consists of two PDF files (Q and A respectiely). 

In the outcome PDF file, each QA session will take place staring on the even number page, and one blank page will be inserted into the document when necessary. 

The program is implemented using Python 3, and it is required to install PyPDF2 and reportlab packages to run this program.

```
sudo pip3 install PyPDF2 reportlab
```


The usage of the program is described as follows.

```
usage: pdf-merger.py [-h] [-Q Q_FOLDER] [-A A_FOLDER] [-o FILE] input_filename

positional arguments:
  input_filename        the lookup table to merge PDF files

optional arguments:
  -h, --help            show this help message and exit
  -Q Q_FOLDER, --Q_Folder Q_FOLDER
                        folder to store Questions, default= ./PDF-Q/
  -A A_FOLDER, --A_Folder A_FOLDER
                        folder to store Answers, default= ./PDF-A/
  -o FILE, --output FILE
                        write merged PDF to FILE, default=output.pdf
```
