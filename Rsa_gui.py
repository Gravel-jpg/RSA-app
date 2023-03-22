from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
import random
import linecache

####-----Dialog Boxes-----####
class Ui_Encrypt_Dialog(object):
    def fileDialog(self):
        fname = QFileDialog.getOpenFileName(None,'Open file','Public key','(*.txt)')
#         fname = QFileDialog.getOpenFileName("QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)")
        if fname and fname != ('',''):
            print(fname)
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(150, 60, 100, 23))
        self.pushButton.setObjectName("pushButton")
        
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(125, 140, 150, 20))
        self.lineEdit.setObjectName("lineEdit")
        
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 270, 100, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        #file dialog
        self.pushButton.clicked.connect(self.fileDialog)
        #save ciphertext
        self.pushButton_2
        
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Select public keys"))
        self.pushButton_2.setText(_translate("Dialog", "Save ciphertext"))
class Ui_Decrypt_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(150, 40, 100, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 80, 100, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(75, 110, 250, 180))
        self.textBrowser.setObjectName("textBrowser")
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Select private keys"))
        self.pushButton_2.setText(_translate("Dialog", "select ciphertext"))
        self.textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
####-----Rsa functions-----#####
def choose_primes(filename,lim):
    p = random.randint(1,lim)
    q = random.randint(1,lim)
    p = linecache.getline(filename,p)
    q = linecache.getline(filename,q)
    while p == q:
        q = random.randint(1,lim)
        q = linecache.getline(filename,q)
    return int(p),int(q)  
def generate_keys(p,q):
    n = p*q
    m = (p-1)*(q-1)
    e = 65537
    gen1 = [1,0,e,None]
    gen2 = [0,1,m,None]
    gen3 = [None,None,None,None]
    while True:
        gen3[3] = int((gen1[2]//gen2[2]))
        gen3[0] = gen1[0] - (gen2[0]*gen3[3])
        gen3[1] = gen1[1] - (gen2[1]*gen3[3])
        gen3[2] = gen1[2] - (gen2[2]*gen3[3])
        if gen3[2] == 0:
            break
        gen1 = gen2.copy()
        gen2 = gen3.copy()
    d = gen2[0]+m
    return(n,m,e,d)
####-----Main Window-----####
class Ui_MainWindow(object):
#     def fileDialog(self):
#         fname = QFileDialog.getOpenFileName(self,'Open file','All Files (*);;Text Files (*.txt)')
# #         fname = QFileDialog.getOpenFileName("QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)")
#         if fname:
#             print(fname)
    def open_Encrypt_Window(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Encrypt_Dialog()
        self.ui.setupUi(self.window)
        self.window.show()
        
    def open_Decrypt_Window(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Decrypt_Dialog()
        self.ui.setupUi(self.window)
        self.window.show()
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 300)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.button1 = QtWidgets.QPushButton(self.centralwidget)
        self.button1.setGeometry(QtCore.QRect(125, 10, 150, 60))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button1.sizePolicy().hasHeightForWidth())
        self.button1.setSizePolicy(sizePolicy)
        self.button1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.button1.setObjectName("button1")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setEnabled(True)
        self.pushButton.setGeometry(QtCore.QRect(125, 90, 150, 60))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(125, 170, 150, 60))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
#         self.button1.clicked.connect(self.fileDialog)
        self.button1.clicked.connect(Generate_New_keys)
        self.pushButton.clicked.connect(self.open_Encrypt_Window)
        self.pushButton_2.clicked.connect(self.open_Decrypt_Window)
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Rsa"))
        self.button1.setText(_translate("MainWindow", "Generate New keys"))
        self.pushButton.setText(_translate("MainWindow", "Encrypt"))
        self.pushButton_2.setText(_translate("MainWindow", "Decrypt"))
        self.actionAbout.setText(_translate("MainWindow", "About"))

def Generate_New_keys():
    global p,q,n,m,e,d
    p,q = choose_primes('300 digit primes.txt',15)
    n,m,e,d = generate_keys(p,q)
    with open('private_keys.txt','w') as f:
        f.write(str(n)+'\n')
        f.write(str(d))
        
    
# def Encrypt():
#     pass
# def Decrypt():
#     pass
#Not sure why this needs to be in this if statement but its stops crashing on startup so ¯\_(ツ)_/¯
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)        
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
