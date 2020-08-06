from PyQt5.QtWidgets import QApplication,QWidget,QLineEdit,QTextEdit,QVBoxLayout,QHBoxLayout,QPushButton,QFormLayout,QGridLayout,QMainWindow,QDialog
from PyQt5.QtWidgets import QStatusBar,QLabel
from PyQt5 import QtCore
import time
from Query.Query import Query
import math
import sys
import speech_recognition as sr
import pyttsx3
import threading
from StyleSheet.StyleSheets import StyleSheets
class MainApplication(QMainWindow):
    def __init__(self,parent = None):
        super().__init__(parent)
        self._allWidgets:dict = {}
        self._unicode:dict = {
            "rootsign":"\u221a",
            "square":"X\u00b2",
            "backarrow":"\u2192"            
        }
        self.Query = Query()
        self.setGeometry(100,30,500,800)
        self.setWindowTitle("Calculator")
        self.setStyleSheet(StyleSheets.MainWindowStyleSheet())
        self.createMenu()
        self.createStatusBar()
        self._iseqlpressed = False
        self.buttonGrid = QGridLayout()
        self.mainWidget = QWidget()
        self.extrabuttonGrid = QGridLayout()
        self.mainOuterlLayout = QHBoxLayout(self.mainWidget)
        self.mainRightLayout = QVBoxLayout()
        self.mainLeftLayout = QVBoxLayout()
        self.setCentralWidget(self.mainWidget)
        self.createAllButtons()
        self.createExtraButton()
        self.BindAllMainWidget()

        self.RecEngine = None
        self.VoiceEngine = None
        self.is_listning = False
        self.audio = None
        self.notspeaking = True
        self.allThreadStart = False

    def createOneBtn(self,text,stylesheet):
        btn = QPushButton(text)
        btn.setStyleSheet(stylesheet)
        if text not in ['C','=',"1/X","+,-","+","-","X","/","%","Sin","Cos","Tan","Log"] + list(self._unicode.values()):
            btn.clicked.connect(lambda : (self.Query.numbtnpressed(text),self.updateUI()))
        else:
            self.setButtonClick(text,btn)
        self._allWidgets["btn"+text] = btn
        return btn

    def setButtonClick(self,symbol,btn):
        if symbol == "C":
            btn.clicked.connect(lambda: (self.Query.clearQuery(),self.updateUI()))
        if symbol == "=":
            btn.clicked.connect(lambda : (self.Query.evalRes(),self.updateUI()))
        if symbol == self._unicode["rootsign"]:
            btn.clicked.connect(lambda : (self.Query.calcRoot(),self.updateUI()))
        if symbol == self._unicode["square"]:
            btn.clicked.connect(lambda : (self.Query.calcSquare(),self.updateUI()))
        if symbol == self._unicode["backarrow"]:
            btn.clicked.connect(lambda : (self.Query.backclicked(),self.updateUI()))
        if symbol == "1/X":
            btn.clicked.connect(lambda : (self.Query.ratioclicked(),self.updateUI()))
        if symbol == "+,-":
            btn.clicked.connect(lambda : (self.Query.Signclicked(),self.updateUI()))
        if symbol == "Sin":
            btn.clicked.connect(lambda : (self.Query.Sinclicked(),self.updateUI()))
        if symbol == "Cos":
            btn.clicked.connect(lambda : (self.Query.Cosclicked(),self.updateUI()))
        if symbol == "Tan":
            btn.clicked.connect(lambda : (self.Query.Tanclicked(),self.updateUI()))
        if symbol == "Log":
            btn.clicked.connect(lambda : (self.Query.Logclicked(),self.updateUI()))
        if symbol in ["+","-","X","/","%"]:
            btn.clicked.connect(lambda : (self.Query.operationBtnPressed(symbol),self.updateUI()))


    def createMenu(self):
        menu1 = self.menuBar().addMenu("File")
        menu1.addAction("Start Voice Asistance",self.StartThreading)
        menu1.addAction("Restart Voice Asistance",lambda:(self.StopThreading(),self.StartThreading()))
        menu1.addAction("Stop Voice Asistance",self.StopThreading)
        menu1.addAction("Exit",self.close)


    def createStatusBar(self):
        status = QStatusBar()
        status.showMessage("Status Bar")
        self.setStatusBar(status)
        self._allWidgets["statusbar"] = status

    def createTopLabel(self):
        toplabel = QLabel("Standard")
        toplabel.setStyleSheet(StyleSheets.TopLabelStyleSheet())
        self._allWidgets["toplabel"] = toplabel
        return toplabel


    def createHistorySection(self):
        history = QTextEdit("")
        history.setReadOnly(True)
        history.setAlignment(QtCore.Qt.AlignTop)
        history.setFixedWidth(400)
        history.setStyleSheet(StyleSheets.HistorySectionStyleSheet())
        self._allWidgets["history"] = history
        return history


    def createHistoryLabel(self):
        histlabl = QLabel("History")
        histlabl.setStyleSheet(StyleSheets.TopLabelStyleSheet())
        self._allWidgets["histlabl"] = histlabl
        return histlabl

    
    def createEditWindow(self):
        _query_view = QLineEdit(self.Query.getcurrentQuery())
        _query_view.setAlignment(QtCore.Qt.AlignRight)
        _query_view.setStyleSheet(StyleSheets.EditTextStyleSheet())
        _query_view.setReadOnly(True)
        _query_view.setFocus()
        self._allWidgets["queryView"] = _query_view
        return _query_view
    
    def BindAllMainWidget(self):
        self.mainOuterlLayout.addLayout(self.mainRightLayout)
        self.mainOuterlLayout.addLayout(self.mainLeftLayout)
        self.mainRightLayout.addWidget(self.createTopLabel())
        self.mainRightLayout.addWidget(self.createEditWindow())
        self.mainRightLayout.addLayout(self.buttonGrid)
        self.mainLeftLayout.addWidget(self.createHistoryLabel())
        self.mainLeftLayout.addWidget(self.createHistorySection())
        self.mainLeftLayout.addLayout(self.extrabuttonGrid)


    def createAllButtons(self):
        self.buttonGrid.addWidget(self.createOneBtn('%',StyleSheets.GreyButtonStyleSheet()),0,0)
        self.buttonGrid.addWidget(self.createOneBtn('\u221a',StyleSheets.GreyButtonStyleSheet()),0,1)
        self.buttonGrid.addWidget(self.createOneBtn('X\u00b2',StyleSheets.GreyButtonStyleSheet()),0,2)
        self.buttonGrid.addWidget(self.createOneBtn('1/X',StyleSheets.GreyButtonStyleSheet()),0,3)
        self.buttonGrid.addWidget(self.createOneBtn('C',StyleSheets.GreyButtonStyleSheet()),1,0,1,2)
        self.buttonGrid.addWidget(self.createOneBtn('\u2192',StyleSheets.GreyButtonStyleSheet()),1,2)
        self.buttonGrid.addWidget(self.createOneBtn('/',StyleSheets.GreyButtonStyleSheet()),1,3)
        self.buttonGrid.addWidget(self.createOneBtn('7',StyleSheets.ButtonStyleSheet()),2,0)
        self.buttonGrid.addWidget(self.createOneBtn('8',StyleSheets.ButtonStyleSheet()),2,1)
        self.buttonGrid.addWidget(self.createOneBtn('9',StyleSheets.ButtonStyleSheet()),2,2)
        self.buttonGrid.addWidget(self.createOneBtn('X',StyleSheets.GreyButtonStyleSheet()),2,3)
        self.buttonGrid.addWidget(self.createOneBtn('4',StyleSheets.ButtonStyleSheet()),3,0)
        self.buttonGrid.addWidget(self.createOneBtn('5',StyleSheets.ButtonStyleSheet()),3,1)
        self.buttonGrid.addWidget(self.createOneBtn('6',StyleSheets.ButtonStyleSheet()),3,2)
        self.buttonGrid.addWidget(self.createOneBtn("-",StyleSheets.GreyButtonStyleSheet()),3,3)
        self.buttonGrid.addWidget(self.createOneBtn('1',StyleSheets.ButtonStyleSheet()),4,0)
        self.buttonGrid.addWidget(self.createOneBtn('2',StyleSheets.ButtonStyleSheet()),4,1)
        self.buttonGrid.addWidget(self.createOneBtn('3',StyleSheets.ButtonStyleSheet()),4,2)
        self.buttonGrid.addWidget(self.createOneBtn('+',StyleSheets.GreyButtonStyleSheet()),4,3)
        self.buttonGrid.addWidget(self.createOneBtn('+,-',StyleSheets.GreyButtonStyleSheet()),5,0)
        self.buttonGrid.addWidget(self.createOneBtn('0',StyleSheets.ButtonStyleSheet()),5,1)
        self.buttonGrid.addWidget(self.createOneBtn('.',StyleSheets.GreyButtonStyleSheet()),5,2)
        self.buttonGrid.addWidget(self.createOneBtn('=',StyleSheets.GreyButtonStyleSheet()),5,3)
    def createExtraButton(self):
        self.extrabuttonGrid.addWidget(self.createOneBtn('Sin',StyleSheets.GreyButtonStyleSheet()),0,0)
        self.extrabuttonGrid.addWidget(self.createOneBtn('Cos',StyleSheets.GreyButtonStyleSheet()),0,1)
        self.extrabuttonGrid.addWidget(self.createOneBtn('Tan',StyleSheets.GreyButtonStyleSheet()),1,0)
        self.extrabuttonGrid.addWidget(self.createOneBtn('Log',StyleSheets.GreyButtonStyleSheet()),1,1)

    def updateUI(self):
        self._allWidgets["queryView"].setText(self.Query.getcurrentQuery())
        self._allWidgets["history"].setText(self.Query.getTotalQuery())     
        self._allWidgets["statusbar"].showMessage(self.Query.getStatus())  




    def StartThreading(self):
        if not self.allThreadStart:
            self._allWidgets["statusbar"].showMessage("Please Wait . . . . ")
            # this thread used for setup speech recognition engine
            self.setupsrenginethread = threading.Thread(target=self.SetupSREngine)
            self.setupsrenginethread.daemon = True
            self.setupsrenginethread.start()

            # this is the second thread and used for setup the voice engine
            self.setupVoiceThread = threading.Thread(target=self.SetupVoiceEngine)
            self.setupVoiceThread.daemon = True
            self.setupVoiceThread.start()


            # this is third thread and used for listening our command
            if self.RecEngine:
                self.takecommandthread = threading.Thread(target = self.takeCommand)
                self.takecommandthread.daemon = True
                self.takecommandthread.start()
                
            self.allThreadStart = True
    def StopThreading(self):
        if self.allThreadStart:
            self.is_listning = False
            
            self.allThreadStart = False
            self.takeCommand()
            self.ProcessCommand()
            #print("All Proccess stop")


        
    # this fuction is used for setup speech recognition engine 
    def SetupSREngine(self):
        #setup speech recognition engine
        self.RecEngine = sr.Recognizer()
        self.is_listning = True
        self._allWidgets["statusbar"].showMessage('Listening Engine setup')
    

    def SetupVoiceEngine(self):
        #this function is use for septup voice engine and set the propeties of the engine like voice and rate
        try:
        #setup voice engine here 
            self.VoiceEngine = pyttsx3.Engine('sapi5')
            voice = self.VoiceEngine.getProperty("voices")
            if len(voice)>0:
                #set voice property of the engine
                self.VoiceEngine.setProperty('voice',voice[0])
            else:
                self._allWidgets["statusbar"].showMessage('No Voice Installed')
            #set rate property of engine
            self.VoiceEngine.setProperty('rate',100)
            
            self._allWidgets["statusbar"].showMessage("Voice Engine setup successfully")
        except Exception as e:
            print(e)
            self._allWidgets["statusbar"].showMessage('Unknown error occur')


    def Speak(self,voice):
        #this function is used for speaking whatever i want
        self.notspeaking = False 
        self._allWidgets["statusbar"].showMessage("Speaking. . . ")
        self.VoiceEngine.say(voice)
        self.VoiceEngine.startLoop(False)
        self.VoiceEngine.iterate()
        self.VoiceEngine.endLoop()
        self.notspeaking = True
        return

    #this fuction take command from microphone
    def takeCommand(self):
        try:
            #create microphone for recording the sound
            with sr.Microphone() as source:
                if not self.RecEngine:
                    self._allWidgets["statusbar"].showMessage("Speech recognition is not working")
                    return
                if self.is_listning and self.notspeaking:
                    self._allWidgets["statusbar"].showMessage('Listening . . . .')
                    #listen the audio from micophone using engine
                    self.audio = self.RecEngine.listen(source)
                    #amount of second for wait whe no one is speaking
                    #self.RecEngine.pause_threshold = 0.8
                    self.RecEngine.energy_threshold = 300
                    # after listening process the command
                    self.ProcessCommand()
                else:
                    self._allWidgets["statusbar"].showMessage("Listening Stopped")
                    return
        except OSError as e:
            print(e)
            self.StopThreading()
            self._allWidgets["statusbar"].showMessage("OS error Occur ,Listening Stopped ,Restart the process")
            
        
    #this function process the command using google api
    def ProcessCommand(self):
        query = ''
        voice = ''
        if not self.is_listning:
            return
        if self.audio.get_raw_data != None:
            self._allWidgets["statusbar"].showMessage('Processing Please Wait')
            try:
                #this google api is convert the audio data into text
                query = self.RecEngine.recognize_google(self.audio,language='en-in')
                print(query)
                rawquery = query
                if 'x' in query or 'X' in query or 'multiply' in query:
                    query = query.replace('x','*')
                    query = query.replace('X','*')
                    query = query.replace('multiply','*')
                    query = query.replace('into','*')
                if 'plus' in query:
                    query = query.replace('plus','+')
                if 'minus' in query:
                    query = query.replace('minus','-')
                if 'by' in query:
                    query = query.replace('by','/')
                    query = query.replace('divide','')
                if 'divide' in query:
                    query = query.replace('by','')
                    query = query.replace('divide','/')
                if 'modulus' in query:
                    query = query.replace('modulus','%')
                if 'sin' in query:
                    query = self.modifyQuery(query)
                if 'cos' in query:
                    query = self.modifyQuery(query)
                if 'tan' in query:
                    query = self.modifyQuery(query)
                if 'log' in query:
                    query = self.modifyQuery(query)
                if 'root' in query:
                    query = self.modifyQuery(query)
                if 'square' in query:
                    query = self.modifyQuery(query)
                if 'stop' in query:
                    self.StopThreading()
                    #self.is_listning = False
                    #self.takeCommand()
                    return
                    # result is calculate using eval() function
                self._allWidgets["queryView"].setText(str(eval(query)))
                voice = str(rawquery) + 'is' + str(eval(query))
                voice = self.ClearVoice(voice)
                #for speaking the output
                self.Speak(voice)
                
            except Exception as e:
                #print('Query is ' + query)
                print("Exception",e)
                self._allWidgets["statusbar"].showMessage("Can't Recognized.Please say again")
                time.sleep(2)
            if self.is_listning:
                #print('hi')
                self.takeCommand()
    # this function cleat the voice or remove unwanted words for processing
    def ClearVoice(self,voice):
        if '/' in voice:
            voice = voice.replace('/','by')
        if '*' in voice:
            voice = voice.replace('*','multiply by')
        if '.' in voice:
            voice = voice.replace('.','point')
        return voice
    def modifyQuery(self,query:str):
        if 'sin' in query:
            query = query.replace("of","")
            query = query.replace('sin',"math.sin(")+")"
            return query
        if 'cos' in query:
            query = query.replace("of","")
            query = query.replace('cos',"math.cos(")+")"
            return query
        if 'tan' in query:
            query = query.replace("of","")
            query = query.replace('tan',"math.tan(")+")"
            return query
        if 'log' in query:
            query = query.replace("of","")
            query = query.replace('log',"math.log(")+")"
            return query
        if 'root' in query:
            query = query.replace("of","")
            query = query.replace('root',"math.sqrt(")+")"
            return query
        if 'square' in query:
            query = query.replace("of","")
            query = query.replace('square',"math.pow(")+",2)"
            return query