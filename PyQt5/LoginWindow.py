from PyQt5.QtWidgets import QApplication,QVBoxLayout,QLineEdit,QPushButton,QDialog ## for all GUI components
import sys #for exit argument of application
import os 
from FirstCalc import MainApplication             ## main calculator Application 
from StyleSheet.StyleSheets import StyleSheets    ## for styling of GUI component
class LoginWindow(QDialog):
    def __init__(self,parent = None):
        super().__init__(parent)
        self.setWindowTitle("Login")             ##set the title of window
        self.VLayout = QVBoxLayout()             ##create vertical layout
        self.setLayout(self.VLayout)             ##set main layout of window
        self.currDir = os.path.dirname(__file__) ##store current directory of file 
        self.allwidget = {}          ## this dict hold the all UI object in the screen
        self.setUI()                 ## set all UI component to main window
        self.UserData = {}           ## hold the user name and password
        self.LoadUser()              ##Load User's name and password
    #### Function to open calculator main window when login button is clicked ###
    def openCalc(self):
        mainapp = MainApplication()
        mainapp.show()
        self.close()
    ### function to check the username and password is correct or not ###
    def LoginClicked(self):
        self.allwidget['userent'].setStyleSheet(StyleSheets.EntryStyleSheet())
        self.allwidget['passwent'].setStyleSheet(StyleSheets.EntryStyleSheet())
        username = self.allwidget["userent"].displayText()  ## get the username enter by user 
        password = self.allwidget["passwent"].text()        ## get the password enter bu user
        if self.UserData["username"] == username:           ## check if the user name is correct or not
            if self.UserData["password"] == password:       ## check if the password is correct or not
                self.openCalc()                             ## if password and usename is correct open the calculator
            else:                                           ## if password is wronge set red background
                self.allwidget["passwent"].setStyleSheet(StyleSheets.WrongEntryStyleSheet())    
        else:                                               ## if username is wronge set red background
            self.allwidget["userent"].setStyleSheet(StyleSheets.WrongEntryStyleSheet())

    ### function to create Login button  ###
    def LoginButton(self):
        loginbtn = QPushButton("Login")                             ##create login button instance
        loginbtn.setStyleSheet(StyleSheets.LoginButtonStyleSheet()) ##set style to login button
        loginbtn.clicked.connect(self.LoginClicked)                 ##bind callback funcion to button when it clicked
        self.allwidget["loginbutton"] = loginbtn                    ## save the button instance to dictonary
        return loginbtn                                             ## return the instance from function
    ### function to create username field ###
    def userEntry(self):
        userent = QLineEdit("")                              ## create instance of entry field
        userent.setPlaceholderText("User name")              ## set placeholder to field
        userent.setStyleSheet(StyleSheets.EntryStyleSheet()) ## set style to field
        self.allwidget["userent"] = userent                  ## save the entry field to dictonary
        return userent                                       ## return the instance from function
    ### function to create password field ###
    def passwordEntry(self):
        passw = QLineEdit("")                                ## create instance of entry field
        passw.setPlaceholderText("Password")                 ## set placeholder to field
        passw.setEchoMode(QLineEdit.Password)                ## set the text should displayed in password formate
        passw.setStyleSheet(StyleSheets.EntryStyleSheet())   ## set style to field
        self.allwidget["passwent"] = passw                   ## save the entry field to dictonary
        return passw                                         ## return the instance from function
    ### Set all buttons and entry field to the login window ###
    def setUI(self):
        self.VLayout.addWidget(self.userEntry())             ## set username entry field in vertical layout
        self.VLayout.addWidget(self.passwordEntry())         ## set password entry field in vertical layout
        self.VLayout.addWidget(self.LoginButton())           ## set login button in vertical layout
    ### Load user name and password in the program from external file ###
    def LoadUser(self):
        file = open(os.path.join(self.currDir,"UserData/user.txt"),'r') ## open the file which store username nad password
        username,passw = file.read().splitlines()                       ## split the username and password and save in different variables
        self.UserData['username'] = username                            ## save username to dictonary
        self.UserData['password'] = passw                               ## save password to dictonary
        file.close()                                                    ## close the file