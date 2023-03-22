from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
import random
import linecache
#####TODO#####
#turn shift_ciphers into a .json file that is loaded on startup?
#find someway to make this into a .exe
shift_cipher1 = {'a':15,'b':78,'c':23,'d':11,'e':65,'f':24,'g':76,'h':87,'i':90,'j':16,'k':48,'l':93,'m':58,'n':97,'o':53,'p':84,'q':86,'r':59,'s':35,'t':36,'u':63,'v':57,'w':75,'x':41,'y':79,'z':74,' ':92,',':10,'.':29,'!':12}
shift_cipher2 = {15:'a',78:'b',23:'c',11:'d',65:'e',24:'f',76:'g',87:'h',90:'i',16:'j',48:'k',93:'l',58:'m',97:'n',53:'o',84:'p',86:'q',59:'r',35:'s',36:'t',63:'u',57:'v',75:'w',41:'x',79:'y',74:'z',92:' ',10:',',29:'.',12:'!'}
class Ui_Encrypt_Dialog(object):
    def fileDialog(self):
        global n,e
        fname = QFileDialog.getOpenFileName(None,'Open file','Public keys','(*.txt)')
        if fname and fname != ('',''):
            n = linecache.getline(fname[0],1)
            e = linecache.getline(fname[0],2)
    def save_ciphertext(self):
        fileName = QFileDialog.getSaveFileName(None,'Save file')
        with open(fileName[0],'w') as f:
            text = self.lineEdit.text()
            Msg = ''
            for i in text:
                i = i.lower()
                x = str(shift_cipher1[i])
                Msg += x
            Ciphertext = crypt(int(Msg),int(e),int(n))
            f.write(str(Ciphertext))
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
        self.pushButton.clicked.connect(self.fileDialog)
        self.pushButton_2.clicked.connect(self.save_ciphertext)
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Select public keys"))
        self.pushButton_2.setText(_translate("Dialog", "Save ciphertext"))
class Ui_Decrypt_Dialog(object):
    def fileDialog(self):
        global n,d
        fname = QFileDialog.getOpenFileName(None,'Open file','Private keys','(*.txt)')
        if fname and fname != ('',''):
            n = linecache.getline(fname[0],1)
            d = linecache.getline(fname[0],2)
    def select_ciphertext(self):
        if d == None:
            raise Exception
        fname = QFileDialog.getOpenFileName(None,'Open file','Ciphertext file','(*.txt)')
        ciphertext = int(linecache.getline(fname[0],1))
        text = str(crypt(ciphertext,int(d),int(n)))
        text = [text[i:i+2] for i in range(0, len(text), 2)]
        translated = ''
        for i in text:
            translated += shift_cipher2[int(i)]
        self.textBrowser.append(translated)
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(150, 40, 100, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.fileDialog)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 80, 100, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.select_ciphertext)
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
def crypt(base,exponent,mod):
    oldbase = base
    exponent = bin(exponent)
    for i in range(3,len(exponent)):
        if exponent[i] == '0':
            base = (base**2)%mod
        else:
            base = ((base**2)*oldbase)%mod
    return(base%mod)
####-----Main Window-----####
class Ui_MainWindow(object):
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
    p,q = choose_primes('300 digit primes.txt',18)
    n,m,e,d = generate_keys(p,q)
    with open('private_keys.txt','w') as f:
        f.write(str(n)+'\n')
        f.write(str(d))
    with open('public_keys.txt','w') as f:
        f.write(str(n)+'\n')
        f.write(str(e))
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)        
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()