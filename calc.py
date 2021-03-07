from PyQt5 import QtWidgets, uic
import sys
import pprint
from math import sqrt, trunc

BUTTONS = [
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine',
    'zero',
    'multiply',
    'devide',
    'reset',
    'dot',
    'equal',
    'plus',
    'minus'
    ]

ACTION_BUTTONS = [
    'multiply',
    'devide',
    'reset',
    'dot',
    'equal',
    'plus',
    'minus'
]


def parceInput(obj):
    if obj.currInput:
        return int(str(obj.currInput).strip('[]').replace(',','').replace(' ',''))
def parcePending(obj):
    if obj.pendingInput:
        return int(str(obj.pendingInput).strip('[]').replace(',','').replace(' ',''))
        
def moveParcedToPending(obj):
    currAnswer = obj.currAnswer
    prevAnswer = obj.prevAnswer
    answerList = [int(x) for x in str(trunc(currAnswer))]
    if obj.prevAnswer:
        answerList = [int(x) for x in str(trunc(prevAnswer))]
    else:
        answerList = [int(x) for x in str(trunc(currAnswer))]
    obj.pendingInput = answerList.copy()

def moveToPending(obj, reset = False):
    obj.pendingInput = obj.currInput.copy()
    obj.currInput[:] = []
    if reset:
        obj.label.setText(str(0))
    # print('hi')

def resetVariables(obj, reset = False):
    obj.currInput[:] = []
    # obj.pendingInput[:] = []
    if reset:
        obj.currOperation = str()
        obj.label.setText(str(0))

def executeOperation(obj):
    parcedInput = parceInput(obj)
    parcedPending = parcePending(obj)
    currAns = obj.currAnswer
    if currAns is not 0:
        pass
    if obj.currInput and obj.pendingInput:
        if obj.currOperation == 'plus':
            obj.currAnswer = parcedPending + parcedInput
        elif obj.currOperation == 'minus':
            obj.currAnswer = parcedPending - parcedInput
        elif obj.currOperation == 'multiply':
            obj.currAnswer = parcedPending * parcedInput
            print(sqrt(parcedInput),'hello')
        elif obj.currOperation == 'devide':
            obj.currAnswer = parcedPending / parcedInput

    # elif obj.currInput and not obj.pendingInput:
    #     if obj.currOperation == 'sqrroot':
    #         obj.currAnswer = sqrt(parcedInput)
    #         print(sqrt(parcedInput),'hello')
    #     elif obj.currOperation == 'exponent':
    #         obj.currAnswer = parcedInput**2

class Ui(QtWidgets.QDialog):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('calc.ui', self)
        # Link buttons to buttonPress fucntion
        for button in BUTTONS:
            curr_btn = getattr(self, button)
            curr_btn.clicked.connect(self.buttonPress)

        # Define variables
        self.currInput = []
        self.pendingInput = []
        self.currOperation = str()
        self.currAnswer = 0
        self.prevAnswer = 0
        self.show()

    # Button press handler
    def buttonPress(self):
        btnName = self.sender().objectName()
        # Check if button is in an 'operation' button
        if btnName in ACTION_BUTTONS:
            if btnName == 'plus' or btnName == 'minus' or btnName == 'multiply' or btnName == 'devide':
                moveToPending(self,reset=True)
                self.currOperation = btnName

            if btnName == 'equal':
                executeOperation(self)
                print(self.currAnswer)
                self.label.setText(str(round(self.currAnswer,2)))
                self.prevAnswer = self.currAnswer
                print('Answer:', self.currAnswer)
                moveParcedToPending(self)
                resetVariables(self)
                
                # moveToPending(self)
                # self.currInput[:] = []
                # self.pendingInput[:] = []

            if btnName == 'reset':
                resetVariables(self,reset = True)
                # self.currInput[:] = []
                # self.pendingInput[:] = []
                # self.label.setText(str(0))
            # print('post',self.pendingInput)

        else:
            num = int(self.sender().text())
            if len(self.currInput) < 5:
                self.currInput.append(num)
                parsedInput = parceInput(self)
                self.label.setText(str(parsedInput))


app = QtWidgets.QApplication(sys.argv)
window = Ui()

# print(dir(window))
app.exec_()