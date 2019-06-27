import logging
from logger import Log
import os
import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QApplication, QLineEdit, QMessageBox, QShortcut

from browser import run_script


def get_ui_file_for(ui_filename):
    """
    Finds the path for the specified UI file and returns it.

    Checks to see if the applcation is an executable. 
    (sys._MEIPASS is a temporary directory for PyInstaller)
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ui_filename)

    return os.path.join(os.path.dirname(os.path.realpath(__file__)), ui_filename)


UI_MainWindow, QtBaseClass = uic.loadUiType(get_ui_file_for('coupon.ui'))


class CouponApp(UI_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        QtWidgets.QMainWindow.__init__(self)
        UI_MainWindow.__init__(self)
        log= Log()
        log.basic_config(
            logfile_name='coupon',
            logfile_path='log',
            file_level= logging.INFO,
            console_level= logging.CRITICAL
        )
        log.get_logger()
        self.setupUi(self)
        self.setWindowTitle('Coupon')
        self.setWindowIcon(QIcon('publix.png'))
        self.run_button.clicked.connect(self.run)
        self.quit_button.clicked.connect(self.quit)
        self.quit_button.shortcut = QShortcut(QKeySequence('CTRL+Q'), self)
        self.quit_button.shortcut.activated.connect(self.quit)
        self.pass_toggle.toggled.connect(self.toggle_password)
        self.progressBar.hide()
        self.progressBar.setValue(0)
        self.update_status()

    def toggle_password(self):
        """Toggles the password bar"""
        if self.pass_toggle.isChecked():
            self.pass_input.setEchoMode(QLineEdit.Normal)
            logging.debug('Password Shown')

        else:
            self.pass_input.setEchoMode(QLineEdit.Password)
            logging.debug('Password Hidden')

    def get_data(self):
        """gets the username and password"""
        data = self.user_input.text(), self.user_input.text()

        if len(data[0]):
            logging.info('Username is "%s"', data[0])

        else:
            logging.info('Username was NOT entered')

        if len(data[1]):
            logging.info('Password exists')
            logging.debug('Password is "%s"', data[0])

        else:
            logging.info('Password was NOT entered')

        return data

    def data_empty(self):
        """Returns true if the data is empty"""
        if len(self.user_input.text()) or len(self.user_input.text()):
            logging.debug('Username and password boxes are full')
            return False

        logging.debug('Username and password boxes are empty')
        return True

    def clear_data(self):
        """Clears the username and password field"""
        self.user_input.clear()
        self.pass_input.clear()
        logging.debug('Cleared username and password')

    def toggle_data(self, toggle=True):
        """Toggles the username and password box"""
        if toggle:
            logging.debug('Username and password field are now ON')
            self.user_input.setEnabled(True)
            self.pass_input.setEnabled(True)
        else:
            logging.debug('Username and password field are now OFF')
            self.user_input.setEnabled(False)
            self.pass_input.setEnabled(False)

    def run(self):
        """runs the script"""
        logging.info('Run button pressed')
        value = 0

        if self.data_empty():
            self.update_status('Please enter a username and password')

        else:
            self.toggle_data(False)
            self.progressBar.show()
            self.update_status('Processing')

        # TODO Implement code here
            run_script(self.get_data()[0], self.get_data()[1])
            self.get_data()
            while value < 100:
                value += 0.00001
                self.progressBar.setValue(value)

            self.clear_data()
            self.toggle_data()
            self.update_status('Done')
            QMessageBox.about(self, 'Done', 'Enjoy Shopping')

    def get_widgets(self):
        """returns a list of widgets"""
        widgets = [self.title,
                   self.info,
                   self.user_label,
                   self.pass_label,
                   self.pass_toggle,
                   self.run_button,
                   self.quit_button]
        print('grabbed widgets')

        return widgets

    def update_status(self, text='Ready'):
        """Updates the status bar text at the bottom of the app"""
        self.statusBar().showMessage(text)

    def quit(self):
        """quits the app"""
        logging.debug('Quit button pressed')
        QApplication.quit()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = CouponApp()
    window.show()
    logging.debug('Main window shown')
    app.exec_()


if __name__ == '__main__':
    main()
