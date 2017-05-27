from loginForm import *
from mainForm import *
from pwForm import *
from profileForm import *
from studentCourseForm import *
from adminSelectCourse import *
from addMajorAdmin import *
from addFacultyAdmin import *
from viewGradeForm import *
from addCourseForm import *
from seeCourseProf import *
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import *


import sys

class GUImanager(QMainWindow):
    def __init__(self):
        self.user = None
        # Main UI set up
        QMainWindow.__init__(self, None)
        self.setMinimumSize(900, 600)
        self.setFixedSize(900,600)
        self.setWindowTitle("G-Man version 0.7.9 (Alpha)")
        
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("resources/images/background.png")))
        self.setPalette(palette)

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.login_widget = LoginUI(self)
        self.main_widget = mainUI(self)
        self.pw_widget = pwUI(self)
        self.add_major_for_admin_widget = AddMajorUI(self)
        self.view_grade_widget = viewGradeUI(self)
        self.addCourse_widget = addCourseUI(self)
        self.student_course_widget = StudentCourseUI(self)
        self.add_faculties_for_admin = AddFacultyUI(self)
        self.profile_widget = profileUI(self)
        self.select_course = selectCourseUI(self)
        self.see_course_widget = seeCourseProfUI(self)

        
        self.central_widget.addWidget(self.login_widget)
        self.central_widget.addWidget(self.view_grade_widget)
        self.central_widget.addWidget(self.profile_widget)
        self.central_widget.addWidget(self.main_widget)
        self.central_widget.addWidget(self.student_course_widget)
        self.central_widget.addWidget(self.pw_widget)
        self.central_widget.addWidget(self.addCourse_widget)
        self.central_widget.addWidget(self.profile_widget)
        self.central_widget.addWidget(self.add_major_for_admin_widget)
        self.central_widget.addWidget(self.select_course)
        self.central_widget.addWidget(self.add_faculties_for_admin)
        self.central_widget.addWidget(self.see_course_widget)


    def changePageLoginSection(self,signal = None):
        if signal == "login":
            print("login")
            self.centralWidget().setCurrentWidget(self.login_widget)

        if signal == "forget":
            print("forget")
            self.centralWidget().setCurrentWidget(self.pw_widget)

        if signal == "home":
            print("home")
            self.centralWidget().setCurrentWidget(self.main_widget)
############################################## STUDENT signal ################################################ 
        if signal == "profile":
            print("profile")
            self.centralWidget().setCurrentWidget(self.profile_widget)
            self.profile_widget.updatePage()

        if signal == "studentGrade":
            print("studentGrade")
            self.centralWidget().setCurrentWidget(self.view_grade_widget)

        if signal == "studentCourse":
            print("studentCourse")
            self.centralWidget().setCurrentWidget(self.student_course_widget)

        if signal == "studentGrade":
            print("studentGrade")
            self.centralWidget().setCurrentWidget(self.view_grade_widget)
############################################## Prof signal ################################################ 
        if signal == "grade":
            print("grade")
            self.centralWidget().setCurrentWidget(self.select_course)
            #self.centralWidget().setCurrentWidget(self.view_grade_widget)
            #self.view_grade_widget.updatePage()

        if signal == "course":
            print("course")
            self.centralWidget().setCurrentWidget(self.see_course_widget)

############################################## Admin signal ################################################ 

        if signal == "addcourse":
            print("addcourse")
            self.centralWidget().setCurrentWidget(self.addCourse_widget)

        if signal == "addfaculties":
            print("addfaculties")
            self.centralWidget().setCurrentWidget(self.add_faculties_for_admin)
            self.add_faculties_for_admin.updatePage()
            
        if signal == "addmajor":
            print("addmajor")
            self.centralWidget().setCurrentWidget(self.add_major_for_admin_widget)
        

    def setCurrentUser(self, user):
        self.user = user
        
    def getCurrentUser(self):
        return self.user

    ##MessageDialogs
    def showOK(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        ret_val = msg.exec_()
        if (ret_val == QMessageBox.Ok):
            print("MessageBox Clicked:", ret_val)

    def showCONFIRM(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        ret_val = msg.exec_()
        if (ret_val == QMessageBox.Ok):
            print("MessageBox Clicked:", ret_val)
            return True
        else:
            return False

    def showERROR(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        ret_val = msg.exec_()
        if (ret_val == QMessageBox.Ok):
            print("MessageBox Clicked:", ret_val)
def main():
    app = QApplication(sys.argv)
    ui = GUImanager()
    ui.show()
    app.exec_()

if __name__ == "__main__":
    main()

        
