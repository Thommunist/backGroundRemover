import io

from rembg import remove
from PIL import Image
from pathlib import Path, PureWindowsPath
import PySimpleGUI as sg
import os.path

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
        sg.Text("Default location at ouput/ouput.png")
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
            image = Image.open(values["-FILE-"])
            image.thumbnail((400, 400))
            bio = io.BytesIO()
            image.save(bio, format="PNG")
            window["-IMAGE-"].update(data=bio.getvalue())

            window["-FILENAME-"].update("Input path" + filename)

            input_path = Path(filename)

            if foldername != "":
                if not (".png" or ".PNG") in foldername:
                    output_path = "output/output.png"
                else:
                    output_path = foldername
            else:
                output_path = "output/output.png"

            inputForProgram = Image.open(input_path)
            output = remove(inputForProgram)
            output.save(output_path)

            imageOutput = Image.open(output_path)
            imageOutput.thumbnail((400, 400))
            bioOutput = io.BytesIO()
            imageOutput.save(bioOutput, format="PNG")
            window["-IMAGEREMOVED-"].update(bioOutput.getvalue())
            window["-NEWLOCATIONNAME-"].update("Output path: " + output_path)

window.close()
