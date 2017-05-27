from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import *
import plugin.databaseConn as database
import plugin.gradeData as grade


class QTableWidgetDisabledItem(QItemDelegate):
    """
    Create a readOnly QTableWidgetItem
    """
    def __init__(self, parent):

        QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        item = QLineEdit(parent)
        item.setReadOnly(True)
        #item.setEnabled(False)
        return item

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        editor.setText(index.model().data(index))
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())

class addGradeAdmin(QMainWindow):
    def __init__(self, courseData, parent = None):
        QMainWindow.__init__(self,None)
        self.setMinimumSize(622,651)
        self.setWindowTitle("Select Course")
        self.parent = parent
        self.courseData = courseData
        self.UIinit()

    def UIinit(self):
        loader = QUiLoader()
        form = loader.load("resources/UI/addGrade.ui",None)
        self.setCentralWidget(form)


        #page properties
        self.grade_table = form.findChild(QTableWidget,"addGradeTable")
        self.save_button = form.findChild(QPushButton,"saveButton")
        self.back_button = form.findChild(QPushButton,"backButton")
        self.import_button = form.findChild(QPushButton,"importButton")
        self.export_button = form.findChild(QPushButton,"exportButton")
        self.courseName = form.findChild(QLabel, "courseName")
        self.courseID = form.findChild(QLabel, "courseID")


        self.header = self.grade_table.horizontalHeader()
        self.header.setResizeMode(0,QHeaderView.ResizeToContents)
        self.header.setResizeMode(1,QHeaderView.Stretch)
        self.header.setResizeMode(2,QHeaderView.ResizeToContents)

        self.grade_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.grade_table.setSelectionMode(QAbstractItemView.SingleSelection)

        self.size = QTableWidgetDisabledItem(self.grade_table)
        self.grade_table.setItemDelegateForColumn(0,self.size)
        self.grade_table.setItemDelegateForColumn(1,self.size)

        #Internal Button Pressed
        self.save_button.clicked.connect(self.saveData)
        self.back_button.clicked.connect(self.backPage)
        self.import_button.clicked.connect(self.importFile)
        self.export_button.clicked.connect(self.exportFile)

    def updatePage(self):
        self.courseName.setText(self.courseData.getCourseName())
        self.courseID.setText(self.courseData.getCourseID())
        db = database.databaseGrade()
        temp = db.getAllUserCourse(self.courseData.getCourseID())
        grades = self.createBulk(temp)
        id = db.getUserData(temp)
        print(temp)
        print(id)
        self.grade_table.setRowCount(len(grades))
        i = 0
        for items in grades:
            self.grade_table.setItem(i,0,QTableWidgetItem(items.getUserID()))
            self.grade_table.setItem(i,1,QTableWidgetItem(id[items.getUserID()]))
            self.grade_table.setItem(i,2,QTableWidgetItem(items.getGrade()))
            i = i + 1

    def importFile(self):
        pass

    def exportFile(self):
        pass

    def saveData(self):
        pass

    def backPage(self):
        self.close()

    def createBulk(self, data):
        temp = []
        for i in data:
            temp.append(grade.gradeData(i, self.courseData))
        return temp



    
