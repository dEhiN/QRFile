# Purpose
This is an attempt to use Python to generate a QR code that will allow one to download a file

# How it works
The idea is that the user is prompted to select a file using a standard file dialog box and that is converted to a QR code which can then be scanned. This would allow, for example, easy sharing of a file from a laptop to a phone.

Currently, the Python script uses the module `segno` to generate the QR code. The module `pybase64` is also used as an intermediary to convert the file data, once read in, to a base64 string using UTF-8 encoding.

# Current status
Date: 2024-12-01
After writing up the whole script and testing it, the QR code is properly generated. The script currently just shows the QR code but doesn't save it. However, when scanned, the QR code is just the base64 string in text format that can be copied.

# Next steps
Date: 2024-12-01
Will need to explore `segno` to see if it can directly generate a QR code for a file.
