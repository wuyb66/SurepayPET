'''Wrapper for logging.'''

import log
import functools
import sys
import os.path

def logged (level, message):
    log_funcs = {'debug':log.debug, 'info':log.info, 'warning':log.warning,
                 'error':log.error, 'critical':log.critical,'exception':log.exception}


    def outputMessage(f,*args,**kargs):
        str = '%s called, args: %r, kargs:%r, - %s'%(f.__name__,args,kargs,message)
        return str

    def pre_logged(f):
        @functools.wraps(f)
        def wrapper(*args,**kargs):
            func = log_funcs.get(level, log.info)
            func(outputMessage(f,args,kargs))
            return f(*args,**kargs)
        return wrapper
    return pre_logged

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