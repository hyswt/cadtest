from PySide6.QtWidgets import QApplication
from module import window

app = QApplication()
mywindow = window.MyWindow()
mywindow.show()
app.exec()
