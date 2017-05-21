from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import *


class editProfileUI(QMainWindow):
    def __init__(self,parent = None):
        QMainWindow.__init__(self,None)
        self.setMinimumSize(900,600)
        self.setWindowTitle("Edit_Profile")
        self.parent = parent
        self.UIinit()

    def UIinit(self):
        loader = QUiLoader()
        form = loader.load("resources/UI/editProfileStudent.ui",None)
        self.setCentralWidget(form)

        #QPushButton
        self.confirm_button = form.findChild(QPushButton,"confirmButton")
        self.cancel_button = form.findChild(QPushButton,"cancelButton")
        self.upload_button = form.findChild(QPushButton,"uploadButton")

        #LineEdit
        self.address_edit = form.findChild(QLineEdit,"addressEdit")
        self.email_edit = form.findChild(QLineEdit,"emailEdit")

        #Connect
        self.confirm_button.clicked.connect(self.editSuccess)
        self.cancel_button.clicked.connect(self.cancel)

    def cancel(self):
        pass

    def editSuccess(self):
        pass
        

    
    

    
        
    