# A script to read in a file of the user's choosing and generate a QR code for that file

import os.path
import tkinter.filedialog as file_chooser
import sys
import pybase64
import segno


def error_handling(e: Exception = None):
    """Function to handle all errors

    Args:
        e (Exception, optional): A specific error or exception that was caught. Defaults to None.
    """
    if e:
        print(e)
    else:
        print("There was a problem!")

    sys.exit()


def get_file():
    """Function to get the file that the user wants

    This function will use the Tkinter FileDialog option to have the user select a file

    Returns:
        str: The absolute path the to file
    """
    # Use the askopenfilename function to get the file and path using a standard file dialog window
    file_name = file_chooser.askopenfilename(title="Choose the file to use")

    # Convert Unix path separators
    win_file_name = file_name.replace("/", "\\")

    return str(win_file_name)


def read_file(file_name: str):
    """Function to read in a file

    This function will read in a file

    Args:
        file_name (str): The file to open as a string with the full absolute path

    Returns:
        bytes: A byte stream of the file that's been read in
    """
    # Check if the file exists
    if os.path.isfile(file_name):
        try:
            with open(file_name, "rb") as file_in:
                file_data = file_in.read()

                return file_data
        except Exception as error:
            error_handling(error)
    else:
        error_handling()


def encode_file(data: bytes):
    """Function to encode a byte stream to base64

    This function will convert a byte stream to base64 using UTF-8 encoding

    Args:
        data (bytes): The byte stream to convert

    Returns:
        str: The converted base64 string in UTF-8
    """
    if data:
        converted_data = pybase64.b64encode(data)
        encoded_data = converted_data.decode("utf-8")

        return encoded_data
    else:
        error_handling()


def create_qr(b64_str: str):
    """Function to create a QR code

    Args:
        b64_str (str): A string in base64

    Returns:
        QRCode: An object of the QRCode class with the generated QR code
    """
    qr_code = segno.make_qr(b64_str)

    return qr_code


if __name__ == "__main__":
    file = get_file()
    print(file)

    input("Press enter key to continue...")

    read_data = read_file(file)
    print(f"\n{read_data}")

    input("Press enter key to continue...")

    converted_data = encode_file(read_data)
    print(f"\n{converted_data}")

    input("Press enter key to continue...")

    qr = create_qr(converted_data)
    print(f"\n{qr.show()}")
