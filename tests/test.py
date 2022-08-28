from datetime import datetime
import os
# from pywin32_system32 import win32con, win32gui, wi
import win32con
import win32api
import win32gui
import sys
import time


#
# def test_AssertTrue():
#     assert False


def log_info(msg):
    """ Prints """
    print(msg)
    f = open("c:\\Users\\w34450\\test.log", "a")
    f.write(msg + "\n")
    f.close()


def wndproc(hwnd, msg, wparam, lparam):
    log_info("wndproc: %s" % msg)


if __name__ == "__main__":
    log_info("*** STARTING ***")
    hinst = win32api.GetModuleHandle(None)
    wndclass = win32gui.WNDCLASS()
    wndclass.hInstance = hinst
    wndclass.lpszClassName = "testWindowClass"
    messageMap = {win32con.WM_QUERYENDSESSION: wndproc,
                  win32con.WM_ENDSESSION: wndproc,
                  win32con.WM_QUIT: wndproc,
                  win32con.WM_DESTROY: wndproc,
                  win32con.WM_CLOSE: wndproc}

    wndclass.lpfnWndProc = messageMap

    try:
        myWindowClass = win32gui.RegisterClass(wndclass)
        hwnd = win32gui.CreateWindowEx(win32con.WS_EX_LEFT,
                                       myWindowClass,
                                       "testMsgWindow",
                                       0,
                                       0,
                                       0,
                                       win32con.CW_USEDEFAULT,
                                       win32con.CW_USEDEFAULT,
                                       win32con.HWND_MESSAGE,
                                       0,
                                       hinst,
                                       None)
    except Exception as e:
        log_info("Exception: %s" % str(e))

    if hwnd is None:
        log_info("hwnd is none!")
    else:
        log_info("hwnd: %s" % hwnd)

    while True:
        win32gui.PumpWaitingMessages()
        time.sleep(1)


#
# def test():
#     assert True
#
# print(type(datetime.now()))
# print(str(datetime.now()))
