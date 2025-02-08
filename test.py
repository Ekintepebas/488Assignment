
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import json
from camera import Camera


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


if __name__ == "__main__":
    t = read_json_file("scene.json")
    
    #print(t)
    p = QJsonDocument(t).toVariant()
    #q = QJsonArray(t)
    #m = Camera.from_json_document(p.get('camera'))
    print(p)

    print(p['camera'])
