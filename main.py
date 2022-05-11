#Amasa, Sophia Nicolette C.
#2020-0424
#CCC151 CS2
#Simple Student Information System

import sys
import csv
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QPushButton, QTextEdit, QLabel, QComboBox, QMessageBox
import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd="Sophr@@t1",
    database =  'students'
    )

data = []
info = []
header = []
mycursor = mydb.cursor()
        
def search(info): #Function for searching
    sqlSearch = "SELECT * FROM students WHERE %s in (student_id, full_name)"
    mycursor.execute(sqlSearch, (info, ))
    myresult = mycursor.fetchall()
    for result in myresult:
        data.append(result)

class MainWindow(QMainWindow): #UI for Main Window
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("mainWindow.ui", self)

        self.idTextEdit = self.findChild(QTextEdit, "textEdit")
        
        self.searchButton = self.findChild(QPushButton, "pushButton")
        self.searchButton.clicked.connect(self.searchStudent)
        
        self.editButton = self.findChild(QPushButton, "pushButton_2")
        self.editButton.clicked.connect(self.editStudent)
        
        self.deleteButton = self.findChild(QPushButton, "pushButton_3")
        self.deleteButton.clicked.connect(self.deleteStudent)
        
        self.addButton = self.findChild(QPushButton, "pushButton_4")
        self.addButton.clicked.connect(self.gotoAddStudentScreen)

        self.clearButton = self.findChild(QPushButton, "pushButton_5")
        self.clearButton.clicked.connect(self.clearStudents)

        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        self.tableWidget.selectionModel().selectionChanged.connect(self.on_selectionChanged)
        self.allStudents()

    def gotoAddStudentScreen(self):
        widget.setCurrentIndex(widget.currentIndex()+1)

    def clearStudents(self): #Function to clear search box
        self.idTextEdit.setPlainText("")
        self.allStudents()
        
    def display(self, row, student): #Function to display
        self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(student[0]))
        self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(student[1]))
        course = self.codeToName(student[2])
        self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(course))
        self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(student[3])))  
        self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(student[4]))
        
    def on_selectionChanged(self, selected, deselected): #Function for getting item when clicked
        for ix in selected.indexes():
            if info:
                info.remove(info[0])
            it = self.tableWidget.item(ix.row(), ix.column())
            self.it_text = it.text()
            info.append(search(self.it_text))

    def Popup(self, text): #Function to open Pop-up
        self.showPopup = PopupWindow()
        self.showPopup.label.setText(text)
        self.showPopup.show()
        
    def allStudents(self): #Function to display all students on table
        mycursor.execute("SELECT * FROM students")
        data = mycursor.fetchall()
        row=0
        self.tableWidget.setRowCount(len(data))
        for student in data:
            self.display(row, student)
            row=row+1
            
    def codeToName(self, course_code): #Function to display corresponding name of course
        sql = "SELECT * FROM course_info WHERE course_code = %s"
        mycursor.execute(sql, (course_code, ))
        myresult = mycursor.fetchall()
        for code in myresult:
            course = code
        return course[1]
    
    def editStudent(self): #Function for editing students
        addStudent.addPlainText()
        addStudent.correct = True
        addStudent.edit = True
        
        widget.setCurrentIndex(widget.currentIndex()+1)
            
    def searchStudent(self): #Function for searching students
        info = self.idTextEdit.toPlainText()
        search(info)
        sublist = data[0]
        if sublist is None:
            self.Popup('Student not Found')
        else:
            self.display(0, sublist)
            self.tableWidget.setRowCount(1)
        data.remove(sublist)

    def deleteStudent(self): #Function for deleting students
        stud_list = data[0]
        sqlDelete = "DELETE FROM students WHERE student_id = %s"
        mycursor.execute(sqlDelete, (stud_list[0], ))
        mydb.commit()
        self.allStudents()
        self.Popup('Student Deleted')

class addStudentScreen(QDialog): #UI for the screen for adding students
    def __init__(self):
        super(addStudentScreen, self).__init__()
        loadUi("addStudent.ui", self)
        
        self.idYearTextEdit = self.findChild(QTextEdit, "textEdit")
        self.idNumTextEdit = self.findChild(QTextEdit, "textEdit_2")
        self.nameTextEdit = self.findChild(QTextEdit, "textEdit_3")
        self.courseComboBox = self.findChild(QComboBox, "comboBox_3")
        self.yearComboBox = self.findChild(QComboBox, "comboBox_2")
        self.genderComboBox = self.findChild(QComboBox, "comboBox")
        
        self.addButton = self.findChild(QPushButton, "pushButton")
        self.xButton = self.findChild(QPushButton, "pushButton_2")

        self.correct = True
        self.edit = False

        self.addButton.clicked.connect(self.addStudent)
        self.xButton.clicked.connect(self.mainMenu)
    
    def Popup(self, text): #Function to open Pop-up
        self.showPopup = PopupWindow()
        self.showPopup.label.setText(text)
        self.showPopup.show()
        
    def addPlainText(self): #Function for inserting data to screen
        self.stud_list = data[0]
        self.idYearTextEdit.setPlainText(self.stud_list[0][0:4])
        self.idNumTextEdit.setPlainText(self.stud_list[0][5:])
        self.nameTextEdit.setPlainText(self.stud_list[1])
        self.courseComboBox.setCurrentText(self.stud_list[2])
        self.yearComboBox.setCurrentText(str(self.stud_list[3]))
        self.genderComboBox.setCurrentText(self.stud_list[4])
        
    def addStudent(self): #Function for adding students
        student_info = []
        
        while self.correct:
            id_year = self.idYearTextEdit.toPlainText()
            id_num = self.idNumTextEdit.toPlainText()
            try:
                int_year = int(id_year)
                int_num = int(id_num)
            except:
                self.Popup('Enter a Number')
                break
            student_id = str(id_year + '-' + id_num)
            student_info.append(student_id)

            name = self.nameTextEdit.toPlainText()
            student_info.append(name)

            course = self.courseComboBox.currentText()
            student_info.append(course)

            year_level = self.yearComboBox.currentText()
            student_info.append(year_level)

            gender = self.genderComboBox.currentText()
            student_info.append(gender)
        
            self.idYearTextEdit.setPlainText("")
            self.idNumTextEdit.setPlainText("")
            self.nameTextEdit.setPlainText("")

            print(student_info)
            if self.edit:
                student_info.append(self.stud_list[0])
                sqlEdit = "UPDATE students SET student_id = %s, full_name = %s, course_code = %s, year_level = %s, gender = %s where student_id = %s"
                mycursor.execute(sqlEdit, student_info)
                mydb.commit()
                data.remove(self.stud_list)
                self.edit = False
            else:
                sqlInsert = "INSERT INTO students VALUES (%s, %s, %s, %s, %s)"
                mycursor.execute(sqlInsert, student_info)
                mydb.commit()
            
            self.correct = False
            self.Popup('Student Added')
            
    def mainMenu(self): #Function to go back to main menu
        if data:
            data.remove(data[0])
        mainwindow.allStudents()
        widget.setCurrentIndex(widget.currentIndex()-1)

class PopupWindow(QDialog): #UI for Pop-up
    def __init__(self):
        super(PopupWindow,self).__init__()
        loadUi("Popup.ui", self)
        
        self.label = self.findChild(QLabel, "label")

app = QApplication(sys.argv)
widget=QtWidgets.QStackedWidget()

mainwindow = MainWindow()
widget.addWidget(mainwindow)

addStudent = addStudentScreen()
widget.addWidget(addStudent)

widget.setFixedHeight(600)
widget.setFixedWidth(1000)
widget.show()

        
