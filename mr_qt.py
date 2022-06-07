import re
import sys
import os
import time

import PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget,QPushButton, QLabel, QFileDialog, QFrame, QTextEdit, QWidget, QDialog, QSpinBox, QLineEdit, QProgressBar,\
            QCheckBox, QRadioButton, QGroupBox, QHBoxLayout, QVBoxLayout, QComboBox, QScrollArea
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import QRect,Qt,pyqtSlot,QCoreApplication
import user
import mr_globel as gl
import paramiko
import mr_utils as ut


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



class mr_qt_kit:
    @staticmethod
    def label(object,name, rect, text, font=QFont('Consolas', 10, QFont.Bold), pos=Qt.AlignLeft):
        label1 = QLabel(object)
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
    @staticmethod
    def push_button(object, name, rect, text, method):
        push_button1 = QPushButton(object)
        push_button1.setObjectName(name)
        push_button1.setText(text)
        push_button1.setGeometry(rect)
        push_button1.clicked.connect(method)
        return push_button1
    @staticmethod
    def text_edit(object, name, rect, data=''):
        text = QTextEdit(object)
        text.setObjectName(name)
        text.setGeometry(rect)
        text.setText(data)
        return text
    @staticmethod
    def line_edit(object, name, rect, data='', echomode=QLineEdit.Normal):
        line = QLineEdit(object)
        line.setObjectName(name)
        line.setGeometry(rect)
        line.setText(data)
        line.setEchoMode(echomode)
        return line
    @staticmethod
    def spinbox(object, name, rect, data=0, range=(0, 1000), step=1):
        box = QSpinBox(object)
        box.setObjectName(name)
        box.setGeometry(rect)
        box.setRange(*range)
        box.setValue(data)
        box.setSingleStep(step)
        return box
    @staticmethod
    def progress_bar(object, name, rect, value=0, range=(0,100)):
        pro_bar = QProgressBar(object)
        pro_bar.setObjectName(name)
        pro_bar.setGeometry(rect)
        pro_bar.setValue(value)
        pro_bar.setRange(*range)
        return pro_bar
    @staticmethod
    def checkbox(object, name, rect, data, is_ckd=False):
        ckbox = QCheckBox(object)
        ckbox.setObjectName(name)
        ckbox.setGeometry(rect)
        ckbox.setText(data)
        ckbox.setChecked(is_ckd)
        return ckbox
    @staticmethod
    def radiobox(object, name, rect, data, is_ckd=False):
        rdbox = QRadioButton(object)
        rdbox.setObjectName(name)
        rdbox.setGeometry(rect)
        rdbox.setText(data)
        rdbox.setChecked(is_ckd)
        return rdbox
    @staticmethod
    def groupbox(object, name, rect, item_set=(), layout=QHBoxLayout()):
        gpbox = QGroupBox(object)
        gpbox.setObjectName(name)
        gpbox.setGeometry(rect)
        for item in item_set:
            layout.addWidget(item)
        gpbox.setLayout(layout)
        return gpbox
    @staticmethod
    def combobox(object, name, rect, item_set=(), current_text='2048'):
        cmbox = QComboBox(object)
        cmbox.setObjectName(name)
        cmbox.setGeometry(rect)
        cmbox.addItems(item_set)
        cmbox.setCurrentText(current_text)
        return cmbox
    @staticmethod
    def widget(object, name, rect):
        wd = QWidget(object)
        wd.setObjectName(name)
        wd.setGeometry(rect)
        return wd
    @staticmethod
    def scroll(object, name, rect, widget, size=(50, 50), policy=Qt.ScrollBarAsNeeded):
        roll = QScrollArea(object)
        roll.setObjectName(name)
        roll.setGeometry(rect)
        roll.setHorizontalScrollBarPolicy(policy)
        roll.setMinimumSize(*size)
        roll.setWidget(widget)
        return roll

