"""Logs module"""
import logging


class Datalog:
    """Create, save, show and clear log"""

    def __init__(self):
        """Create logger"""
        self.logger = logging.getLogger(__name__)

    def logger_set(self):
        """Create logger to save and output info about games"""
        self.logger.setLevel(logging.INFO)
        log_handler = logging.FileHandler('logs/logging.log')
        log_handler.setLevel(logging.INFO)
        format_log = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S %p')
        log_handler.setFormatter(format_log)
        self.logger.addHandler(log_handler)

    @staticmethod
    def show_log_file():
        """Open reed and show the logging file in little messagebox windows"""
        with open('logs/logging.log', 'r', encoding='utf-8') as read_f:
            last_l = read_f.read()
        print(last_l)

    @staticmethod
    def clear_log_file():
        """Clear the logging file"""
        with open('logs/logging.log', 'w', encoding='utf-8') as clear_f:
            clear_f.write("")

    def save_logs(self, info):
        """Save log file"""
        self.logger.info(info)
