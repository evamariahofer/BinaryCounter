#!/usr/bin/env python3
# 2021 nr@bulme.at

from gpiozero import Button
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QLCDNumber,
    QVBoxLayout, QApplication)
from gpiozero import LED

leds = [LED(18),LED(23),LED(24),LED(25)]

DOWN_PIN = 22
RESET_PIN = 27
UP_PIN = 17 

class QtButton(QObject):
    changed = pyqtSignal()

    def __init__(self, pin):
        super().__init__()
        self.button = Button(pin) 
        self.button.when_pressed = self.gpioChange        

    def gpioChange(self):
        self.changed.emit()

class Counter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.count = 0
        self.binaryNr = [8,4,2,1]

    def initUi(self):
        self.lcd = QLCDNumber()
        self.lcd.display(0)

        vbox = QVBoxLayout()
        vbox.addWidget(self.lcd)

        self.setLayout(vbox)
        self.setMinimumSize(400, 200)
        self.setWindowTitle('Counter')
        self.show()


    def countUp(self):
        if self.count < 15:        
            self.count += 1
        else:
            self.count = 0
        self.countLeds()
        self.lcd.display(self.count)
        
    def countDown(self):
        if self.count > 0:        
            self.count -= 1
        else:
            self.count = 15
        self.countLeds()
        self.lcd.display(self.count)  
        
    def countReset(self):
        self.count = 0
        self.countLeds()
        self.lcd.display(self.count)
        
    def countLeds(self):
        tmp = self.count
        for index, nr in enumerate(self.binaryNr):
            if tmp - nr >= 0:
                leds[index].on()
                tmp -= nr
            else:
                leds[index].off()
        

if __name__ ==  '__main__':
    app = QApplication([])
    gui = Counter()
    button = QtButton(UP_PIN)
    button.changed.connect(gui.countUp)
    button = QtButton(DOWN_PIN)
    button.changed.connect(gui.countDown)
    button = QtButton(RESET_PIN)
    button.changed.connect(gui.countReset)
    app.exec_()
    
