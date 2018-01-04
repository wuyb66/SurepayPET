#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename:logger.py
import os
import logbook
from logbook import Logger, TimedRotatingFileHandler
from logbook.more import ColorizedStderrHandler
import functools
import sys
import os.path

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.00"

# Global logger
g_logger = None

def user_handler_log_formatter(record, handler):
    # '[%(levelname)-8s] - %(asctime)s - [%(process)d:%(thread)d] - %(message)s',
    log = "[{dt}][{level:<8}][{filename}][{func_name}][{lineno:>4}] - {msg}".format(
        dt=record.time,
        level=record.level_name,                       # Log level
        filename = os.path.split(record.filename)[-1], # File name
        func_name = record.func_name,                  # Function name
        lineno = record.lineno,                        # Line number
        msg=record.message,                            # Log content
    )
    return log

def logged (level, message):
    log_funcs = {'debug':g_logger.debug, 'info':g_logger.info, 'warning':g_logger.warning,
                 'error':g_logger.error, 'critical':g_logger.critical,'exception':g_logger.exception}


    def outputMessage(f,*args,**kargs):
        str = '%s called, args: %r, kargs:%r, - %s'%(f.__name__,args,kargs,message)
        return str

    def pre_logged(f):
        @functools.wraps(f)
        def wrapper(*args,**kargs):
            func = log_funcs.get(level, g_logger.info)
            retval = f(*args,**kargs)
            func(outputMessage(f,args,kargs) + ' - return: %s'%retval)
            return retval
        return wrapper
    return pre_logged

# Print to screen
user_std_handler = ColorizedStderrHandler(bubble=True)
user_std_handler.formatter = user_handler_log_formatter

# Log dir, Log dir will be generate at project root dir
LOG_DIR = os.path.join('log')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Print to file
user_file_handler = TimedRotatingFileHandler(
    os.path.join(LOG_DIR , '%s.log' % 'pet_log'), date_format='%Y%m%d', bubble=True)
user_file_handler.formatter = user_handler_log_formatter
# Logger for user
user_log = Logger("user_log")

def init_logger():
    '''Reload the global logger.'''
    global g_logger

    if g_logger is None:
        g_logger = Logger ('Surepay PET Log')
    else:
        g_logger.handlers = []

def import_log_funcs():
    '''Import the common log functions from the global logger to the module.'''
    global g_logger

    curr_mod = sys.modules[__name__]
    log_funcs = ['debug', 'info', 'warning', 'error', 'critical',
                 'exception']

    for func_name in log_funcs:
        func = getattr(g_logger, func_name)
        setattr(curr_mod, func_name, func)

def set_logger():
    global g_logger
    init_logger()
    logbook.set_datetime_format("local")
    g_logger.handlers = []
    # g_logger.handlers.append(user_std_handler)
    g_logger.handlers.append(user_file_handler)
    import_log_funcs()

# Init log system
set_logger()


@logged('info','%s[line:%4s], %s'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1, sys._getframe(0).f_code.co_name))
def hello(name):
    print("hello", name)


@logged('debug', 'debug test')
def test(a, b=1):
    print(a + b)

@logged('abc', 'abc test')
def test2(a, b=2):
    print(a + b)

@logged('abc', 'abc test')
def test3():
    print('test3')

class aaa:
    @logged('info', '%s[line:%4s], %s' % (os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1, sys._getframe(0).f_code.co_name))
    def __init__(self):
        pass

    @logged('info', '%s[line:%4s], %s' % (os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1, sys._getframe(0).f_code.co_name))
    def bbb(self):
        pass

if __name__ == '__main__':
    hello("world")
    test(1, 2)
    test2(3)
    test3()
    hello("world2")
    test(2, 4)
    test2(6)
    test3()
    x = aaa()
    x.bbb()
    g_logger.info("my test.")
    g_logger.error("test error!")