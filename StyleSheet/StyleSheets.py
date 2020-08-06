class StyleSheets():
    def ButtonStyleSheet():
        return """
                QPushButton{
                    background-color:#ffffff;
                    border:hidden;
                    height:100px;
                    width:100px;
                    font-weight: bold;
                    font-size:40px;
                }
                QPushButton:hover{
                    background-color:#9be6ff;
                    
                    
                }
        """
    def GreyButtonStyleSheet():
        return """
                QPushButton{
                    background-color:#cfcfcf;
                    border:hidden;
                    height:100px;
                    width:100px;
                    font-size:25px;
                }
                QPushButton:hover{
                    background-color:#66ff7f;
                    
                    
                }
        """
    def EditTextStyleSheet():
        return """
                QLineEdit{
                    font-weight: bold;
                    text-align: right;
                    border:hidden;
                    font-size:30px;
                    height:250px;
                    background-color: transparent;
                }
                QLineEdit:hover{
                    
                    border:2px black;
                }
        """
    def MainWindowStyleSheet():
        return """
                QMainWindow{
                    border:12px black;
                }
        """
    def TopLabelStyleSheet():
        return """
                QLabel{
                    background-color:transparent;
                    font-Size:30px;
                    font-weight:100px;
                }
        """
    def HistorySectionStyleSheet():
        return """
                QTextEdit{
                    background-color:transparent;
                    font-Size:20px;
                    
                    font-weight:100px;
                }
        """
    def LoginButtonStyleSheet():
        return '''
                QPushButton{
                    background-color:#a2a8ff;
                    color:#0210da;
                    font-size:20px;
                    font-weight:bold;
                }
        '''
    def EntryStyleSheet():
        return '''
                QLineEdit{
                    height:50px;
                    font-size:20px;
                }
        '''
    def WrongEntryStyleSheet():
        return '''
                QLineEdit{
                    height:50px;
                    font-size:20px;
                    background-color:#ffd6d6;
                }
        '''