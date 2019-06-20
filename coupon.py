import os
import sys
from datetime import datetime
import logging

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QLineEdit

# has to be in local file as it uses the path from where the class is located


def get_ui_file_for(ui_filename):
    '''
    Finds the path for the specified UI file and returns it.

    Checks to see if the applcation is an executable. 
    (sys._MEIPASS is a temporary directory for PyInstaller)
    '''
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ui_filename)

    return os.path.join(os.path.dirname(os.path.realpath(__file__)), ui_filename)

UI_MainWindow, QtBaseClass = uic.loadUiType(get_ui_file_for('coupon.ui'))

class CouponApp(UI_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        QtWidgets.QMainWindow.__init__(self)
        UI_MainWindow.__init__(self)
        self.setupUi(self)
        setup_logging(self, logname='coupon', level=logging.DEBUG)

        self.run_button.clicked.connect(self.run)
        self.quit_button.clicked.connect(self.quit)
        self.pass_toggle.toggled.connect(self.toggle_password)
        self.progressBar.hide()
        self.progressBar.setValue(0)
        self.update_status()

    def toggle_password(self):
        '''Toggles the password bar'''
        if self.pass_toggle.isChecked():
            self.pass_input.setEchoMode(QLineEdit.Normal)
            logging.debug(' Password Shown')
        else:
            self.pass_input.setEchoMode(QLineEdit.Password)
            logging.debug(' Password Hidden')
    
    def get_data(self):
        '''gets the username and password'''
        data= self.user_input.text(), self.user_input.text()
        
        if len(data[0]):
            logging.info(' Username is "%s"', data[0])
        else:
            logging.info(' Username was NOT entered')

        if len(data[1]):
            logging.info(' Password exists')
            logging.debug(' Password is "%s"', data[0])
            
        else:
            logging.info(' Password was NOT entered')

        return data
    
    def clear_data(self):
        self.user_input.clear()
        self.pass_input.clear()
        logging.debug(' Cleared username and password')

    def run(self):
        '''runs the script'''
        self.user_input.setEnabled(False)
        self.pass_input.setEnabled(False)
        self.progressBar.show()
        self.update_status('Processing')

        value= 0

# TODO Implement code here
        self.get_data()

        while value < 100:
            value += 0.00001
            self.progressBar.setValue(value)

        self.clear_data()
        self.user_input.setEnabled(True)
        self.pass_input.setEnabled(True)
        self.update_status('Done')

        logging.info(' Run button pressed')

    def get_widgets(self):
        '''returns a list of widgets'''
        widgets = [self.title,
                self.info,
                self.user_label,
                self.pass_label,
                self.pass_toggle,
                self.run_button,
                self.quit_button]
        print('grabbed widgets')
        return widgets

    def update_status(self, text='Enter Data'):
        self.statusBar().showMessage(text)
    
    def quit(self):
        '''quits the app'''
        logging.debug(' Quit button pressed')
        QApplication.quit()

def get_time():
    '''returns current time'''
    now= datetime.now()
    # current_datetime_formatstring= now.strftime("%d/%m/%Y %H:%M:%S")
    current_datetime_formatstring= now.strftime("_%d-%m-%Y__%I_%M_%S_%p")
    return current_datetime_formatstring

def setup_logging(self, logname='default', level=logging.INFO):
    file= logname + get_time() +'.log'
    logging.basicConfig(filename=file ,level=level, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.debug(' Logging file created')

def main():
    main_window = CouponApp()
    main_window.show()
    # sys.exit(main_app)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = CouponApp()
    window.show()
    logging.debug(' Main window shown')
    sys.exit(app.exec_())
