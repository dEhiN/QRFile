# A script to read in a file of the user's choosing and generate a QR code for that file

import os.path, sys, io
import pybase64, segno
import tkinter.filedialog as file_chooser, flask as fl, werkzeug.utils as wu

app = fl.Flask(__name__)

QR_SCALE = 3
QR_DARK = "#e4b5a2"
QR_DATA_DARK = "#40cbd4"
QR_LIGHT = "#16161e"
QR_DATA_LIGHT = "#d6d8df"
TEST_FILENAME = "README.md"


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
        file_name (str): The file to open as a string

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


def save_qr(qr_code: segno.QRCode):
    """Function to save the QR code as a file

    Args:
        qr_code (segno.QRCode): A QRCode object created by the module segno
    """
    qr_code.save(
        "static/file.png",
        scale=QR_SCALE,
        dark=QR_DARK,
        data_dark=QR_DATA_DARK,
        light=QR_LIGHT,
        data_light=QR_DATA_LIGHT,
    )


def generate_bytesio(qr_code: segno.QRCode):
    """Function to generate a BytesIO object from the QR code passed in

    Args:
        qr_code (segno.QRCode): A QRCode object created by the module segno

    Returns:
        io.BytesIO: The QR object saved into a IO stream using the BytesIO class
    """
    buffer = io.BytesIO()
    qr_code.save(
        buffer,
        kind="png",
        scale=QR_SCALE,
        dark=QR_DARK,
        data_dark=QR_DATA_DARK,
        light=QR_LIGHT,
        data_light=QR_DATA_LIGHT,
    )
    buffer.seek(0)
    return buffer


@app.route("/")
def route_home():
    return fl.render_template("index.html")


@app.route("/qr")
def route_qr():
    return fl.render_template("qr-code.html", qr=qr)


@app.route("/qr/upload", methods=["POST", "GET"])
def route_qr_user():
    if fl.request.method == "POST":
        form_file_name = "userfile"
        if form_file_name not in fl.request.files:
            return fl.redirect(fl.url_for("route_home"))

        user_file = fl.request.files["userfile"]
        usr_file_name = user_file.filename

        if usr_file_name == "":
            return fl.redirect(fl.url_for("route_home"))

        user_file.save(wu.secure_filename(usr_file_name))

    return fl.redirect("/qr")


@app.route("/qr/pretty")
def route_qr_pretty():
    return fl.render_template("qr-code-pretty.html", qr=fl.url_for("static", filename="file.png"))


@app.route("/save")
def route_save():
    return fl.send_file(
        fl.url_for("static", "file.png"),
        as_attachment=True,
        download_name="file.png",
        mimetype="image/png",
    )


if __name__ == "__main__":
    file_data = read_file(TEST_FILENAME)
    converted_data = encode_file(file_data)
    qr = create_qr(converted_data)
    save_qr(qr)
    app.run(debug=True)
