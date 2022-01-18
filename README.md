# Task 

This is a task created by Kiwi as an entrence task for python weekend.  
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



## Version 
I created different solutions for the same task 

v1_solution_pandas.py -> my first and very simple code to set and test algorithm. Uses pandas for reading and sorting the input data.  Returns output flights visualized as flight table, easy to read for a human. 



v2_solution_csv.py -> this is the same solution as previous one, only without pandas, using csv library.  Returns output flights visualized as flight table, easy to read for a human.


v3_solution_json.py ->  solution sent to evaluation, since structure of code is finished to match all requirements. Uses dataclass to structure output flights as required json format. 
