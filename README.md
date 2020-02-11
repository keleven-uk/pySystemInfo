Print Hardware and System Information in Python

Inspired by https://www.thepythoncode.com/article/get-hardware-system-information-python


usage: pySystemInfo.py [-h] [-a] [-p] [-b] [-c] [-m] [-d] [-n] [-v] [-l]

System and hardware Information from Python.
-----------------------
Prints a lot of stuff about the Platform, CPU and Network.

optional arguments:
  -h, --help      show this help message and exit
  -a, --all       Print All the Info.
  -p, --platform  Print the Platform Info.
  -b, --bootTime  Print the Boot Time.
  -c, --cpu       Print the CPU Info.
  -m, --memory    Print the Memory Info.
  -d, --disk      Print the Disk Info.
  -n, --network   Print the NetWork Info.
  -v, --version   show program's version number and exit
  -l, --license   Print the Software License.

 If no arguments are given, a Menu will be displayed.

        Kevin Scott (C) 2020


PySystemInfo 1.2.0   Copyright (C) 2020  Kevin Scott
This program comes with ABSOLUTELY NO WARRANTY; for details type `PySystemInfo -l''.
This is free software, and you are welcome to redistribute it under certain conditions.


Please select one of the following:
1. Platform
2. Boot Time
3. CPU
4. Memory
5. Disk
6. Network
7. All
8. Quit


History
-------

1.0.0   27 January  2020  Basic program, All seems to be working.
1.1.0   28 January  2020  Added command arguments
1.2.0   28 January  2020  If no arguments are supplied, a menu is displayed.
1.2.1   10 February 2020  Added IP Adress & MAC Address to Platform Info.
1.3.0   10 February 2020  Started to move the information gathering to a seperate class / file.
1.3.1   11 February 2020  Moved the remaining items across [Disk & Network].

