import json
import sys
from typing import Union

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidgetItem

from Table_results import *

app = QtWidgets.QApplication(sys.argv)
Form = QtWidgets.QWidget()

mt = {}


def calc():
    n1 = ui.lineEdit_1.text().strip()
    n2 = ui.lineEdit_2.text().strip()
    if n1 == '' or n2 == '':
        msg: Union[QMessageBox, QMessageBox] = QMessageBox()
        if n1 == '' and n2 != '':
            msg.setText('Перша лінійка не заповнена!')
        elif n1 != '' and n2 == '':
            msg.setText('Друга лінійка не заповнена!')
        else:
            msg.setText('Обидві лінійки не заповнені!')
        msg.setWindowTitle('Помилка вводу')
        msg.setIcon(QMessageBox.Critical)
        msg.exec()
        return
    if n1 == n2:
        msg = QMessageBox()
        msg.setText('Імена команд повинні бути різні!')
        msg.setWindowTitle('Помилка вводу')
        msg.setIcon(QMessageBox.Critical)
        msg.exec()
        return
    g1 = ui.spinBox_1.value()
    g2 = ui.spinBox_2.value()
    if n1 in mt:
        if g1 > g2:
            mt[n1][0] += 1
        elif g1 == g2:
            mt[n1][1] += 1
        else:
            mt[n1][2] += 1
    else:
        mt[n1] = [0, 0, 0]
        if g1 > g2:
            mt[n1][0] += 1
        elif g1 == g2:
            mt[n1][1] += 1
        else:
            mt[n1][2] += 1
    if n2 in mt:
        if g1 < g2:
            mt[n2][0] += 1
        elif g1 == g2:
            mt[n2][1] += 1
        else:
            mt[n2][2] += 1
    else:
        mt[n2] = [0, 0, 0]
        if g1 < g2:
            mt[n2][0] += 1
        elif g1 == g2:
            mt[n2][1] += 1
        else:
            mt[n2][2] += 1
    update()


def update():
    mtl = list(mt.items())
    n = len(mtl)
    ui.tableWidget.setRowCount(len(mt))
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if mtl[j][1][0] * 3 + mtl[j][1][1] * 1 < mtl[j + 1][1][0] * 3 + mtl[j + 1][1][1] * 1:
                mtl[j], mtl[j + 1] = mtl[j + 1], mtl[j]
    i = 0
    for key, value in mtl:
        ui.tableWidget.setItem(i, 0, QTableWidgetItem(key))
        ui.tableWidget.setItem(i, 1, QTableWidgetItem(str(sum(value))))
        ui.tableWidget.setItem(i, 2, QTableWidgetItem(str(value[0])))
        ui.tableWidget.setItem(i, 3, QTableWidgetItem(str(value[1])))
        ui.tableWidget.setItem(i, 4, QTableWidgetItem(str(value[2])))
        ui.tableWidget.setItem(i, 5, QTableWidgetItem(str(value[0] * 3 + value[1] * 1)))
        i += 1


def load():
    global mt
    fd = QFileDialog()
    fname = fd.getOpenFileName(caption='Open file', filter='(*.txt)')[0]
    if fname == '':
        msg = QMessageBox()
        msg.setText('Дані не завантажені')
        msg.setWindowTitle('Помилка завантаження')
        msg.setIcon(QMessageBox.Information)
        msg.exec()
        return
    with open(fname, 'r') as fo:
        mt = json.load(fo)
    update()


def upload():
    fd = QFileDialog()
    fname = fd.getSaveFileName(caption='Open file', directory='Results.txt')[0]
    if fname == '':
        msg = QMessageBox()
        msg.setText('Дані не вивантажені')
        msg.setWindowTitle('Помилка вивантаження')
        msg.setIcon(QMessageBox.Information)
        msg.exec()
        return
    with open(fname, 'w') as fo:
        json.dump(mt, fo)


Form.calc = calc

Form.load = load
Form.upload = upload
ui = Ui_Form()
ui.setupUi(Form)

ui.tableWidget.setColumnCount(6)
ui.tableWidget.setColumnWidth(0, 125)
ui.tableWidget.setColumnWidth(1, 65)
ui.tableWidget.setColumnWidth(2, 65)
ui.tableWidget.setColumnWidth(3, 65)
ui.tableWidget.setColumnWidth(4, 65)
ui.tableWidget.setColumnWidth(5, 65)
ui.tableWidget.setHorizontalHeaderLabels(['Команда', 'К-сть ігор', 'В', 'Н', 'П', 'Очки'])

Form.show()
sys.exit(app.exec_())
