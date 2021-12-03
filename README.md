# Task 

This is a task created by Kiwi as an entrence task for python weekend 
Assignment here: https://github.com/kiwicom/python-weekend-xmas-task



## Prerequisites
Python 3.8.+

## Install 
Uses only the standard libraries, no installs required.

## Solution
The idea is using Dijkstra's algorithm: find a route between two airports 
ordered by price of the ticket .

## Usage
```
$ python .\solution.py -h
usage: solution.py [-h] csv_file from_airport to_airport [bags]

Lists all flight combinations for a selected route between airports A ->
B, ordered by price

positional arguments:
  csv_file      CSV file.
  from_airport  from airport shortcut
  to_airport    to airport shortcut
  bags          number of bags allowed

optional arguments:
  -h, --help    show this help message and exit
```

Example usage:
```
python solution.py example0.csv WIW RFZ
```

Usage with bags set:
```
python solution.py example0.csv WIW RFZ 2
```

# CAVEAT: 
In case no airport combination is found, or bags argument is supplied with 
higher amount of bags than any flight allows, empty list is returned.






