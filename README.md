# MicrobitProjects
## Table of contents:
* [installation](#installation)
* [setup](#setup)
* [modules used](#modules-used)
* [Files](Files)
* [What does it do](#What-does-it-do)
* [Contributor](#Contributor)

## installation:
* To be able to view it is enough to have the notepad, better [Visual Studio Code](https://code.visualstudio.com/Download).
* to run the program and play [python 3.10](https://www.python.org/)

## setup:
- Computer
- [Microbit](https://www.microbit.org/) 

Instead, to run the code, you need to install Python [3.10](https://www.python.org/downloads/)
## modules used:
* socket
* os
* time
* pygame
* sys
* serial
* serial.tools.list_ports
* Thread
* tkinter
* webbrowser

All modules can be downloaded via the following command, enter the command on a shell (linux) or command prompt (Windows)
command: **"pip install name"**, substitute the module name for "name"

## Files:
* [TicTacToeServer](https://github.com/Bosticardo-Andrea/Microbit-Project/blob/main/TicTacToeServer.py) --> game server, must be started before the client, you must enter the name in the client box first
* [TicTacToeClient](https://github.com/Bosticardo-Andrea/Microbit-Project/blob/main/TicTacToeClient.py) --> game client, it must be started after the server, it must send the name after the server has done it
* [main](https://github.com/Bosticardo-Andrea/Microbit-Project) --> main of the Microbit, use [Thonny](https://thonny.org/) or flash the code from this [site](https://python.microbit.org/v/2)
## What does it do:
This project is a microbit-controlled Tris.
Sockets are used to enable the server and client to communicate.
The threads are used to be able to constantly read the data obtained from the serial, sent by the microbit, and for the tkinter window.
To move inside the field you have to press the A (down), B (right) keys, while moving it you place the token.
to run the code you must be on the Wifi network, moreover, you need to know your IP, (if you don't know how to do it click here) and change these lines:
- [client](https://github.com/Bosticardo-Andrea/Microbit-Project/blob/main/TicTacToeClient.py): line 163 add to it with: "s.connect ((" Your IP ", 8000))"
- [server](https://github.com/Bosticardo-Andrea/Microbit-Project/blob/main/TicTacToeServer.py): line 159 substituted with: "s.connect ((" Your IP ", 8000))"

## Contributor:
@[DavideRebuffo](https://github.com/DavideRebuffo)
