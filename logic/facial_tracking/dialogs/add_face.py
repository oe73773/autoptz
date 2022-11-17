import os

import cv2
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog

from shared.message_prompts import show_critical_messagebox, show_info_messagebox

class AddFaceUI(object):
    def __init__(self):
        self.name_line = None
        self.horizontalLayout = None
        self.cancel_btn = None
        self.enter_name_btn = None
        self.camera = None
        self.add_face_title_label = None
        self.verticalLayout = None
        self.window = None
        self.count = 0

    def setupUi(self, add_face, camera):
        self.window = add_face
        self.camera = camera
        add_face.setObjectName("add_face")
        add_face.resize(150, 60)
        self.verticalLayout = QtWidgets.QVBoxLayout(add_face)
        self.verticalLayout.setObjectName("verticalLayout")
        self.add_face_title_label = QtWidgets.QLabel(add_face)
        self.add_face_title_label.setText("add_face_title")
        self.verticalLayout.addWidget(self.add_face_title_label)

        self.name_line = QtWidgets.QLineEdit(add_face)
        self.name_line.setObjectName("name_line")
        self.verticalLayout.addWidget(self.name_line)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.enter_name_btn = QtWidgets.QPushButton(add_face)
        self.enter_name_btn.setObjectName("enter_name_btn")
        self.enter_name_btn.clicked.connect(self.add_face_prompt)
        self.horizontalLayout.addWidget(self.enter_name_btn)

        self.cancel_btn = QtWidgets.QPushButton(add_face)
        self.cancel_btn.setObjectName("cancel_btn")
        self.cancel_btn.clicked.connect(self.window.close)
        self.horizontalLayout.addWidget(self.cancel_btn)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.translate_ui(add_face)
        QtCore.QMetaObject.connectSlotsByName(add_face)

    def add_face_prompt(self):
        print("Adding Face with " + self.camera.objectName())
        if self.name_line.text().strip() == "":
            return
        else:
            # check if path exists, if not create path for images to be stored
            path = '../logic/facial_tracking/images/' + self.name_line.text().strip()
            if os.path.exists(path):
                print("\n [INFO] Name Already Taken")
                show_critical_messagebox(window_title="Add Face Process", critical_message="User's Face Already Exists.\nPlease add another user.")
                return
            else:
                os.makedirs(path)
                print("\n [INFO] New Path Created")
                show_info_messagebox("Initializing face capture. \nLook at the select camera and wait...")
                print("\n [INFO] Initializing face capture. Look at the select camera and wait...")
                self.camera.image_processor_thread.config_add_face(name=self.name_line.text().strip())
                self.window.close()

    def translate_ui(self, add_face):
        _translate = QtCore.QCoreApplication.translate
        add_face.setWindowTitle(_translate("add_face", "Add Face"))
        self.add_face_title_label.setText(_translate("add_face_title", "Enter Name:"))
        self.enter_name_btn.setText(_translate("enter_name_btn", "Submit"))
        self.cancel_btn.setText(_translate("cancel_btn", "Cancel"))


class AddFaceDlg(QDialog):
    """Setup Add Face Dialog"""

    def __init__(self, parent=None, camera=None):
        super().__init__(parent)
        # Create an instance of the GUI
        self.ui = AddFaceUI()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self, camera=camera)