import sys
import os
import re

from PyQt4 import QtGui,QtCore

FPS = 60
BUFFER_PATH = os.path.join(os.getcwd(),"buffer/")

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]


class CascadeTV(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(CascadeTV, self).__init__(parent)
        
        # Carrega imagem do BUFFER
        self.buffer = []
        for each in os.listdir(BUFFER_PATH):

            selFile = os.path.join(BUFFER_PATH, each)
            print selFile
            if os.path.isfile(selFile) and selFile.endswith('png'):
                self.buffer.append(selFile)

        self.buffer.sort(key=natural_keys)
        print BUFFER_PATH
        # Contador 
        self.count = 0

        # Taxa de update
        self.updateTimer = QtCore.QTimer()
        self.updateTimer.start(FPS)

        # connect do Qt
        self.connect(self.updateTimer, QtCore.SIGNAL("timeout()"), self.nextImage)

        # Criando a Janela
        screen = QtGui.QDesktopWidget().screenGeometry(self)

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.label = QtGui.QLabel("yoo")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.setCentralWidget(self.label)

        # Pegando proxima imagem do BUFFER
        self.nextImage()  
        
        
    # Desenha na tela
    def nextImage(self):
        if self.buffer:
            if self.count >= len(self.buffer):
                self.count = 0

            image = QtGui.QImage(self.buffer[self.count])
            pp = QtGui.QPixmap.fromImage(image)
            if not pp.isNull():
                self.label.setPixmap(pp.scaled(
                        self.label.size(),
                        QtCore.Qt.KeepAspectRatio,
                        QtCore.Qt.SmoothTransformation))

            self.count += 1



if __name__ == '__main__':
    

    # Criando aplicativo
    app = QtGui.QApplication(["CascadeTV"])    
    window = CascadeTV()
    window.show()
    window.resize(800,800*9/16)  
    window.raise_()
    app.exec_()
