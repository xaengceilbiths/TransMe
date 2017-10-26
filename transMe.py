#!/usr/bin/python2
# -*- coding: utf-8 -*-
"""
Date     : 2016/07/19 18:55:56
FileName : transMe.py
Author   : septicmk
"""

import sys
import re
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication
from PyQt4.QtWebKit import QWebView
import youdao_dict as yd

import imgs_rc

class Info(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Info, self).__init__(parent)

        screen_resolution = QApplication.desktop().screenGeometry()
        self.area_width, self.area_height = screen_resolution.width(), screen_resolution.height()

        self.resize(460,420)
        self.setStyleSheet("background-color:#3B4141;")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.X11BypassWindowManagerHint)
        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Popup)

        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)

        self.web_view = QWebView()
        self.layout.addWidget(self.web_view)

        self.quitAction = QtGui.QAction("&Quit", self, triggered=QtGui.qApp.quit)
        self.on_offAction = QtGui.QAction("&Switch",self, triggered=self.on_off)
        self.trayIconMenu = QtGui.QMenu(self)
        
        self.trayIconMenu.addAction(self.on_offAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)
        self.trayIconMenu.setStyleSheet("color:#ffffff;font-size:18px")

        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setIcon(QtGui.QIcon(":/imgs/dictionary-icon.png"))
        self.trayIcon.show()
        self.cpb = QApplication.clipboard()
        self.cpb.selectionChanged.connect(self.query)

        self.flag = True

    def on_off(self):
        self.flag = not self.flag

    def leaveEvent(self, e):
        self.hide()

    def keyPressEvent(self, e):
        if e == QtCore.Qt.Key_F4:
            self.flag = False

    def query(self):
        if not self.flag:
            return
        #self.mut = QtCore.QMutex()
        #self.mut.lock()

        html= u'''
            <style type="text/css">
            body {
                font-family: Monaco, Consolas, "Lucida Console", monospace,"微软雅黑";
            }
            </style>
            <h2 style="color: #ffffff">
            Loading...
            </h2>
            '''
        self.web_view.setHtml(html)
        self.web_view.reload()

        pos = QtGui.QCursor.pos()
        posx, posy = pos.x(), pos.y()
        if posx+460+20 > self.area_width:
            posx = self.area_width - 460 - 20
        if posy+420+20 > self.area_height:
            posy = self.area_height - 420 - 20
        self.move(QtCore.QPoint(posx, posy))
        #self.move(QtGui.QCursor.pos())

        text=str(self.cpb.text(1).toUtf8())
        text=''.join(text.split('-\n'))
        text=''.join(re.split('[^a-zA-Z]*',text))
        if len(text) <= 3:
            text = ''
        translation,explains,web=yd.query(text)
        if translation == None:
            if text != '':
                if text[-1] == 's':
                    text=text[0:-1]
                    translation,explains,web=yd.query(text)
        if translation == None:
            self.hide()
            html = u'''
            <style type="text/css">
            body {
                font-family: Monaco, Consolas, "Lucida Console", monospace,"微软雅黑";
            }
            </style>
            <h2 style="color: #ffffff">
            None
            </h2>
            '''
        else:
            self.show()
            html = u'''
            <style type="text/css">
            body {
                font-family: Monaco, Consolas, "Lucida Console", monospace,"微软雅黑";
            }
            </style>
            <h2 style="color: #ffffff">
            %(translation)s
            </h2>

            <span style="color: #cccccc; font-weight: bold; font-size: 18px">● 基本翻译:</span>
            <p style="color: #eeeeee"> %(explains)s </p>

            <span style="color: #cccccc; font-weight: bold; font-size: 18px">● 网络释意:</span>
            <p style="color: #eeeeee"> %(web)s </p>''' % locals()
        self.web_view.setHtml(html)
        self.web_view.reload()
        #self.mut.unlock()
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    info = Info()
    #info.query()
    app.exec_()

