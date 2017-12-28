#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename:logger.py
import os
import logbook
from logbook import Logger, TimedRotatingFileHandler
from logbook.more import ColorizedStderrHandler

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.00"

def user_handler_log_formatter(record, handler):
    log = "[{dt}][{level}][{filename}][{func_name}][{lineno}] {msg}".format(
        dt=record.time,
        level=record.level_name,                       # Log level
        filename = os.path.split(record.filename)[-1], # File name
        func_name = record.func_name,                  # Function name
        lineno = record.lineno,                        # Line number
        msg=record.message,                            # Log content
    )
    return log

# Print to screen
user_std_handler = ColorizedStderrHandler(bubble=True)
user_std_handler.formatter = user_handler_log_formatter

# Log dir, Log dir will be generate at project root dir
LOG_DIR = os.path.join('log')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Print to file
user_file_handler = TimedRotatingFileHandler(
    os.path.join(LOG_DIR , '%s.log' % 'test_log'), date_format='%Y%m%d', bubble=True)
user_file_handler.formatter = user_handler_log_formatter
# Logger for user
user_log = Logger("user_log")
def init_logger():
    logbook.set_datetime_format("local")
    user_log.handlers = []
    user_log.handlers.append(user_std_handler)
    user_log.handlers.append(user_file_handler)

# Init log system
init_logger()


#!/usr/bin/evn python3
# -*- coding: utf-8 -*-
# filename: test_looger.py
import os
# from logger import user_log as logger
if __name__ == "__main__":
    user_log.info("my test.")
    user_log.error("test error!")