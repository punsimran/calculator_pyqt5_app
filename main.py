import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from calculator_ui import Ui_MainWindow

class Calculator(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Make the window fixed size (prevent resizing)
        self.setFixedSize(self.size())
        
        self.setWindowTitle("Calculator")
        
        # Fix display focus
        self.ui.display.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.ui.display.setFocus()
        # Prevent direct typing into the display (so letters can't be entered)
        self.ui.display.setReadOnly(True)
        
        # Initialize
        self.current_expression = ""
        self.ui.display.setText("0")
        
        # Remove all shortcuts from buttons
        self.remove_all_shortcuts()
        
        # Connect all buttons
        self.connect_buttons()
        
    def remove_all_shortcuts(self):
        """Remove shortcuts from all buttons so keyboard works properly"""
        for button in self.findChildren(QtWidgets.QPushButton):
            button.setShortcut("")
        
    def connect_buttons(self):
        # Number buttons (0-9)
        self.ui.btn_0.clicked.connect(lambda: self.button_clicked('0'))
        self.ui.btn_1.clicked.connect(lambda: self.button_clicked('1'))
        self.ui.btn_2.clicked.connect(lambda: self.button_clicked('2'))
        self.ui.btn_3.clicked.connect(lambda: self.button_clicked('3'))
        self.ui.btn_4.clicked.connect(lambda: self.button_clicked('4'))
        self.ui.btn_5.clicked.connect(lambda: self.button_clicked('5'))
        self.ui.btn_6.clicked.connect(lambda: self.button_clicked('6'))
        self.ui.btn_7.clicked.connect(lambda: self.button_clicked('7'))
        self.ui.btn_8.clicked.connect(lambda: self.button_clicked('8'))
        self.ui.btn_9.clicked.connect(lambda: self.button_clicked('9'))
        
        # Operator buttons
        self.ui.btn_add.clicked.connect(lambda: self.button_clicked('+'))
        self.ui.btn_minus.clicked.connect(lambda: self.button_clicked('-'))
        self.ui.btn_multiply.clicked.connect(lambda: self.button_clicked('×'))
        self.ui.btn_divide.clicked.connect(lambda: self.button_clicked('÷'))
        self.ui.btn_decimal.clicked.connect(lambda: self.button_clicked('.'))
        
        # Function buttons
        self.ui.btn_output.clicked.connect(self.calculate)
        self.ui.btn_clear.clicked.connect(self.clear_last)
        self.ui.btn_clearall.clicked.connect(self.clear_all)
        self.ui.btn_module.clicked.connect(self.percentage)
        self.ui.btn_off.clicked.connect(self.close)
        
    def button_clicked(self, value):
        """Handles all button clicks"""
        self.current_expression += value
        self.ui.display.setText(self.current_expression)
        
    def clear_last(self):
        """Remove last character"""
        self.current_expression = self.current_expression[:-1]
        if not self.current_expression:
            self.ui.display.setText("0")
        else:
            self.ui.display.setText(self.current_expression)
        
    def clear_all(self):
        """Clear everything"""
        self.current_expression = ""
        self.ui.display.setText("0")
        
    def calculate(self):
        """Calculate the result"""
        if not self.current_expression:
            return
            
        try:
            # Replace × with * and ÷ with /
            expression = self.current_expression.replace('×', '*').replace('÷', '/')
            result = eval(expression)
            
            # Format result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
                    
            self.current_expression = str(result)
            self.ui.display.setText(self.current_expression)
            
        except ZeroDivisionError:
            self.ui.display.setText("Cannot divide by zero")
            self.current_expression = ""
        except Exception:
            self.ui.display.setText("Error")
            self.current_expression = ""
            
    def percentage(self):
        """Calculate percentage"""
        if not self.current_expression:
            return
            
        try:
            expression = self.current_expression.replace('×', '*').replace('÷', '/')
            result = eval(expression) / 100
            
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
                    
            self.current_expression = str(result)
            self.ui.display.setText(self.current_expression)
            
        except Exception:
            pass
            
    def keyPressEvent(self, event):
        """Handle keyboard input - including numpad"""
        key = event.key()
        
        # Regular number keys (0-9)
        if Qt.Key_0 <= key <= Qt.Key_9:
            self.button_clicked(chr(key))
        
        # Numpad numbers (16777248 to 16777257 in PyQt5)
        elif 16777248 <= key <= 16777257:
            num = str(key - 16777248)
            self.button_clicked(num)
        
        # Numpad operators
        elif key == Qt.Key_Plus:
            self.button_clicked('+')
        elif key == Qt.Key_Minus:
            self.button_clicked('-')
        elif key == Qt.Key_Asterisk:
            self.button_clicked('×')
        elif key == Qt.Key_Slash:
            self.button_clicked('÷')
        elif key == Qt.Key_Period:
            self.button_clicked('.')
        
        # Numpad Enter (16777220) and regular Enter/Return
        elif key in (Qt.Key_Enter, Qt.Key_Return):
            self.calculate()
        
        # Backspace
        elif key == Qt.Key_Backspace:
            self.clear_last()
        
        # Escape for clear all
        elif key == Qt.Key_Escape:
            self.clear_all()
        
        # Percent
        elif key == Qt.Key_Percent:
            self.percentage()
        
        # Equals key
        elif key == Qt.Key_Equal:
            self.calculate()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())