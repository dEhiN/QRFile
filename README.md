# Purpose
This is an attempt to use Python to generate a QR code that will allow one to download a file

# How it works
The idea is that the user is prompted to select a file using a standard file dialog box and that is converted to a QR code which can then be scanned. This would allow, for example, easy sharing of a file from a laptop to a phone.

Currently, the Python script uses the module `segno` to generate the QR code. The module `pybase64` is also used as an intermediary to convert the file data, once read in, to a base64 string using UTF-8 encoding.

# Current status
Date: 2024-12-01

After writing up the whole script and testing it, the QR code is properly generated. The script currently just shows the QR code but doesn't save it. However, when scanned, the QR code is just the base64 string in text format that can be copied.

Explored `segno` and while it has a byte mode, the QR code it generates would never be able to "hold" a file. Checked out a QR code file generator online and it works by uploading the file, then generating a QR code containing a link to the file.

While continuing to explore, started reading more of the `segno` documentation where they demonstrate how to use the module in a web development setting using _Flask_.

Started playing around with the idea of using _Flask_ to show the QR code based on the `segno` documentation examples.

Created a _Flask_ app with 3 views. The "starter code" - the code initially created to let the user choose a file, read it in, convert it to base64, and generate a QR code from it - still exists.

In the main `if` block, the _Flask_ app is run after the starter code. To distinguish the types of functions - those for the _Flask_ views and the others - the _Flask_ view ones start with `route_`.

# Next steps
Date: 2024-12-01

Keep playing around with Flask.
