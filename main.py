import io
import os
from rembg import remove
from PIL import Image
from pathlib import Path
import PySimpleGUI as sg

file_types = [
    ("All files (*.*)", "*.*")
]

layout = [
    [
        sg.Text("Image File"),
        sg.Input(size=(25, 1), key="-FILE-"),
        sg.FileBrowse(file_types=file_types),
        sg.Button("Convert"),
    ],

    [
        sg.Text("New image location"),
        sg.Input(size=(25, 1), key="-NEWLOCATION-"),
        sg.FolderBrowse(),
    ],

    [
        sg.Text("Make sure <filename>.png is behind the folder location."),
    ],

    [
        sg.Text("Default location at output/output.png")
    ],

    [
        sg.Image(key="-IMAGE-"),
        sg.Image(key="-IMAGEREMOVED-")
    ],

    [sg.Text(key="-FILENAME-")],
    [sg.Text(key="-NEWLOCATIONNAME-")],

]

window = sg.Window("Image background remover", layout, size=(900, 450))

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == "Convert":
        filename = values["-FILE-"]
        foldername = values["-NEWLOCATION-"]
        if os.path.exists(filename):
            image = Image.open(filename)
            image.thumbnail((400, 400))
            bio = io.BytesIO()
            image.save(bio, format="PNG")
            window["-IMAGE-"].update(data=bio.getvalue())

            window["-FILENAME-"].update("Input path: " + filename)

            if foldername != "":
                # Ensure the output path ends with a slash
                if not foldername.endswith(os.sep):
                    foldername += os.sep
                # Construct the output file name
                output_filename = os.path.basename(filename).rsplit('.', 1)[0] + ".png"
                output_path = foldername + output_filename
            else:
                output_path = "output/output.png"

            inputForProgram = Image.open(filename)
            output = remove(inputForProgram)
            output.save(output_path)

            imageOutput = Image.open(output_path)
            imageOutput.thumbnail((400, 400))
            bioOutput = io.BytesIO()
            imageOutput.save(bioOutput, format="PNG")
            window["-IMAGEREMOVED-"].update(bioOutput.getvalue())
            window["-NEWLOCATIONNAME-"].update("Output path: " + output_path)

window.close()
