# Devnet UI automation

## Requirements
- Python3.x or more: https://www.python.org/downloads/
- Ncclient library: https://github.com/ncclient/ncclient
- Pygubu library: https://github.com/alejandroautalan/pygubu
- Jinja2 library: https://palletsprojects.com/p/jinja/
- Lxml library: https://lxml.de/installation.html

## What is this
This is basically an application made as a final project to configure devnet-sandbox routers using ncclient, jinja and tkinter.

## How it works
Making use of ncclient and jinja templates to load xml files of configuration to devnet-sandbox routers, the application is now able to load interfaces configuration, hostname changes, motd banner and also making an xml file of all the router configuration.

## Installation
To install search by last release, to execute from source code;
```
git clone https://github.com/Godkayaki/Router-devnet-config/tree/main#readme
cd Router-devnet-config/src
python3 main.py
```