class mr_dialog_conf(QDialog):
    def __init__(self, mainwindow):
        super().__init__(mainwindow)
        self.init_ui()
    def init_ui(self):
        try:
            ut.conf_xml_parse()

            self.resize(800, 700)
            self.setWindowTitle('mr config')
            self.setWindowIcon(QIcon('.\\source\\配置.ico'))
            self.headTitleLabel = mr_qt_kit.label(self, 'conf_label_title', QRect(325,0,150,50), 'MR配置', QFont('微软雅黑', 20, QFont.Bold), PyQt5.QtCore.Qt.AlignCenter)

            #TEST widget

            self.label_testConf = mr_qt_kit.label(self, 'conf_label_testconf_title', QRect(10, 50, 120, 30), 'TEST_CONF', QFont('微软雅黑', 15, QFont.Normal))

            self.wd_test = mr_qt_kit.widget(self, 'conf_widget_test', QRect(50, 90, 750, 700))
            # wd_test.label_ts = mr_qt_kit.label(wd_test, 'conf_test', QRect(100, 100, 40, 40), 'test-test',  QFont('微软雅黑', 12, QFont.Normal))

            #test_total_time
            test_height = 5
            self.label_testTotalTime = mr_qt_kit.label(self.wd_test, 'conf_label_testtotaltime', QRect(50, test_height, 120,25), '测试总时间:', QFont('微软雅黑', 12, QFont.Normal))
            self.box_testTotalTime = mr_qt_kit.spinbox(self.wd_test, 'conf_box_testtotaltime', QRect(200, test_height, 60, 25), float(gl.TEST_CONF['test_total_time']), (1, 1000), 1)
            self.label_testTotalTime_unit = mr_qt_kit.label(self.wd_test, 'conf_label_testtotaltime_unit', QRect(265, test_height + 5, 40, 15), '小时')

            #cellid
            self.label_testCellid = mr_qt_kit.label(self.wd_test, 'conf_label_test_cellid', QRect(330, test_height, 50, 25), 'cellid:', QFont('微软雅黑', 12, QFont.Normal))
            self.line_testCellid = mr_qt_kit.line_edit(self.wd_test, 'conf_lineedit_cellid', QRect(390, test_height, 50, 25), gl.TEST_CONF['cellid'])
            #enbid
            self.label_testEnbid = mr_qt_kit.label(self.wd_test, 'conf_label_test_enbid', QRect(450, test_height, 50, 30), 'enbid:', QFont('微软雅黑', 12, QFont.Normal))
            self.line_testEnbid = mr_qt_kit.line_edit(self.wd_test, 'conf_lineedit_enbid', QRect(510, test_height, 50, 30), gl.TEST_CONF['enbid'])
            #event
            test_height += 35
            self.label_testEvent = mr_qt_kit.label(self.wd_test, 'conf_label_test_event', QRect(50, test_height, 120, 30), 'event:', QFont('微软雅黑', 12, QFont.Normal))
            self.ckbox_testEventA1 = mr_qt_kit.checkbox(self.wd_test, 'conf_ckbox_eventA1', QRect(200, test_height, 50, 30), 'A1', 'A1' in gl.TEST_CONF['event'])
            self.ckbox_testEventA2 = mr_qt_kit.checkbox(self.wd_test, 'conf_ckbox_eventA2', QRect(250, test_height, 50, 30), 'A2', 'A2' in gl.TEST_CONF['event'])
            self.ckbox_testEventA3 = mr_qt_kit.checkbox(self.wd_test, 'conf_ckbox_eventA3', QRect(300, test_height, 50, 30), 'A3', 'A3' in gl.TEST_CONF['event'])
            self.ckbox_testEventA4 = mr_qt_kit.checkbox(self.wd_test, 'conf_ckbox_eventA4', QRect(350, test_height, 50, 30), 'A4', 'A4' in gl.TEST_CONF['event'])
            self.ckbox_testEventA5 = mr_qt_kit.checkbox(self.wd_test, 'conf_ckbox_eventA5', QRect(400, test_height, 50, 30), 'A5', 'A5' in gl.TEST_CONF['event'])
            self.ckbox_testEventA6 = mr_qt_kit.checkbox(self.wd_test, 'conf_ckbox_eventA6', QRect(450, test_height, 50, 30), 'A6', 'A6' in gl.TEST_CONF['event'])
            self.ckbox_testEventB1 = mr_qt_kit.checkbox(self.wd_test, 'conf_ckbox_eventB1', QRect(500, test_height, 50, 30), 'B1', 'B1' in gl.TEST_CONF['event'])
            self.ckbox_testEventB2 = mr_qt_kit.checkbox(self.wd_test, 'conf_ckbox_eventB2', QRect(550, test_height, 50, 30), 'B2', 'B2' in gl.TEST_CONF['event'])
            #standard_LTE
            test_height += 40
            self.label_testStandard_LTE = mr_qt_kit.label(self.wd_test, 'conf_label_test_standardLTE', QRect(50, test_height, 150, 30), 'standard_LTE:', QFont('微软雅黑', 12, QFont.Normal))
            self.rdbox_testStandard_LTE_FDD = mr_qt_kit.radiobox(self.wd_test, 'conf_rdbox_test_standard_LTE_FDD', QRect(220, test_height, 60, 30), 'FDD-LTE', 'FDD-LTE' in gl.TEST_CONF['standard_LTE'])
            self.rdbox_testStandard_LTE_TD = mr_qt_kit.radiobox(self.wd_test, 'conf_rdbox_test_standard_LTE_TD', QRect(290, test_height, 60, 30), 'TD-LTE', 'TD-LTE' in gl.TEST_CONF['standard_LTE'])
            self.gpbox_testStandard_LTE = mr_qt_kit.groupbox(self.wd_test, 'conf_gpbox_test_standard_LTE', QRect(200, test_height, 300, 35), (self.rdbox_testStandard_LTE_FDD, self.rdbox_testStandard_LTE_TD), QHBoxLayout(self))

            #OEM
            test_height += 40
            self.label_testOem = mr_qt_kit.label(self.wd_test, 'conf_label_test_oem', QRect(50, test_height, 80, 30), 'OEM', QFont('微软雅黑', 12, QFont.Normal))
            self.line_testOem = mr_qt_kit.line_edit(self.wd_test, 'conf_lineedit_oem', QRect(200, test_height, 80, 30), gl.TEST_CONF['OEM'])
            #file_delay_time
            test_height += 40
            self.label_testFiledelayTime = mr_qt_kit.label(self.wd_test, 'conf_label_file_delay_time', QRect(50, test_height, 150, 30), '文件生成延时:', QFont('微软雅黑', 12, QFont.Normal))
            self.spinbox_testFiledelaytime = mr_qt_kit.spinbox(self.wd_test, 'conf_spinbox_file_delay_time', QRect(200, test_height, 50, 30), int(gl.TEST_CONF['file_delay_time']))
            self.label_testFiledelaytime_unit = mr_qt_kit.label(self.wd_test, 'conf_label_file_delay_time_unit', QRect(260, test_height + 10, 50, 20), '分钟')
            #out_item: is_57_out_excel is_58_out_excel is_59_out_excel test51- test_add_timestamp test_add_mro_s_value

            test_height += 40
            self.label_test_outitem = mr_qt_kit.label(self.wd_test, 'conf_label_outitem', QRect(50, test_height, 150, 30), '测试项输出:', QFont('微软雅黑', 12, QFont.Normal))
            self.ckbox_test51 = mr_qt_kit.checkbox(self.wd_test, 'conf_ckbox_test51', QRect(200, test_height, 80, 15), 'test51', int(gl.TEST_CONF['test51']) == 1)
            self.ckbox_test52 = mr_qt_kit.checkbox(self.wd_test, 'conf_ckbox_test52', QRect(300, test_height, 80, 15), 'test52', int(gl.TEST_CONF['test52']) == 1)
            self.ckbox_test53 = mr_qt_kit.checkbox(self.wd_test, 'conf_ckbox_test53', QRect(400, test_height, 80, 15), 'test53', int(gl.TEST_CONF['test53']) == 1)
            self.ckbox_test54 = mr_qt_kit.checkbox(self.wd_test, 'conf_ckbox_test54', QRect(500, test_height, 80, 15), 'test54', int(gl.TEST_CONF['test54']) == 1)
            self.ckbox_test55 = mr_qt_kit.checkbox(self.wd_test, 'conf_ckbox_test55', QRect(600, test_height, 80, 15), 'test55', int(gl.TEST_CONF['test55']) == 1)

            test_height += 40
            self.ckbox_test56 = mr_qt_kit.checkbox(self.wd_test, 'conf_ckbox_test56', QRect(200, test_height, 80, 15), 'test56', int(gl.TEST_CONF['test56']) == 1)
            self.ckbox_test57 = mr_qt_kit.checkbox(self.wd_test, 'conf_ckbox_test57', QRect(300, test_height, 80, 15), 'test57', int(gl.TEST_CONF['test57']) == 1)
            self.ckbox_test58 = mr_qt_kit.checkbox(self.wd_test, 'conf_ckbox_test58', QRect(400, test_height, 80, 15), 'test58', int(gl.TEST_CONF['test58']) == 1)
            self.ckbox_test59 = mr_qt_kit.checkbox(self.wd_test, 'conf_ckbox_test59', QRect(500, test_height, 80, 15), 'test59', int(gl.TEST_CONF['test59']) == 1)
            self.ckbox_test71 = mr_qt_kit.checkbox(self.wd_test, 'conf_ckbox_test71', QRect(600, test_height, 80, 15), 'test71', int(gl.TEST_CONF['test71']) == 1)

            test_height += 40
            self.ckbox_test72 = mr_qt_kit.checkbox(self.wd_test, 'conf_ckbox_test72', QRect(200, test_height, 80, 15), 'test72', int(gl.TEST_CONF['test72']) == 1)
            self.ckbox_test73 = mr_qt_kit.checkbox(self.wd_test, 'conf_ckbox_test73', QRect(300, test_height, 80, 15), 'test73', int(gl.TEST_CONF['test73']) == 1)
            self.ckbox_testAddTimestamp = mr_qt_kit.checkbox(self.wd_test, 'conf_ckbox_test_add_timestamp', QRect(400, test_height, 150, 15), 'MRO-timeStamp', int(gl.TEST_CONF['test_add_timestamp']) == 1)
            self.ckbox_testAddMrosvalue = mr_qt_kit.checkbox(self.wd_test, 'conf_ckbox_test_add_mros_value', QRect(550, test_height, 150, 15), 'mro-mrs diff', int(gl.TEST_CONF['test_add_mro_s_value']) == 1)

            test_height += 40
            self.ckbox_testAddmreEventnum = mr_qt_kit.checkbox(self.wd_test, 'conf_ckbox_test_add_mre_event_num', QRect(200, test_height, 150, 15), 'mre_event num', int(gl.TEST_CONF['test_add_mre_event_num']) == 1)

            test_height += 40
            self.ckbox_test57_excel = mr_qt_kit.checkbox(self.wd_test, 'conf_ckbox_test57_excel', QRect(200, test_height, 150, 15), '57项输出excel文件', int(gl.TEST_CONF['is_57_out_excel']) == 1)
            self.ckbox_test58_excel = mr_qt_kit.checkbox(self.wd_test, 'conf_ckbox_test58_excel', QRect(350, test_height, 150, 15), '58项输出excel文件', int(gl.TEST_CONF['is_58_out_excel']) == 1)
            self.ckbox_test59_excel = mr_qt_kit.checkbox(self.wd_test, 'conf_ckbox_test59_excel', QRect(500, test_height, 150, 15), '59项输出excel文件', int(gl.TEST_CONF['is_59_out_excel']) == 1)

            test_height += 40

            if gl.TEST_CONF['mre_begin_time'] == '0001-01-01T00:00:00.000' or re.match('^[0-9]{1,4}-([0-9]{1,2})-([0-9]{1,2})T([0-9]{1,2}):([0-9]{1,2}):([0-9]{1,2}).[0-9]{3}$', gl.TEST_CONF['mre_begin_time']) == None :
                tm_begin_struct = time.localtime(time.time() - 86400)
            else:
                tm_begin_struct = time.localtime(ut.get_timestamp_by_str_format(gl.TEST_CONF['mre_begin_time']) / 1000)
            mon_date_num = (31,
                               28 if ( tm_begin_struct.tm_year + 1970) % 4 == 0 and (tm_begin_struct.tm_year + 1970) % 100 != 0 or (tm_begin_struct.tm_year + 1970) % 400 == 0 else 29,
                               31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
            self.label_testMREeventnumBegin = mr_qt_kit.label(self.wd_test, 'conf_label_mre_event_num_begin', QRect(50, test_height, 150, 30), 'event begin-time:', QFont('微软雅黑', 12, QFont.Normal))
            self.spinbox_testMREeventBeginYear = mr_qt_kit.spinbox(self.wd_test, 'conf_spinbox_mre_event_begin_year', QRect(200, test_height, 80, 30), tm_begin_struct.tm_year, (0, 9999)  )
            self.label_testMREeventBeginYearUnit = mr_qt_kit.label(self.wd_test, 'conf_label_mre_event_begin_year_unit', QRect(280, test_height+5, 20, 25), '年', QFont('微软雅黑', 12, QFont.Normal))
            self.spinbox_testMREeventBeginMonth = mr_qt_kit.spinbox(self.wd_test, 'conf_spinbox_mre_event_begin_month', QRect(300, test_height, 40, 30), tm_begin_struct.tm_mon, (1,12) )
            self.label_testMREeventBeginMonthUnit = mr_qt_kit.label(self.wd_test, 'conf_label_mre_event_begin_month_unit', QRect(340, test_height+5, 20, 25), '月', QFont('微软雅黑', 12, QFont.Normal))
            self.spinbox_testMREeventBeginDay = mr_qt_kit.spinbox(self.wd_test, 'conf_spinbox_mre_event_begin_day', QRect(360, test_height, 40, 30), tm_begin_struct.tm_mday , (1,  mon_date_num[tm_begin_struct.tm_mon-1]))
            self.label_testMREeventBeginTunit = mr_qt_kit.label(self.wd_test, 'conf_label_mre_event_T_unit', QRect(410, test_height+5, 10, 25), 'T', QFont('微软雅黑', 12, QFont.Normal))
            self.spinbox_testMREeventBeginHour = mr_qt_kit.spinbox(self.wd_test, 'conf_spinbox_mre_event_begin_hour', QRect(420, test_height, 40, 30), tm_begin_struct.tm_hour, (0, 23))
            self.label_testMREeventBeginHourunit = mr_qt_kit.label(self.wd_test, 'conf_label_mre_event_begin_hour_unit', QRect(470, test_height+5, 10, 25), ':', QFont('微软雅黑', 12, QFont.Normal))
            self.spinbox_testMREeventBeginMin = mr_qt_kit.spinbox(self.wd_test, 'conf_spinbox_mre_event_begin_minute', QRect(480, test_height, 40, 30), tm_begin_struct.tm_min, (0, 59))
            self.label_testMREeventBeginMinunit = mr_qt_kit.label(self.wd_test, 'conf_label_mre_event_begin_min_unit', QRect(530, test_height+5, 10, 25), ':', QFont('微软雅黑', 12, QFont.Normal))
            self.spinbox_testMREeventBeginSec = mr_qt_kit.spinbox(self.wd_test, 'conf_spinbox_mre_event_begin_second', QRect(540, test_height, 40, 30), tm_begin_struct.tm_sec, (0, 59))
            self.label_testMREeventBeginSecunit = mr_qt_kit.label(self.wd_test, 'conf_label_mre_event_begin_second_unit', QRect(590, test_height + 5, 10, 25), '.', QFont('微软雅黑', 12, QFont.Normal))
            self.spinbox_testMREeventBeginMsec = mr_qt_kit.spinbox(self.wd_test, 'conf_spinbox_mre_event_begin_msecond', QRect(600, test_height, 60, 30), int(gl.TEST_CONF['mre_begin_time'].split('.')[-1]), (0, 999))

            test_height += 40
            if gl.TEST_CONF['mre_end_time'] == '0001-01-01T00:00:00.000' or re.match('^[0-9]{1,4}-([0-9]{1,2})-([0-9]{1,2})T([0-9]{1,2}):([0-9]{1,2}):([0-9]{1,2}).[0-9]{3}$', gl.TEST_CONF['mre_end_time']) == None :
                tm_end_struct = time.localtime(time.time() )
            else:
                tm_end_struct = time.localtime(ut.get_timestamp_by_str_format(gl.TEST_CONF['mre_end_time'])/1000 )
            self.label_testMREeventnumEnd = mr_qt_kit.label(self.wd_test, 'conf_label_mre_event_num_end', QRect(50, test_height, 150, 30), 'event end-time:', QFont('微软雅黑', 12, QFont.Normal))
            self.spinbox_testMREeventEndYear = mr_qt_kit.spinbox(self.wd_test, 'conf_spinbox_mre_event_end_year', QRect(200, test_height, 80, 30), tm_end_struct.tm_year, (0, 9999)  )
            self.label_testMREeventEndYearUnit = mr_qt_kit.label(self.wd_test, 'conf_label_mre_event_end_year_unit', QRect(280, test_height+5, 20, 25), '年', QFont('微软雅黑', 12, QFont.Normal))
            self.spinbox_testMREeventEndMonth = mr_qt_kit.spinbox(self.wd_test, 'conf_spinbox_mre_event_end_month', QRect(300, test_height, 40, 30), tm_end_struct.tm_mon, (1,12) )
            self.label_testMREeventEndMonthUnit = mr_qt_kit.label(self.wd_test, 'conf_label_mre_event_end_month_unit', QRect(340, test_height+5, 20, 25), '月', QFont('微软雅黑', 12, QFont.Normal))
            self.spinbox_testMREeventEndDay = mr_qt_kit.spinbox(self.wd_test, 'conf_spinbox_mre_event_end_day', QRect(360, test_height, 40, 30), tm_end_struct.tm_mday , (1,  mon_date_num[tm_end_struct.tm_mon-1]))
            self.label_testMREeventEndTunit = mr_qt_kit.label(self.wd_test, 'conf_label_mre_event_end_T_unit', QRect(410, test_height+5, 10, 25), 'T', QFont('微软雅黑', 12, QFont.Normal))
            self.spinbox_testMREeventEndHour = mr_qt_kit.spinbox(self.wd_test, 'conf_spinbox_mre_event_end_hour', QRect(420, test_height, 40, 30), tm_end_struct.tm_hour, (0, 23))
            self.label_testMREeventEndHourunit = mr_qt_kit.label(self.wd_test, 'conf_label_mre_event_End_hour_unit', QRect(470, test_height+5, 10, 25), ':', QFont('微软雅黑', 12, QFont.Normal))
            self.spinbox_testMREeventEndMin = mr_qt_kit.spinbox(self.wd_test, 'conf_spinbox_mre_event_end_minute', QRect(480, test_height, 40, 30), tm_end_struct.tm_min, (0, 59))
            self.label_testMREeventEndMinunit = mr_qt_kit.label(self.wd_test, 'conf_label_mre_event_end_min_unit', QRect(530, test_height+5, 10, 25), ':', QFont('微软雅黑', 12, QFont.Normal))
            self.spinbox_testMREeventEndSec = mr_qt_kit.spinbox(self.wd_test, 'conf_spinbox_mre_event_end_second', QRect(540, test_height, 40, 30), tm_end_struct.tm_sec, (0, 59))
            self.label_testMREeventEndSecunit = mr_qt_kit.label(self.wd_test, 'conf_label_mre_event_end_second_unit', QRect(590, test_height + 5, 10, 25), '.', QFont('微软雅黑', 12, QFont.Normal))
            self.spinbox_testMREeventEndMsec = mr_qt_kit.spinbox(self.wd_test, 'conf_spinbox_mre_event_end_msecond', QRect(600, test_height, 60, 30), int(gl.TEST_CONF['mre_end_time'].split('.')[-1]), (0, 999))


            test_height += 40
            self.wd_test.setGeometry(QRect(50, 90, 750, test_height))
            self.scroll_test = mr_qt_kit.scroll(self, 'scroll_conf_test', QRect(10, 90, 780, 250), self.wd_test, (780, 250))
            #MR-conf
            self.label_mr_conf_title = mr_qt_kit.label(self, 'conf_label_testmrtitle', QRect(10, 370, 100, 30), 'MR_CONF', QFont('微软雅黑', 15, QFont.Normal))

            self.wd_mr_conf = mr_qt_kit.widget(self, 'conf_widget_mr_conf', QRect())
            #UploadPeriod
            self.label_testuploadPeriod = mr_qt_kit.label(self, 'conf_label_uploadPeroid', QRect(50, 400, 100, 30), '文件上报周期:', QFont('微软雅黑', 12, QFont.Normal))
            self.spinbox_testUploadPeriod = mr_qt_kit.spinbox(self, 'conf_spinbox_uploadPeroid', QRect(200, 400, 50, 20), int(gl.MR_CONF['UploadPeriod']))
            self.label_testuploadPeriod_unit = mr_qt_kit.label(self, 'conf_label_uploadPeriod_unit', QRect(250, 400, 50, 20), '分钟', QFont('微软雅黑', 12, QFont.Normal))
            #SamplePeriod
            self.label_testSamplePeriod = mr_qt_kit.label(self, 'conf_label_samplePeriod', QRect(320, 400, 110, 30), '采集上报周期:',  QFont('微软雅黑', 12, QFont.Normal))
            self.combox_testSamplePeriod = mr_qt_kit.combobox(self, 'conf_combox_samplePeriod', QRect(440, 400, 50, 20),
                                                              ('2048', '5120', '10240', '60000', '360000', '720000', '1800000', '3600000'), gl.MR_CONF['SamplePeriod'])
            self.label_testSamplePeriod_unit = mr_qt_kit.label(self, 'conf_label_samplePeriod_unit', QRect(500, 400, 50, 20), 'ms', QFont('微软雅黑', 12, QFont.Normal))
            #SubFrameNum
            self.label_testSubFrameNum = mr_qt_kit.label(self, 'conf_label_subframenum', QRect(50, 430, 100, 20), '子帧:', QFont('微软雅黑', 12, QFont.Normal))
            self.ckbox_sub0 = mr_qt_kit.checkbox(self, 'conf_ckbox_sub0', QRect(200, 430, 50, 20), '0','0' in gl.MR_CONF['SubFrameNum'])
            self.ckbox_sub1 = mr_qt_kit.checkbox(self, 'conf_ckbox_sub1', QRect(250, 430, 50, 20), '1','1' in gl.MR_CONF['SubFrameNum'])
            self.ckbox_sub2 = mr_qt_kit.checkbox(self, 'conf_ckbox_sub2', QRect(300, 430, 50, 20), '2','2' in gl.MR_CONF['SubFrameNum'])
            self.ckbox_sub3 = mr_qt_kit.checkbox(self, 'conf_ckbox_sub3', QRect(350, 430, 50, 20), '3','3' in gl.MR_CONF['SubFrameNum'])
            self.ckbox_sub4 = mr_qt_kit.checkbox(self, 'conf_ckbox_sub4', QRect(400, 430, 50, 20), '4','4' in gl.MR_CONF['SubFrameNum'])
            self.ckbox_sub5 = mr_qt_kit.checkbox(self, 'conf_ckbox_sub5', QRect(450, 430, 50, 20), '5','5' in gl.MR_CONF['SubFrameNum'])
            self.ckbox_sub6 = mr_qt_kit.checkbox(self, 'conf_ckbox_sub6', QRect(500, 430, 50, 20), '6','6' in gl.MR_CONF['SubFrameNum'])
            self.ckbox_sub7 = mr_qt_kit.checkbox(self, 'conf_ckbox_sub7', QRect(550, 430, 50, 20), '7','7' in gl.MR_CONF['SubFrameNum'])
            self.ckbox_sub8 = mr_qt_kit.checkbox(self, 'conf_ckbox_sub8', QRect(600, 430, 50, 20), '8','8' in gl.MR_CONF['SubFrameNum'])
            self.ckbox_sub9 = mr_qt_kit.checkbox(self, 'conf_ckbox_sub9', QRect(650, 430, 50, 20), '9','9' in gl.MR_CONF['SubFrameNum'])

            #PrbNum
            self.label_testPrbNum = mr_qt_kit.label(self, 'conf_label_prbnum', QRect(50, 460, 100, 20), '子帧分帧:', QFont('微软雅黑', 12, QFont.Normal))
            self.line_testPrbNum = mr_qt_kit.line_edit(self, 'conf_lineedit_prbnum', QRect(200, 460, 200, 20), gl.MR_CONF['PrbNum'])
            #MeasureType
            self.label_testMeasureType = mr_qt_kit.label(self, 'conf_label_MeasureType', QRect(50, 490, 100, 20), 'MeasureType:',QFont('微软雅黑', 12, QFont.Normal))
            self.ckbox_mro = mr_qt_kit.checkbox(self, 'conf_ckbox_mro', QRect(200, 490, 80, 20), 'MRO', 'MRO' in gl.MR_CONF['MeasureType'])
            self.ckbox_mre = mr_qt_kit.checkbox(self, 'conf_ckbox_mre', QRect(300, 490, 80, 20), 'MRE', 'MRE' in gl.MR_CONF['MeasureType'])
            self.ckbox_mrs = mr_qt_kit.checkbox(self, 'conf_ckbox_mrs', QRect(400, 490, 80, 20), 'MRS', 'MRS' in gl.MR_CONF['MeasureType'])

            #OmcName
            self.label_omcName = mr_qt_kit.label(self, 'conf_label_OmcName', QRect(50, 520, 150, 20), 'OmcName', QFont('微软雅黑', 12, QFont.Normal))
            self.line_omcName = mr_qt_kit.line_edit(self, 'conf_lineedit_OmcName', QRect(200, 520, 200, 20), gl.MR_CONF['OmcName'])
            #SampleBeginTime
            self.label_sampleBeginTime = mr_qt_kit.label(self, 'conf_label_samplebeginTime', QRect(50, 550, 150, 20), 'SampleBeginTime', QFont('微软雅黑', 12, QFont.Normal))
            self.line_sampleBeginTime = mr_qt_kit.line_edit(self, 'conf_lineedit_sampleBeginTime', QRect(200, 550, 200, 20), gl.MR_CONF['SampleBeginTime'])
            #SampleEndTime
            self.label_SampleEndTime = mr_qt_kit.label(self, 'conf_label_sampleendTime', QRect(50, 580, 150, 20), 'SampleEndTime', QFont('微软雅黑', 12, QFont.Normal))
            self.line_sampleEndTime = mr_qt_kit.line_edit(self, 'conf_lineedit_sampleendTime', QRect(200, 580, 200, 20), gl.MR_CONF['SampleEndTime'])
            #MRECGIList
            self.label_MRECGILIST = mr_qt_kit.label(self, 'conf_label_mrecgilist', QRect(50, 610, 150, 20), 'MRECGIList', QFont('微软雅黑', 12, QFont.Normal))
            self.line_MRECGIList = mr_qt_kit.line_edit(self, 'conf_lineedit_mrecgilist', QRect(200, 610, 200, 20), gl.MR_CONF['MRECGIList'])

            #MeasureItems
            self.label_MeasureItems = mr_qt_kit.label(self, 'conf_label_mreasureItems', QRect(50, 640, 150, 20),'MeasureItems', QFont('微软雅黑', 12, QFont.Normal))
            self.line_MeasureItems = mr_qt_kit.line_edit(self, 'conf_lineedit_measureItems', QRect(200, 640, 200, 20), gl.MR_CONF['MeasureItems'])

            self.button_ok = mr_qt_kit.push_button(self, 'conf_button_ok', QRect(500, 610, 50, 30), '确认', self.push_ok)
            self.button_quit = mr_qt_kit.push_button(self, 'conf_button_quit', QRect(560, 610, 50, 30), '退出', self.push_quit)


            self.show()
        except Exception as rt:
            print (str(rt) + str(rt.__traceback__.tb_lineno))
    def push_ok(self):
        outItem_dict = {'is_57_out_excel':self.ckbox_test57_excel , 'is_58_out_excel':self.ckbox_test58_excel, 'is_59_out_excel':self.ckbox_test59_excel,
                       'test51':self.ckbox_test51, 'test52':self.ckbox_test52, 'test53':self.ckbox_test53, 'test54':self.ckbox_test54, 'test55':self.ckbox_test55,
                        'test56':self.ckbox_test56, 'test57':self.ckbox_test57, 'test58':self.ckbox_test58, 'test59':self.ckbox_test59,
                       'test71':self.ckbox_test71, 'test72':self.ckbox_test72, 'test73':self.ckbox_test73,
                        'test_add_timestamp':self.ckbox_testAddTimestamp, 'test_add_mro_s_value':self.ckbox_testAddMrosvalue, 'test_add_mre_event_num':self.ckbox_testAddmreEventnum }
        set_subfram = (self.ckbox_sub0, self.ckbox_sub1, self.ckbox_sub2,self.ckbox_sub3, self.ckbox_sub4, self.ckbox_sub5, self.ckbox_sub6,
                self.ckbox_sub7,self.ckbox_sub8,self.ckbox_sub9 )
        set_event = (self.ckbox_testEventA1, self.ckbox_testEventA2, self.ckbox_testEventA3, self.ckbox_testEventA4,
                     self.ckbox_testEventA5, self.ckbox_testEventA6, self.ckbox_testEventB1, self.ckbox_testEventB2)
        set_mrType = (self.ckbox_mro, self.ckbox_mre, self.ckbox_mrs)
        gl.CONF_XML_DATA[1]['test_total_time'] = self.box_testTotalTime.text()
        gl.CONF_XML_DATA[1]['cellid'] = self.line_testCellid.text()
        gl.CONF_XML_DATA[1]['enbid'] = self.line_testEnbid.text()
        gl.CONF_XML_DATA[1]['event'] = self.get_str_from_ckbox(set_event)
        gl.CONF_XML_DATA[1]['standard_LTE'] = self.rdbox_testStandard_LTE_FDD.text() if self.rdbox_testStandard_LTE_FDD.isChecked() else self.rdbox_testStandard_LTE_TD.text()
        gl.CONF_XML_DATA[1]['OEM'] = self.line_testOem.text()
        gl.CONF_XML_DATA[1]['file_delay_time'] = self.spinbox_testFiledelaytime.text()
        for item_key in outItem_dict:
            gl.CONF_XML_DATA[1][item_key] = '1' if outItem_dict[item_key].isChecked() else '0'
        gl.CONF_XML_DATA[3]['SampleEndTime'] = self.line_sampleEndTime.text()
        gl.CONF_XML_DATA[3]['SampleBeginTime'] = self.line_sampleBeginTime.text()
        gl.CONF_XML_DATA[3]['UploadPeriod'] = self.spinbox_testUploadPeriod.text()
        gl.CONF_XML_DATA[3]['SubFrameNum'] = self.get_str_from_ckbox(set_subfram)
        gl.CONF_XML_DATA[3]['PrbNum'] = self.line_testPrbNum.text()
        gl.CONF_XML_DATA[3]['MeasureType'] = self.get_str_from_ckbox(set_mrType)
        gl.CONF_XML_DATA[3]['SamplePeriod'] = self.combox_testSamplePeriod.currentText()
        gl.CONF_XML_DATA[3]['OmcName'] = self.line_omcName.text()
        gl.CONF_XML_DATA[3]['MRECGIList'] = self.line_MRECGIList.text()
        gl.CONF_XML_DATA[3]['MeasureItems'] = self.line_MeasureItems.text()

        mre_time_begin = ut.construct_timestr((self.spinbox_testMREeventBeginYear.value(), self.spinbox_testMREeventBeginMonth.value(), self.spinbox_testMREeventBeginDay.value(),
                                               self.spinbox_testMREeventBeginHour.value(), self.spinbox_testMREeventBeginMin.value(), self.spinbox_testMREeventBeginSec.value(),
                                               self.spinbox_testMREeventBeginMsec.value()))
        mre_time_end = ut.construct_timestr((self.spinbox_testMREeventEndYear.value(), self.spinbox_testMREeventEndMonth.value(), self.spinbox_testMREeventEndDay.value(),
                                             self.spinbox_testMREeventEndHour.value(), self.spinbox_testMREeventEndMin.value(), self.spinbox_testMREeventEndSec.value(),
                                             self.spinbox_testMREeventEndMsec.value()))
        if ut.get_timestamp_by_str_format(mre_time_begin) < ut.get_timestamp_by_str_format(mre_time_end):
            gl.CONF_XML_DATA[1]['mre_begin_time'] = mre_time_begin
            gl.CONF_XML_DATA[1]['mre_end_time'] = mre_time_end


        full_file_name = os.path.join(gl.SOURCE_PATH, "conf.xml")
        ut.create_conf_xml(full_file_name)
        self.close()

    def push_quit(self):
        self.close()
    def get_str_from_ckbox(self, set1):
        list1 = []
        for item in set1:
            if item.isChecked():
                list1.append(item.text())
        str1 = ','
        return str1.join(list1)


class mr_dialog_path(QDialog):
    remote_ip = '10.110.38.226'
    remote_port = '22'
    ssh_user = 'root'
    ssh_passwd = 'Bingo1993'
    remote_path = '/data/oran_sftp/pm_mr_mgmt/measurement/1/'
    locate_path = '.\\mr'
    path_filter = '^.*\.xml$'
    is_quit = False
    def __init__(self, mainwindow, local_path):
        super().__init__(mainwindow)
        self.locate_path = local_path
        self.ui_init()
    def ui_init(self):
        self.resize(600, 400)
        self.setWindowTitle('mr sftp')
        self.setWindowIcon(QIcon('.\\source\\问题.ico'))
        self.headTitleLabel = mr_qt_kit.label(self, 'path_label_title', QRect(225,0,150,50), 'MR下载', QFont('微软雅黑', 20, QFont.Bold), PyQt5.QtCore.Qt.AlignCenter)
        #ip



        self.ipLabel = mr_qt_kit.label(self, 'label_ip', QRect(50, 60, 50, 30), 'ip:', QFont('consolas', 15, QFont.Normal))
        self.ipCombox = mr_qt_kit.combobox(self, 'text_ip', QRect(110, 65, 200, 25), ut.get_dict_key_list(gl.INFORM_DICT), ut.get_dict_key_list(gl.INFORM_DICT)[0])
        self.ipCombox.currentTextChanged.connect(self.download_ip_select_changed)
        #port
        self.portLabel = mr_qt_kit.label(self, 'label_port', QRect(330, 60, 50, 30), 'port:', QFont('consolas', 15, QFont.Normal))
        self.portbox = mr_qt_kit.spinbox(self, 'box_port', QRect(390, 60, 50, 30), 22, (1,1023), 1)

        #user passwd
        self.userLabel = mr_qt_kit.label(self, 'label_user', QRect(50, 120, 50, 30), 'user:', QFont('consolas', 15, QFont.Normal))
        self.userLine = mr_qt_kit.line_edit(self, 'line_user', QRect(110, 120, 100, 30), gl.INFORM_DICT[self.ipCombox.currentText()]['user'])
        self.passLabel = mr_qt_kit.label(self, 'label_pass', QRect(220, 120, 50, 30), 'pass:',QFont('consolas', 15, QFont.Normal))
        self.passLine = mr_qt_kit.line_edit(self, 'line_pass', QRect(280, 120, 200, 30), gl.INFORM_DICT[self.ipCombox.currentText()]['passwd'], QLineEdit.Password)

        #path
        self.pathLabel = mr_qt_kit.label(self, 'label_path', QRect(50, 170, 50, 30), 'path:', QFont('consolas', 15, QFont.Normal))
        self.pathLine = mr_qt_kit.line_edit(self, 'line_path', QRect(110, 170, 400, 30), gl.INFORM_DICT[self.ipCombox.currentText()]['path'])

        #filter TODO: add
        self.filterLabel = mr_qt_kit.label(self, 'label_filter', QRect(50, 220, 70, 30), 'filter:', QFont('consolas', 15, QFont.Normal))
        self.filterLine = mr_qt_kit.line_edit(self, 'line_filter', QRect(120, 220, 200, 30), gl.INFORM_DICT[self.ipCombox.currentText()]['filter'])

        # #local path
        # self.lpathLabel = mr_qt_kit.label(self, 'label_lpath', QRect(50, 220, 50, 30), 'local:',  QFont('consolas', 11, QFont.Normal))
        # self.lpathLine = mr_qt_kit.line_edit(self, 'line_lpath', QRect(110, 220, 400, 30), '.\\mr')
        # mr_qt_kit.push_button(self, 'local_path_find', QRect(520, 220, 50, 30), '...', self.select_locate_file_path)

        #progress bar
        self.downLabel = mr_qt_kit.label(self, 'label_download', QRect(50, 260, 100, 30), 'download:', QFont('consolas', 15, QFont.Normal))
        self.progress_bar = mr_qt_kit.progress_bar(self, 'download_progress', QRect(110, 300, 400, 30))

        self.downshowLabel = mr_qt_kit.label(self, 'label_download_show', QRect(50, 330, 500, 30), '', QFont('consolas', 10, QFont.Normal))

        self.button_ok = mr_qt_kit.push_button(self, 'button_ok', QRect(400, 350, 50, 30), '确认' ,self.push_ok)
        self.button_quit = mr_qt_kit.push_button(self, 'button_quit', QRect(460, 350, 50, 30), 'quit', self.close)
        self.show()
    def download_ip_select_changed(self):
        #当ip 改变的时候，改变后面的path，passwd的数据显示
        self.userLine.setText(gl.INFORM_DICT[self.ipCombox.currentText()]['user'])
        self.passLine.setText(gl.INFORM_DICT[self.ipCombox.currentText()]['passwd'])
        self.pathLine.setText(gl.INFORM_DICT[self.ipCombox.currentText()]['path'])
        self.filterLine.setText(gl.INFORM_DICT[self.ipCombox.currentText()]['filter'])
    def push_ok(self):
        if self.ipCombox.currentText() != '':#TODO:re.match
            gl.MR_DOWNLOAD_IP = self.remote_ip = self.ipCombox.currentText()
        if self.portbox.text() != '' and int(self.portbox.text()) < 1024 and int(self.portbox.text()) > 0:
            self.remote_port = self.portbox.text()
        if self.userLine.text() != '' :
            self.ssh_user = self.userLine.text()
        if self.passLine.text() != '':
            self.ssh_passwd = self.passLine.text()
        if self.pathLine.text() != '':
            self.remote_path = self.pathLine.text() + '/'
        if self.filterLine.text() != '':
            self.path_filter = self.filterLine.text()
        else:
            self.path_filter = '^.*\.xml$'
        gl.INFORM_DICT[self.remote_ip] = {'user':self.ssh_user, 'passwd':self.ssh_passwd, 'path':self.remote_path, 'filter':self.path_filter}
        self.button_ok.setEnabled(False)
        self.button_quit.setEnabled(False)
        # print (self.locate_path)
        sftp = ut.sftp_tool(self.remote_ip, self.remote_port, self.ssh_user, self.ssh_passwd)
        sftp.get(self.remote_path, self.locate_path, self.progress_bar, self.path_filter, self.downshowLabel)
        self.button_ok.setEnabled(True)
        self.button_quit.setEnabled(True)
        ut.write_inform_file()
        gl.IS_SSH_CONN = 1
        self.close()
    def select_locate_file_path(self):
        self.locate_path = QFileDialog.getExistingDirectory(self, '浏览', '.\\')
        if self.locate_path == '':
            self.locate_path = '.\\mr'
        self.lpathLine.setText(self.locate_path)
    def click_quit(self):
        self.close()


exit_qt_application = lambda argv:sys.exit(argv)

class mr_ui_window(QMainWindow):
    conf_path = '.\\source\\conf.xml'
    mr_path = '.\\mr'
    output_path = '.\\output'
    def __init__(self):
        super().__init__()
        self.init_ui()
    def init_ui(self):

        self.resize(1200, 800)
        self.center()
        self.setWindowTitle('mr test')
        self.setWindowIcon(QIcon('.\\source\\thinking.ico'))
        #标题
        mr_qt_kit.label(self, 'mr_title',QRect(450,0,300,100), 'mr测试程序',QFont('微软雅黑', 20, QFont.Bold), PyQt5.QtCore.Qt.AlignCenter)


        #conf.xml
        ut.check_conf_xml(self.conf_path)
        mr_qt_kit.label(self, 'conf',QRect(100, 100, 100, 30), '配置文件:', QFont('微软雅黑', 14, QFont.Bold))
        self.conf_path_label = mr_qt_kit.label(self, 'conf_path',QRect(200, 100, 700, 30), self.conf_path, QFont('Consolas', 14, QFont.Normal))
        self.conf_path_label.setFrameShape(QFrame.Box)
        mr_qt_kit.push_button(self, 'conf_read',QRect(910, 100, 50, 30), '查看', self.read_conf_file)
        self.conf_change_button = mr_qt_kit.push_button(self, 'conf_write',QRect(980, 100, 70, 30), '确认修改', self.write_conf_file)
        self.conf_change_button.setEnabled(False)
        self.conf_mod_button = mr_qt_kit.push_button(self, 'conf_mod', QRect(1070, 100, 50, 30), '配置', self.mod_conf)
        #mr_path
        mr_qt_kit.label(self, 'mr_path', QRect(100, 140, 100, 30), 'MR路径:', QFont('微软雅黑', 14, QFont.Bold))
        self.mr_path_label = mr_qt_kit.label(self, 'mr_path_value', QRect(200, 140, 700, 30), self.mr_path, QFont('Consolas', 14, QFont.Normal))
        self.mr_path_label.setFrameShape(QFrame.Box)
        mr_qt_kit.push_button(self, 'mr_path_find', QRect(910, 140, 50, 30), '...', self.select_mr_file_path)
        mr_qt_kit.push_button(self, 'mr_path_download', QRect(990,140,50, 30), '下载', self.mr_file_download_from_sftp)
        #output_path
        mr_qt_kit.label(self, 'output', QRect(100, 180, 100, 30), '输出路径:', QFont('微软雅黑', 14, QFont.Bold))
        self.output_path_label = mr_qt_kit.label(self, 'output_path', QRect(200, 180, 700, 30), self.output_path, QFont('Consolas', 14, QFont.Normal))
        self.output_path_label.setFrameShape(QFrame.Box)
        mr_qt_kit.push_button(self, 'output_path_find', QRect(910, 180, 50, 30), '浏览', self.select_output_file_path)

        #text output
        self.text = mr_qt_kit.text_edit(self, 'line', QRect(100, 220, 1000, 400))

        #start test push_button
        self.test_push_button = mr_qt_kit.push_button(self, 'test_push_button', QRect(910, 650, 70, 30), '开始测试', self.mr_test_start)
        self.cat_data_button = mr_qt_kit.push_button(self, 'cat_data_button', QRect(990, 650, 70, 30), '查看结果', self.cat_data_file)
        self.cat_data_button.setEnabled(False)
        self.quit_push_button = mr_qt_kit.push_button(self, 'quit_push_button', QRect(990, 690, 70, 30), 'QUIT', QCoreApplication.instance().quit)

        self.show()


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

    def mr_file_download_from_sftp(self):
        try:
            self.window = mr_dialog_path(self, self.mr_path)

        except Exception as rt:
            print ('%s %d'%(rt, rt.__traceback__.tb_lineno))
        # self.hide()

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
            print (gl.OUTPUT_PATH)

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



    def mod_conf(self):
        conf_window = mr_dialog_conf(self)
# write_info = lambda info:mr_ui_window.getText().append(info)

class pm_config_dialog(QDialog):
    def __init__(self):
        super().__init__()

    def init_ui(self):
        pass


class pm_ui_window(QDialog):
    conf_path = '.\\source\\conf.xml'
    output_path = '.\\output'
    def __init__(self):
        super().__init__()
        self.init_ui()
    def init_ui(self):
        self.resize(1200, 800)
        self.setWindowTitle('pm test')
        self.setWindowIcon(QIcon('.\\source\\thinking.ico'))
        height = 0
        mr_qt_kit.label(self, 'pm_title',QRect(450,0,300,100), 'pm测试程序',QFont('微软雅黑', 20, QFont.Bold), PyQt5.QtCore.Qt.AlignCenter)
        #conf.xml

        ut.check_conf_xml(self.conf_path)
        height += 100
        mr_qt_kit.label(self, 'conf_pm',QRect(100, height, 100, 30), '配置:', QFont('微软雅黑', 14, QFont.Bold))
        self.conf_path_label = mr_qt_kit.label(self, 'pm_conf_path',QRect(200, height, 700, 30), self.conf_path, QFont('Consolas', 14, QFont.Normal))
        self.conf_path_label.setFrameShape(QFrame.Box)

        self.conf_mod_button = mr_qt_kit.push_button(self, 'pm_conf_mod', QRect(910, height, 50, 30), '配置', self.mod_conf)

        #output_path
        height += 50
        mr_qt_kit.label(self, 'output', QRect(100, height, 100, 30), '输出路径:', QFont('微软雅黑', 14, QFont.Bold))
        self.output_path_label = mr_qt_kit.label(self, 'output_path', QRect(200, height, 700, 30), self.output_path, QFont('Consolas', 14, QFont.Normal))
        self.output_path_label.setFrameShape(QFrame.Box)
        mr_qt_kit.push_button(self, 'output_path_find', QRect(910, height, 50, 30), '浏览', self.select_output_file_path)

        #text output
        height += 50
        self.text = mr_qt_kit.text_edit(self, 'line', QRect(100, height, 1000, 400))

        #start test push_button
        self.test_push_button = mr_qt_kit.push_button(self, 'test_push_button', QRect(910, 650, 70, 30), '开始测试', self.pm_test_start)
        self.cat_data_button = mr_qt_kit.push_button(self, 'cat_data_button', QRect(990, 650, 70, 30), '查看结果', self.cat_data_file)
        self.cat_data_button.setEnabled(False)
        self.quit_push_button = mr_qt_kit.push_button(self, 'quit_push_button', QRect(990, 690, 70, 30), 'QUIT', QCoreApplication.instance().quit)

        self.show()

    def mod_conf(self):
        pass
    def pm_test_start(self):
        self.cat_data_button.setEnabled(True)
    def select_output_file_path(self):
        self.output_path = QFileDialog.getExistingDirectory(self, '浏览', '.\\')
        if self.output_path == '':
            self.output_path = '.\\output'
        self.output_path_label.setText(self.output_path)
    def cat_data_file(self):
        file_name = os.path.join(self.output_path, 'data.txt')
        os.startfile(file_name)
class pm_mr_dialog(QDialog):

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_config()
    def init_ui(self):
        ut.init_inform_dict()
        self.resize(600, 400)
        self.setWindowTitle('mt test')
        self.setWindowIcon(QIcon('.\\source\\thinking.ico'))
        self.mr_test_button = mr_qt_kit.push_button(self, "mr_test_button", QRect(100, 100, 100, 40), "mr_test", self.mr_test_ui)
        self.pm_test_button = mr_qt_kit.push_button(self, "pm_test_button", QRect(300, 100, 100, 40), "pm_test", self.pm_test_ui)
        self.show()
    def mr_test_ui(self):
        self.hide()
        self.mr_test_ui_window = mr_ui_window()

    def pm_test_ui(self):
        #TODO: add pm file time_create offset test
        self.hide()

        try:
            self.pm_test_ui_window = pm_ui_window()
            user.pm_test_process()
        except Exception as rt:
            print ("%s %d"%(rt, rt.__traceback__.tb_lineno))
        return
    def init_config(self):
        ut.init_inform_dict()

