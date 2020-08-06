import math
class Query():
    def __init__(self):
        self.currentQuery = "0"
        self.totalquery = ""
        self.currres = ""
        self.specialopr = False
        self.signpress = False
        self.signres = ""
        self.listening = False
        self.statusmes = "Status "
        self.currentoperation = ""
    def numbtnpressed(self,num):
        if self.listening:
            return
        if num == ".":
            if self.currentQuery.find(".") != -1:
                return
            else:
                if self.currentQuery == "0":
                    self.currentQuery += num
                    self.totalquery += self.currentQuery
                    return
        if self.currentQuery == "0":
            self.currentQuery = ""
        self.currentQuery += num
        if self.specialopr:
            if self.currentoperation != "":
                self.totalquery += self.currentoperation + num
            else:
                self.totalquery = num
            self.currentQuery = num
            self.specialopr = False
        else:
            self.totalquery += num
        self.signpress = False
    def operationBtnPressed(self,opr):
        if self.listening:
            return
        if len(self.totalquery)<=0:
            return
        if opr == "X":
            opr = "*"
        self.currentoperation = opr
        self.currentQuery = "0"
        if self.totalquery[-1] in ['+','-','*','/','%']:
            self.totalquery = self.totalquery[:-1] + opr
        else:
            self.totalquery += opr
            self.specialopr = False
    def clearQuery(self):
        self.currentQuery = "0"
        self.currentoperation = ""
        self.totalquery = ""
        self.specialopr = False
        self.signpress = False
    def evalRes(self):
        if self.listening:
            return
        try:
            self.curres = str(round(eval(self.totalquery),15))
            self.currentQuery = self.curres
            self.totalquery = self.curres
            self.specialopr = False
        except:
            self.statusmes = "Bad expression"
    def calcRoot(self):
        if self.currentQuery != '0':
            currqlen = len(self.currentQuery)
        else:
            return
        res = str(math.sqrt(float(self.currentQuery)))
        self.currentQuery = res
        self.totalquery = self.totalquery[:-currqlen]
        self.totalquery += res 
        self.specialopr = True
        self.signpress = False
    def calcSquare(self):
        if self.currentQuery != '0':
            currqlen = len(self.currentQuery)
        else:
            return
        res = str(math.pow(float(self.currentQuery),2))
        self.currentQuery = res
        self.totalquery = self.totalquery[:-currqlen]
        self.totalquery += res
        self.specialopr = True
        self.signpress = False
    def backclicked(self):
        if len(self.currentQuery)>0 and self.currentQuery != "0":
            self.currentQuery = self.currentQuery[:-1]    
            self.totalquery = self.totalquery[:-1]
    def ratioclicked(self):
        if self.currentQuery == '0':
            return
        currqlen = len(self.currentQuery)
        self.currentQuery = "1/"+self.currentQuery
        res = str(round(eval(self.currentQuery),15))
        self.currentQuery = res
        self.totalquery = self.totalquery[:-currqlen]
        self.totalquery += res
        self.specialopr = True
        self.signpress = False
    def Signclicked(self):
        if self.currentQuery == "":
            return
        if self.currentQuery == '0':
            return
        self.currentQuery = str(float(self.currentQuery)*-1)
        self.totalquery += "*-1"
        self.signpress = True
    def Sinclicked(self):
        if self.currentQuery != '0':
            currqlen = len(self.currentQuery)
        else:
            return
        res = str(math.sin(float(self.currentQuery)))
        self.currentQuery = res
        self.totalquery = self.totalquery[:-currqlen]
        self.totalquery += res
        self.specialopr = True
        self.signpress = False
    def Cosclicked(self):
        if self.currentQuery != '0':
            currqlen = len(self.currentQuery)
        else:
            return
        res = str(math.cos(float(self.currentQuery)))
        self.currentQuery = res
        self.totalquery = self.totalquery[:-currqlen]
        self.totalquery += res
        self.specialopr = True
        self.signpress = False
    def Tanclicked(self):
        if self.currentQuery != '0':
            currqlen = len(self.currentQuery)
        else:
            return
        res = str(math.tan(float(self.currentQuery)))
        self.currentQuery = res
        self.totalquery = self.totalquery[:-currqlen]
        self.totalquery += res
        self.specialopr = True
        self.signpress = False
    def Logclicked(self):
        if self.currentQuery != '0':
            currqlen = len(self.currentQuery)
        else:
            return
        res = str(math.log10(float(self.currentQuery)))
        self.currentQuery = res
        self.totalquery = self.totalquery[:-currqlen]
        self.totalquery += res
        self.specialopr = True
        self.signpress = False
    def getcurrentQuery(self):
        return self.currentQuery
    def getcurrentOpr(self):
        return self.currentoperation
    def getTotalQuery(self):
        return self.totalquery
    def getStatus(self):
        return self.statusmes
    def getcurrAns(self):
        return self.curres
    def setcurrentQuery(self,query):
        self.currentQuery = query
    def setTotalQuery(self,query):
        self.totalquery = query
        