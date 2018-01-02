# encoding: UTF-8

import sys
import os
import ctypes
import platform

import vtPath
from vtEngine import MainEngine
from uiMainWindow import *
import log
from logged import logged

# 文件路径名
path = os.path.abspath(os.path.dirname(__file__))    
ICON_FILENAME = 'vnpy.ico'
ICON_FILENAME = os.path.join(path, ICON_FILENAME)  

SETTING_FILENAME = 'VT_setting.json'
SETTING_FILENAME = os.path.join(path, SETTING_FILENAME)  

#----------------------------------------------------------------------
@logged('info','%s[line:%4s]'%(os.path.split(sys._getframe().f_code.co_filename)[1], sys._getframe().f_lineno + 1))
def main():
    """主程序入口"""
    # 重载sys模块，设置默认字符串编码方式为utf8
    reload(sys)
    sys.setdefaultencoding('utf8')

    
    # 设置Windows底部任务栏图标
    if 'Windows' in platform.uname() :
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('vn.trader')  
    
    # 初始化Qt应用对象
    log.info('Init Qt Application')
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(ICON_FILENAME))
    app.setFont(BASIC_FONT)
    
    # 设置Qt的皮肤
    try:
        log.info('Set application skin')
        f = file(SETTING_FILENAME)
        setting = json.load(f)    
        if setting['darkStyle']:
            import qdarkstyle
            log.info('Use dark style')
            app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    except:
        pass
    
    # 初始化主引擎和主窗口对象
    log.info('Init main engine')
    mainEngine = MainEngine()
    log.info('Init main window')
    mainWindow = MainWindow(mainEngine, mainEngine.eventEngine)
    mainWindow.showMaximized()
    mainEngine.dbConnect()
    mainEngine.connect('CTP')
    # 在主线程中启动Qt事件循环
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
