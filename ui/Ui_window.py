# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'window.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(892, 642)
        self.action1 = QAction(MainWindow)
        self.action1.setObjectName(u"action1")
        self.action1_2 = QAction(MainWindow)
        self.action1_2.setObjectName(u"action1_2")
        self.action3 = QAction(MainWindow)
        self.action3.setObjectName(u"action3")
        self.action4 = QAction(MainWindow)
        self.action4.setObjectName(u"action4")
        self.action1_3 = QAction(MainWindow)
        self.action1_3.setObjectName(u"action1_3")
        self.action1_4 = QAction(MainWindow)
        self.action1_4.setObjectName(u"action1_4")
        self.action1_5 = QAction(MainWindow)
        self.action1_5.setObjectName(u"action1_5")
        self.action2_2 = QAction(MainWindow)
        self.action2_2.setObjectName(u"action2_2")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(9, 9, 268, 60))
        self.label_4.setMinimumSize(QSize(0, 60))
        font = QFont()
        font.setFamilies([u"\u9ed1\u4f53"])
        font.setPointSize(28)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet(u"")
        self.label_4.setAlignment(Qt.AlignCenter)
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(783, 429, 75, 25))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        self.pushButton_2.setFont(font1)
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit = QLineEdit(self.widget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 30))
        self.lineEdit.setFont(font1)

        self.verticalLayout.addWidget(self.lineEdit)

        self.listWidget = QListWidget(self.widget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setMinimumSize(QSize(150, 0))

        self.verticalLayout.addWidget(self.listWidget)

        self.verticalLayout.setStretch(0, 3)
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(390, 360, 256, 192))
        self.textEdit.setReadOnly(True)
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(323, 58, 491, 271))
        self.groupBox.setMinimumSize(QSize(210, 120))
        self.groupBox.setFont(font1)
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(28, 100, 52, 17))
        self.lineEdit_2 = QLineEdit(self.groupBox)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(90, 100, 149, 21))
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(28, 130, 52, 17))
        self.lineEdit_3 = QLineEdit(self.groupBox)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setGeometry(QRect(90, 130, 149, 21))
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(30, 30, 52, 17))
        self.comboBox = QComboBox(self.groupBox)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(100, 30, 68, 22))
        self.lineEdit_5 = QLineEdit(self.groupBox)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setGeometry(QRect(100, 240, 149, 21))
        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(38, 240, 52, 17))
        self.lineEdit_6 = QLineEdit(self.groupBox)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setGeometry(QRect(90, 200, 149, 21))
        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(33, 200, 61, 20))
        self.lineEdit_7 = QLineEdit(self.groupBox)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        self.lineEdit_7.setGeometry(QRect(80, 60, 149, 21))
        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(23, 60, 61, 20))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(690, 430, 75, 25))
        self.pushButton.setFont(font1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 892, 22))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_C = QMenu(self.menubar)
        self.menu_C.setObjectName(u"menu_C")
        self.menu_2 = QMenu(self.menu_C)
        self.menu_2.setObjectName(u"menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.comboBox, self.lineEdit_7)
        QWidget.setTabOrder(self.lineEdit_7, self.lineEdit_2)
        QWidget.setTabOrder(self.lineEdit_2, self.lineEdit_3)
        QWidget.setTabOrder(self.lineEdit_3, self.lineEdit_6)
        QWidget.setTabOrder(self.lineEdit_6, self.lineEdit_5)
        QWidget.setTabOrder(self.lineEdit_5, self.lineEdit)
        QWidget.setTabOrder(self.lineEdit, self.textEdit)
        QWidget.setTabOrder(self.textEdit, self.pushButton)
        QWidget.setTabOrder(self.pushButton, self.listWidget)
        QWidget.setTabOrder(self.listWidget, self.pushButton_2)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_C.menuAction())
        self.menu.addAction(self.action1)
        self.menu_C.addAction(self.action1_2)
        self.menu_C.addAction(self.menu_2.menuAction())
        self.menu_C.addAction(self.action3)
        self.menu_C.addAction(self.action4)
        self.menu_2.addAction(self.action1_3)
        self.menu_2.addAction(self.action2_2)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action1.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u7a97\u53e3", None))
#if QT_CONFIG(shortcut)
        self.action1.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.action1_2.setText(QCoreApplication.translate("MainWindow", u"\u89d2\u63a5\u89e6\u7403\u8f74\u627f", None))
        self.action3.setText(QCoreApplication.translate("MainWindow", u"\u5706\u67f1\u6eda\u5b50\u8f74\u627f", None))
        self.action4.setText(QCoreApplication.translate("MainWindow", u"\u5706\u9525\u6eda\u5b50\u8f74\u627f", None))
        self.action1_3.setText(QCoreApplication.translate("MainWindow", u"\u8f7b\u7cfb\u5217\u8f74\u627f\uff08619\u3001618\u3001160\uff09", None))
        self.action1_4.setText(QCoreApplication.translate("MainWindow", u"\u6d4b\u8bd5\u4f7f\u7528", None))
        self.action1_5.setText(QCoreApplication.translate("MainWindow", u"\u5806\u53e0\u6d4b\u8bd5", None))
        self.action2_2.setText(QCoreApplication.translate("MainWindow", u"\u6df1\u6c9f\u7403\u8f74\u627f\uff080\u30011\u30012\u30013\u30014\u3001\uff09", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Bstart-CAD\u6a21\u5757", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8f74\u627f\u578b\u53f7\u7b5b\u9009", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u53c2\u6570\u8f93\u5165", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u8f74\u627f\u5185\u5f84", None))
        self.lineEdit_2.setText(QCoreApplication.translate("MainWindow", u"95", None))
        self.lineEdit_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"mm", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u8f74\u627f\u5916\u5f84", None))
        self.lineEdit_3.setText(QCoreApplication.translate("MainWindow", u"170", None))
        self.lineEdit_3.setPlaceholderText(QCoreApplication.translate("MainWindow", u"mm", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u8f74\u627f\u5185\u5f84", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"P0", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"P2", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"P4", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"P5", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"P6", None))

        self.lineEdit_5.setText(QCoreApplication.translate("MainWindow", u"15", None))
        self.lineEdit_5.setPlaceholderText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u63a5\u89e6\u89d2", None))
        self.lineEdit_6.setText(QCoreApplication.translate("MainWindow", u"32", None))
        self.lineEdit_6.setPlaceholderText(QCoreApplication.translate("MainWindow", u"mm", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u8f74\u627f\u5bbd\u5ea6", None))
        self.lineEdit_7.setText(QCoreApplication.translate("MainWindow", u"7200", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u8f74\u627f\u540d", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u51fa\u56fe", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u64cd\u4f5c (&O)", None))
        self.menu_C.setTitle(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u8f74\u627f\u578b\u53f7 (&C)", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\u6df1\u6c9f\u7403\u8f74\u627f", None))
    # retranslateUi
