# talonvoice-scripts

Scripts and helpers for use with Talon.

For the most part, these Scripts are named according to the application they directly interface with. Other, more general scripts, may be universally applicable.


## Installation

Copy a Script with the desired functionality into the `~/.talon/user` directory.

This can be done with a single command:

```
cd ~/.talon/user; curl -O "https://raw.githubusercontent.com/dwighthouse/talonvoice-scripts/master/SCRIPT.py"
```

Where `SCRIPT.py` is the name of the desired Script.

Talon (if running), will immediately detect the addition (or change) and adjust its internal list of available commands with the new content.

> **Warning:** If a Script contains a conflicting command, the command in the Script saved or created most recently will take precedence.


## Utilities

Some Scripts make use of utility files that most also be downloaded. Any Script that requires a utility file will import from `user`. For example:

```
from user import utils
```

A Script with the above will require the `utils.py` file to placed along side that Script in the `~/.talon/user` directory.


## Default Scripts

It is recommended that these Scripts be used in conjunction with `std.py`, at minimum. It provides the basic alphabet, common symbols, and some simple commands that are useful in many different contexts. `std.py` and other default scripts can be found at the [official user scripts example repository](https://github.com/talonvoice/examples).