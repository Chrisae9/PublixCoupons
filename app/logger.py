import logging
import os
import sys

from datetime import datetime
from logging import FileHandler
from os import path

"""
To use import, configure, get the logger and start writing messages!

    log= Log()

    log.basic_config(
        logfile_name='coupon',
        logfile_path='log',
        file_level= logging.INFO,
        console_level= logging.CRITICAL
    )

    log.get_logger()

    log.info('This is an info message')

    log.debug('This is a debug message')

-- Chris Alves
"""


class Log:
    def __init__(self):
        self.logger_name = ''
        self.logfile_name = 'log'
        self.logfile_path = 'logs'

        # Levels: NOTSET= 0 DEBUG= 10 INFO= 20 WARNING= 30 ERROR= 40 CRITICAL= 50
        self.file_level = logging.INFO
        self.console_level = logging.CRITICAL

        self.console_format = logging.Formatter(
            "%(levelname)s: %(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")

        self.file_format = logging.Formatter(
            "%(levelname)s: %(funcName)s %(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")

        self.file_timeformat = "_%m-%d-%Y__%I_%M_%S_%p"

    def basic_config(self, logger_name='', logfile_name='log', logfile_path='logs',
                     file_level=logging.INFO, console_level=logging.CRITICAL):
        """A quick wat to configure the logger without formatting"""
        self.logger_name = logger_name
        self.logfile_name = logfile_name
        self.logifle_path = logfile_path
        self.file_level = file_level
        self.console_level = console_level

    def get_logger(self):
        """Configures the main logger"""
        logger = logging.getLogger(self.logger_name)
        # better to have too much log than not enough
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.get_console_handler())
        logger.addHandler(self.get_file_handler())
        # with this pattern, it's rarely necessary to propagate the error up to parent
        logger.propagate = False

        return logger

    def get_file_handler(self):
        """Configures the file handler"""

        file = self.logfile_name + self.get_time() + '.log'
        file_handler = BetterFileHandler(self.logfile_path, file, 'a')
        file_handler.setLevel(self.file_level)
        file_handler.setFormatter(self.file_format)

        return file_handler

    def get_console_handler(self):
        """Configures the console handler"""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.console_level)
        console_handler.setFormatter(self.console_format)

        return console_handler

    def get_time(self):
        """Returns current time"""
        return datetime.now().strftime(self.file_timeformat)


class BetterFileHandler(FileHandler):
    """Fixes path issues with File Handler"""

    def __init__(self, log_file_dir, filename, mode):
        # if this file is moved edit here
        root_dir = path.abspath(path.join(path.dirname(path.realpath(__file__)), ''))
        full_path = path.abspath(path.join(root_dir, log_file_dir))

        if not path.exists(full_path):
            os.mkdir(full_path)

        super(BetterFileHandler, self).__init__(full_path + '/' + filename, mode)
