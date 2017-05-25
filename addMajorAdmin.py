from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import *
import plugin.databaseConn as database

class AddMajorUI(QMainWindow):
    def __init__(self,parent = None):
        QMainWindow.__init__(self,None)
        self.setMinimumSize(900,600)
        self.setWindowTitle("Profile")
        palette = QPalette()
        palette.setBrush(QPalette.Background,QBrush(QPixmap("resources/images/background.png")))
        self.setPalette(palette)
        self.bar = QPixmap("resources/images/bar.png")
        self.parent = parent
        self.UIinit()

    def UIinit(self):
        loader = QUiLoader()
        form = loader.load("resources/UI/addMajor.ui",None)
        self.setCentralWidget(form)

        #Upper Bar
        self.bar_group = form.findChild(QLabel,"barLabel_2")
        self.bar_group.setPixmap(self.bar)
        self.home_button = form.findChild(QPushButton,"homeButton")
        self.profile_button = form.findChild(QPushButton,"profileButton")
        self.grade_button = form.findChild(QPushButton,"gradeButton")
        self.course_button = form.findChild(QPushButton,"courseButton")
        self.other_button = form.findChild(QPushButton, "othersButton")

        #page properties
        self.majorTable = form.findChild(QTableWidget,"majorTable")
        self.faculty_id = form.findChild(QLineEdit,"facultyID")
        self.major_id = form.findChild(QLineEdit,"majorID")
        self.major_name = form.findChild(QLineEdit,"majorName")
        self.add_button = form.findChild(QPushButton,"addButton")
        self.search_button = form.findChild(QPushButton,"searchButton")
        self.add_button.setEnabled(False)

        self.header = self.majorTable.horizontalHeader()
        self.header.setResizeMode(0,QHeaderView.ResizeToContents)
        self.header.setResizeMode(1,QHeaderView.Stretch)

        self.majorTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.majorTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.majorTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


        #Upper Bar pressed
        self.home_button.clicked.connect(self.goHome)
        self.profile_button.clicked.connect(self.goProfile)
        self.grade_button.clicked.connect(self.goGrade)
        self.course_button.clicked.connect(self.goCourse)
        self.other_button.clicked.connect(self.goTemp)
        self.home_button.clicked.connect(self.goHome)

        self.add_button.clicked.connect(self.add)
        self.search_button.clicked.connect(self.searchMajor)

        self.db = database.databaseAdmin()

    def goHome(self):
        self.parent.changePageLoginSection("home")

    def goProfile(self):
        self.parent.changePageLoginSection("profile")

    def goGrade(self):
        self.parent.changePageLoginSection("grade")

    def goCourse(self):
        self.parent.changePageLoginSection("course")

    def goTemp(self):
        self.parent.changePageLoginSection("addcourse")

    def add(self):
        temp = self.db.addMajors(self.faculty_id.text(), self.major_id.text(), self.major_name.text())
        if(temp == 1):
            self.searchMajor()
            self.parent.showOK("Major Added", "Major " + self.major_name + " has been added to the system.")
        elif(temp == "DUPLICATE"):
            self.parent.showERROR("Major ID Duplication Error", "The ID you entered already exists. Please Try Again.")

    def searchMajor(self):
        data = self.db.getallMajors(self.faculty_id.text())
        if(len(data[0]) > 0):
            self.add_button.setEnabled(True)
            self.majorTable.setRowCount(len(data[0]))
            for i in range(0, len(data[0])):
                self.majorTable.setItem(i, 0, QTableWidgetItem(data[0][i].majorID))
                self.majorTable.setItem(i, 1, QTableWidgetItem(data[0][i].degree))
                self.majorTable.setItem(i, 2, QTableWidgetItem(str(data[1][i])))
        else:
            self.add_button.setEnabled(False)