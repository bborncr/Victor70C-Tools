# Victor 70C Digital Multimeter python tools

The application included with the Victor 70C Digital Multimeter (DMM) has many issues and it very outdated.
I figured that a set of python tools to read from the Victor 70C would be a fun project to learn python.

It would seem logical that someone using a DMM for testing might want to be able to create a simple script to link into a more comprehensive set of test procedures.

## Features

* Cross platform (should run on Linux, Mac, Windows)
* Save data to CSV file either continuously or via the space bar
* Plot the data in real time

## Victor 70C data protocol and structure

Probably the most important part of this code is the parsing of the Victor 70C data from the serial port.
The Victor 70C and some other DMMs with serial output use the FS9922-DMM4 integrated circuit.
The documentation for the data protocol and structure can be found here (PDF):
[FS9922-DMM4 Datasheet](https://www.ic-fortune.com/upload/Download/FS9922-DMM4-DS-13_EN.pdf)

The 'parse_victor70c.py' script takes in a line read from the Victor 70C and returns a dictionary with the sign values and units. I suspect that more experienced python programmers would just use this parser and create their own script to integrate the results into their workflow.

## USAGE

