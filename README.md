# DBSeeker

[![Built with Python3](https://img.shields.io/badge/built%20with-Python3-red.svg)](https://www.python.org/) [![PyPI version](https://badge.fury.io/py/dbseeker.svg)](https://badge.fury.io/py/dbseeker) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/dueclic/dbseeler/blob/master/LICENSE) ![Contributors](https://img.shields.io/github/contributors/dueclic/dbseeker)
## Description:

A little but functional script that let you search in several databases for an input string.
It will print the results in a table format, indicating wich table contains the search term, in wich database, how many rows were found and the time it took to search.

Please note that this project is still in alpha stage, so you may encounter bugs and missing features.
## Usage: 

DBSeeker uses argparse to parse  command line arguments.
You can run `python dbseeker.py -h` to see this help message:

```
usage: dbseeker.py [-h] -a address -P port -u user [-p password] [-d database | -bl blacklist] -s search


  -h, --help            
                        To show this help message and exit
  -a address, --address address
                        To Enter the host address
  -P port, --port port  
                        To Enter the port
  -u user, --user user  
                        To Enter the user
  -p password, --password password
                        To Enter the password
  -d database, --database database
                        To Enter databases you want to search in
  -bl blacklist, --blacklist blacklist
                        To Enter databases you want to be excluded, separated by commas
  -s search, --search search
                        To Enter the search term
```
Please note that `-d` and `-bl` are mutually exclusive;

Square brackets indicate _optional_ arguments;

At the moment DBSeeker will accept a minimum of 3 characters for the search term, but it may be changed in the future;

If your search string does include whitespaces, please remember to use quotes.

## Dependencies: ##

Since 'argparse' and 'time' should be both included in your python environment you just need to install the following dependencies:

- mysql-connector-python
- tabulate

as refered in the requirements.txt file.

## Contributors

As always, thanks to our amazing contributors!

<!--GAMFC_DELIMITER-->will be replaced here<!--GAMFC_DELIMITER-END-->

Made with [contributors](https://github.com/jaywcjlove/github-action-contributors).

## Installation:

Inside the project folder, create a new virtual environment, then simply run
```bash
pip install -r requirements.txt
```

Or you can simply run 

```bash
pip install dbseeker
```