import sys
import os
import PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget,QPushButton, QLabel, QFileDialog, QFrame, QTextEdit
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import QRect,Qt,pyqtSlot,QCoreApplication
import user
import mr_globel as gl


create_qt_application = lambda : QApplication(sys.argv)
'''
----------------------------------------------
                MR测试程序                      
    配置文件：      查看， 修改
    MR路径：   ...
    输出路径： ...
    show：
        .......
'''


exit_qt_application = lambda argv:sys.exit(argv)

class mr_ui_window(QMainWindow):
    conf_path = '.\\source\\conf.xml'
    mr_path = '.\\mr'
    output_path = '.\\output'

    def __init__(self):
        super().__init__()
        self.init_slot_map()
        self.init_ui()
    def init_ui(self):

        self.resize(1200, 800)
        self.center()
        self.setWindowTitle('mr test')
        self.setWindowIcon(QIcon('.\\source\\favicon.ico'))
        #标题
        self.label('mr_title',QRect(450,0,300,100), 'mr测试程序',QFont('微软雅黑', 20, QFont.Bold), PyQt5.QtCore.Qt.AlignCenter)
        self.text = self.text_edit('line', QRect(100, 220, 1000, 400))

        #conf.xml
        self.check_conf_xml()
        self.label('conf',QRect(100, 100, 100, 30), '配置文件:', QFont('微软雅黑', 14, QFont.Bold))
        self.conf_path_label = self.label('conf_path',QRect(200, 100, 700, 30), self.conf_path, QFont('Consolas', 14, QFont.Normal))
        self.conf_path_label.setFrameShape(QFrame.Box)
        self.push_button('conf_read',QRect(910, 100, 50, 30), '查看')
        self.conf_change_button = self.push_button('conf_write',QRect(980, 100, 70, 30), '确认修改')
        self.conf_change_button.setEnabled(False)
        #mr_path
        self.label('mr_path', QRect(100, 140, 100, 30), 'MR路径:', QFont('微软雅黑', 14, QFont.Bold))
        self.mr_path_label = self.label('mr_path_value', QRect(200, 140, 700, 30), self.mr_path, QFont('Consolas', 14, QFont.Normal))
        self.mr_path_label.setFrameShape(QFrame.Box)
        self.push_button('mr_path_find', QRect(910, 140, 50, 30), '浏览')
        #output_path
        self.label('output', QRect(100, 180, 100, 30), '输出路径:', QFont('微软雅黑', 14, QFont.Bold))
        self.output_path_label = self.label('output_path', QRect(200, 180, 700, 30), self.output_path, QFont('Consolas', 14, QFont.Normal))
        self.output_path_label.setFrameShape(QFrame.Box)
        self.push_button('output_path_find', QRect(910, 180, 50, 30), '浏览')

        #start test push_button
        self.test_push_button = self.push_button('test_push_button', QRect(910, 650, 70, 30), '开始测试')
        self.cat_data_button = self.push_button('cat_data_button', QRect(990, 650, 70, 30), '查看结果')
        self.cat_data_button.setEnabled(False)
        self.quit_push_button = self.push_button('quit_push_button', QRect(990, 690, 70, 30), 'QUIT')

        self.show()

    def init_slot_map(self):
        self.slot_map_dict = {'conf_read':lambda :self.read_conf_file(), 'conf_write':lambda :self.write_conf_file(), 'mr_path_find':lambda :self.select_mr_file_path(),\
                              'output_path_find':lambda :self.select_output_file_path(), 'test_push_button':lambda :self.mr_test_start(), \
                              'quit_push_button':lambda :QCoreApplication.instance().quit(), 'cat_data_button':lambda :self.cat_data_file()}
    def center(self):
        qrect = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qrect.moveCenter(cp)
        self.move(qrect.topLeft())

    def closeEvent(self, event):
        reply = PyQt5.QtWidgets.QMessageBox.question(self,
            'Message', 'Are you quit?', PyQt5.QtWidgets.QMessageBox.Yes | PyQt5.QtWidgets.QMessageBox.No,
                                        PyQt5.QtWidgets.QMessageBox.No)
        if reply == PyQt5.QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def label(self,name, rect, text, font=QFont('Consolas', 10, QFont.Bold), pos=Qt.AlignLeft):
        label1 = QLabel(self)
        label1.setObjectName(name)
        label1.setText(text)
        label1.setGeometry(rect)
        label1.setFont(font)
        label1.setAutoFillBackground(True)
        palette = PyQt5.QtGui.QPalette()
        #palette.setColor(PyQt5.QtGui.QPalette.Window, PyQt5.QtCore.Qt.white)
        #label1.setPalette(self.palette)
        label1.setAlignment(pos)
        return label1

    def push_button(self, name, rect, text):
        push_button1 = QPushButton(self)
        push_button1.setObjectName(name)
        push_button1.setText(text)
        push_button1.setGeometry(rect)
        push_button1.clicked.connect(self.slot_map_dict[name])
        return push_button1

    def text_edit(self, name, rect):
        text = QTextEdit(self)
        text.setObjectName(name)
        text.setGeometry(rect)
        return text

    def read_conf_file(self):
        self.text.clear()
        with open(self.conf_path, encoding='UTF8') as file_object:
            contents = file_object.read()
            self.text.append(contents)
        self.text.verticalScrollBar().setValue(self.text.verticalScrollBar().minimum())
        self.conf_change_button.setEnabled(True)

    def write_conf_file(self):
        info = self.text.toPlainText()
        with open(self.conf_path,'w', encoding='UTF8') as file_object:
            file_object.write(info)
        self.conf_change_button.setEnabled(False)
        self.text.clear()
        self.text.append('changed ok...')

    def select_mr_file_path(self):
        self.mr_path = QFileDialog.getExistingDirectory(self, '浏览', '.\\')
        if self.mr_path == '':
            self.mr_path = '.\\mr'
        self.mr_path_label.setText(self.mr_path)

    def select_output_file_path(self):
        self.output_path = QFileDialog.getExistingDirectory(self, '浏览', '.\\')
        if self.output_path == '':
            self.output_path = '.\\output'
        self.output_path_label.setText(self.output_path)

    def getText(self):
        return self.text

    def mr_test_start(self):
        try:
            self.text.clear()
            self.text.append('test start...')
            self.test_push_button.setEnabled(False)
            gl.MR_TEST_PATH = self.mr_path + '\\'
            gl.OUTPUT_PATH = self.output_path + '\\'

            user.mr_test_process()

            self.text.append('test ok')
            for i in range(len(gl.str_info)):
                self.text.append(gl.str_info[i])
            gl.str_info.clear()

        except Exception as result:
            self.text.append ('mr test err <%s> -%s- :'%(result, str(result.__traceback__.tb_lineno)))
        self.cat_data_button.setEnabled(True)
        self.test_push_button.setEnabled(True)
    def cat_data_file(self):
        file_name = os.path.join(self.output_path, 'data.txt')
        os.startfile(file_name)

    def check_conf_xml(self):
        if os.path.exists(self.conf_path) == False:
            with open(self.conf_path, 'w', encoding='UTF8') as file_object:
                file_object.write(gl.CONF_XML_DATA)

# write_info = lambda info:mr_ui_window.getText().append(info)

