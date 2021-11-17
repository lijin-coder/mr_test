import xml.dom.minidom
import os
import re
import string
import time
import datetime
import glob
from lxml import etree
import math
#import utils
import xlrd
import xlutils
import openpyxl

TEST_PATH = ".\\"
MR_TEST_PATH = ".\\mr\\"
SOURCE_PATH = ".\\source\\"
OUTPUT_PATH = ".\\output\\"
OUT_PATH = OUTPUT_PATH + "data.txt"
XLS_NAME = "LTE数字蜂窝移动通信网无线操作维护中心（OMC-R）测量报告测试要求表格-V2.1.0.xlsx"
ONE_DIMENSION_NAME = "LTE一维测量报告统计数据"
TIME_OUTPUT_FORMAT = "%Y:%m:%d %H:%M:%S"
MR_DICT = {}
MR_TYPE = {'MRO':1, 'MRE':2, 'MRS':3}
str_info = []

TEST_CONF = {'test_total_time':'', 'cellid':'', 'enbid':'', 'event':'', 'standard_LTE':'', 'OEM':'',  \
             'file_delay_time':'', 'is_57_out_excel':'', 'is_58_out_excel':'', 'is_59_out_excel':'',\
             'test51':'','test52':'','test53':'','test54':'','test55':'','test56':'','test57':'','test58':'','test59':'','test61':'',\
             'test62':'','test63':'','test71':'','test72':'','test73':'','test_add_timestamp':''}
MR_CONF = {'MrEnable':0, 'MrUrl':" ", 'MrUsername':" ", 'MrPassword': " ", 'MeasureType':" ", 'OmcName': " ", 'SamplePeriod': 0, 'UploadPeriod':0, 'SampleBeginTime':" ",'SampleEndTime': " ", 'PrbNum': " ", 'SubFrameNum':"", 'MRECGIList':'', 'MeasureItems':''}
TEST_OUT = {'test_51' : [], 'test_52' : [], 'test_53' : [], 'test_54':[], 'test_55':[], 'test_56':[], 'test_57':[],'test_58':[],'test_59':[],'test_61':[],'test_62':[],'test_63':[],'test_71':[],'test_72':[],'test_73':[], 'test_81':[]}
TEST_ITEM_LIST = []
OUT_LIST_NAME = ['conf_xml_parse', 'MR_xml_init', 'test 51','test 52','test 53','test 54','test 55','test 56','test 57','test 58','test 59','test 61',\
                 'test 62','test 63','test 71','test 72','test 73','test_add_timestamp','end']

dom = []
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
