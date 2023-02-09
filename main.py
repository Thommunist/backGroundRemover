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
    [sg.Image(key="-IMAGE-")],
    [sg.Image(key="-IMAGEREMOVED-")],
    [sg.Text(key="-FILENAME-")],
    [
        sg.Text("Image File"),
        sg.Input(size=(25, 1), key="-FILE-"),
        sg.FileBrowse(file_types=file_types),
        sg.Button("Load Image")
    ]
]

window = sg.Window("Image viewer", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "Load Image":
        filename = values["-FILE-"]
        if os.path.exists(filename):
            image = Image.open(values["-FILE-"])
            image.thumbnail((400, 400))
            bio = io.BytesIO()
            image.save(bio, format="PNG")
            window["-IMAGE-"].update(data=bio.getvalue())
            window["-FILENAME-"].update(filename)





window.close()

# input_path = Path("inputPhoto/konijn.png")
#             output_path = 'output'
#             inputForProgram = Image.open(input_path)
#             output = remove(inputForProgram)
#             output.save(output_path)
