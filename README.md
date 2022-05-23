# MicrobitProjects
## Table of contents:
* [installation](#installation)
* [setup](#setup)
* [modules used](#modules-used)
* [Files](Files)
* [What does it do](#What-does-it-do)
* [Contributor](#Contributor)

## installation:
To be able to view it is enough to have the notepad, better [Visual Studio Code](https://code.visualstudio.com/Download).

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

All modules can be downloaded via the following command, enter the command on a shell (linux) or command prompt (Windows)
command: **"pip install name"**, substitute the module name for "name"

## Files:
* [TicTacToeServer]() --> game server, must be started before the client, you must enter the name in the client box first
* [TicTacToeClient]() --> game client, it must be started after the server, it must send the name after the server has done it
* [main]() --> main of the Microbit, use [Thonny](https://thonny.org/) or flash the code from this [site](https://python.microbit.org/v/2)
## What does it do:
This project is a microbit-controlled Tris.
Sockets are used to enable the server and client to communicate.
The threads are used to be able to constantly read the data obtained from the serial, sent by the microbit, and for the tkinter window.
To move inside the field you have to press the A (down), B (right) keys, while moving it you place the token.

## Contributor:
@[DavideRebuffo](https://github.com/DavideRebuffo)
