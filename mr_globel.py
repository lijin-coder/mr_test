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
IS_SSH_CONN = 0

TEST_CONF = {'test_total_time':'', 'cellid':'', 'enbid':'', 'event':'', 'standard_LTE':'', 'OEM':'',
             'file_delay_time':'', 'is_57_out_excel':'', 'is_58_out_excel':'', 'is_59_out_excel':'',
             'test51':'','test52':'','test53':'','test54':'','test55':'','test56':'','test57':'','test58':'','test59':'','test61':'',
             'test62':'','test63':'','test71':'','test72':'','test73':'','test_add_timestamp':'', 'test_add_mro_s_value':'',
             'test_add_mre_event_num':'','mre_begin_time':'', 'mre_end_time':''}
MR_CONF = {'MrEnable':'', 'MrUrl':"", 'MrUsername':"", 'MrPassword': "", 'MeasureType':"", 'OmcName': "", 'SamplePeriod': '', 'UploadPeriod':'', 'SampleBeginTime':"",'SampleEndTime': "", 'PrbNum': "", 'SubFrameNum':"", 'MRECGIList':'', 'MeasureItems':''}
TEST_OUT = {'test_51' : [], 'test_52' : [], 'test_53' : [], 'test_54':[], 'test_55':[], 'test_56':[], 'test_57':[],'test_58':[],'test_59':[],'test_61':[],'test_62':[],'test_63':[],'test_71':[],'test_72':[],'test_73':[], 'test_81':[]}
PM_CONF = {'Enable':'', 'Alias':'', 'URL':'', 'Username':'', 'Password':'', 'PeriodicUploadInterval':'', 'PeriodicUploadTime':''}
TEST_ITEM_LIST = []
OUT_LIST_NAME = ['conf_xml_parse', 'MR_xml_init', 'test 51','test 52','test 53','test 54','test 55','test 56','test 57','test 58','test 59','test 61',
                 'test 62','test 63','test 71','test 72','test 73','test_add_timestamp','end']
INFORM_DICT = {}
dom = []
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
mr_create_time_dict = {}
MR_REMOTE_FILE_TIME_DIST = {}
MR_DOWNLOAD_IP = ''

#user-func global:
test_mre_event_num_dict = {'A1':{'num':0, 'time_str':[]}, 'A2':{'num':0, 'time_str':[]}, 'A3':{'num':0, 'time_str':[]}, 'A4':{'num':0, 'time_str':[]}, 'A5':{'num':0, 'time_str':[]},
                      'A6':{'num':0, 'time_str':[]}, 'B1':{'num':0, 'time_str':[]}, 'B2':{'num':0, 'time_str':[]}}

CONF_XML_DATA = [
##[0] - head
'''<?xml version="1.0" encoding="UTF-8"?>
<configure>
    <TEST_CONF>
''',
## [1] TEST_CONF- dict
{
    'test_total_time':      '2',
    'cellid':               '215',
    'enbid':                '215',
    'event':                'A1,A2,A3,A4,A5',
    'standard_LTE':         'FDD-LTE',
    'OEM':                  'CMDI',
    'file_delay_time':      '30',
    'is_57_out_excel':      '0',
    'is_58_out_excel':      '0',
    'is_59_out_excel':      '0',
    'test51':               '1',
    'test52':               '1',
    'test53':               '1',
    'test54':               '1',
    'test55':               '1',
    'test56':               '1',
    'test57':               '1',
    'test58':               '1',
    'test59':               '1',
    'test61':               '1',
    'test62':               '1',
    'test63':               '1',
    'test71':               '1',
    'test72':               '1',
    'test73':               '1',
    'test_add_timestamp':   '1',
    'test_add_mro_s_value': '1',
    'mre_begin_time':       '0001-01-01T00:00:00.000',
    'mre_end_time':         '0001-01-01T00:00:00.000'
},
## [2]  TEST-conf  tail
'''    </TEST_CONF>
    <MR_CONF>
''',
## [3] MR_CONF dict
{       'SampleEndTime':        '0001-01-01T00:00:00Z',
        'MrPassword':           'test_mr',
        'UploadPeriod':         '1',
        'MrUrl':                'http://10.110.38.214:9000/pm',
        'MrUsername':           'test_pm',
        'SubFrameNum':          '2,3,7',
        'PrbNum':               '0,1,2,3,4,5,6,7,8,9',
        'MeasureType':          'MRO,MRE,MRS',
        'SamplePeriod':         '2048',
        'OmcName':              'OMC0_2_2048',
        'MrEnable':             '1',
        'SampleBeginTime':      '0001-01-01T00:00:00Z',
        'MRECGIList':           'all',
        'MeasureItems':         'all'
},
##[4] TAIL
'''    </MR_CONF>
    <PM_CONF>
        <Enable>1</Enable>
        <Alias>Alias</Alias>
        <URL>http://10.110.38.214:9000/pm</URL>
        <Username>myftp_2</Username>
        <Password>123</Password>
        <PeriodicUploadInterval>300</PeriodicUploadInterval>
        <PeriodicUploadTime>0001-01-01T00:01:00Z</PeriodicUploadTime>
    </PM_CONF>
    <TEST_OUT>
        <test_51 item_num="10" item1="1" item2="2" item3="3" item4="4"  item5="5" item6="6" item7="7" item8="8" item9="9" item10="10" />
        <test_52 item_num="7" item1="1" item2="2" item3="11" item4="12" item5="13" item6="14" item7="15" />
        <test_53 item_num="4" item1="1" item2="2" item3="16" item4="17"  />
        <test_54 item_num="4" item1="1" item2="2" item3="18" item4="19"  />
        <test_55 item_num="6" item1="1" item2="2" item3="20" item4="21" item5="22" item6="23"/>
        <test_56 item_num="5" item1="1" item2="2" item3="20" item4="24" item5="25" />
        <test_57 item_num="2" item1="1" item2="2"  />
        <test_58 item_num="14" item1="1" item2="2" item3="26" item4="27" item5="28" item6="29" item7="30" item8="31" item9="32" item10="1" item11="2" item12="33" item13="34" item14="32" />
        <test_59 item_num="20" item1="1" item2="2" item3="35" item4="36"  item5="37" item6="38" item7="39" item8="40" item9="41" item10="42" 
            item11="1" item12="2" item13="43" item14="44" item15="45" item16="46" item17="47" item18="48" item19="49" item20="50"/>
        <test_61 item_num="7" item1="1" item2="51" item3="2" item4="20" item5="52" item6="53" item7="54"  />
        <test_62 item_num="13" item1="1" item2="2" item3="55" item4="56" item5="57" item6="58" item7="59" item8="60" item9="61" item10="62" item11="63" item12="64" item13="65"/>
        <test_63 item_num="9" item1="1" item2="2" item3="66" item4="67" item5="67" item6="68" item7="69" item8="70" item9="71" />
        <test_71 item_num="6" item1="1" item2="2" item3="72" item4="73" item5="74" item6="75" />
        <test_72 item_num="8" item1="1" item2="2" item3="76" item4="77" item5="78" item6="79" item7="80" item8="81"/>
        <test_73 item_num="6" item1="1" item2="2" item3="82" item4="83" item5="84" item6="85" />
        <test_81 item_num="5" item1="1" item2="2" item3="86" item4="87" item5="88" />
    </TEST_OUT>
    <ITEM_NAME>
        <item id="1">测试时间</item>
        <item id="2">测试时长</item>
        <item id="3">开启MR测量基站数</item>
        <item id="4">预期文件总数</item>
        <item id="5">MRS统计文件数</item>
        <item id="6">MRO统计文件数</item>
        <item id="7">MRE统计文件数</item>
        <item id="8">MRS统计文件数是否完整</item>
        <item id="9">MRO统计文件数是否完整</item>
        <item id="10">MRE统计文件数是否完整</item>
        <item id="11">RSRP小区数</item>
        <item id="12">RSRQ小区数</item>
        <item id="13">UE发射功率余量小区数</item>
        <item id="14">上行信噪比小区数</item>
        <item id="15">上报的小区是否一致</item>
        <item id="16">皮基站接收干扰功率子帧数</item>
        <item id="17">上报的子帧是否一致</item>
        <item id="18">开启测量测量的皮基站接收干扰功率的PRB数</item>
        <item id="19">上报的PRB是否一致</item>
        <item id="20">测试项</item>
        <item id="21">参考信号接收功率</item>
        <item id="22">参考信号接收质量</item>
        <item id="23">UE发射功率余量</item>
        <item id="24">扩展型皮基站接收干扰功率</item>
        <item id="25">上行信噪比</item>
        <item id="26">测试UE ID</item>
        <item id="27">理论上报采样点数</item>
        <item id="28">参考信号接收功率采样点数</item>
        <item id="29">参考信号接收质量采样点数</item>
        <item id="30">UE发射功率余量采样点数</item>
        <item id="31">上行信噪比采样点数</item>
        <item id="32">上报采样点一致性</item>
        <item id="33">理论扩展型皮基站接收干扰功率采样点数</item>
        <item id="34">实际上报扩展型皮基站接收干扰功率采样点数</item>
        <item id="35">A1事件是否支持</item>
        <item id="36">A2事件是否支持</item>
        <item id="37">A3事件是否支持</item>
        <item id="38">A4事件是否支持</item>
        <item id="39">A5事件是否支持</item>
        <item id="40">A6事件是否支持</item>
        <item id="41">B1事件是否支持</item>
        <item id="42">B2事件是否支持</item>
        <item id="43">A1事件样本数据完整性</item>
        <item id="44">A2事件样本数据完整性</item>
        <item id="45">A3事件样本数据完整性</item>
        <item id="46">A4事件样本数据完整性</item>
        <item id="47">A5事件样本数据完整性</item>
        <item id="48">A6事件样本数据完整性</item>
        <item id="49">B1事件样本数据完整性</item>
        <item id="50">B2事件样本数据完整性</item>
        <item id="51">测试扩展型皮基站版本</item>
        <item id="52">信令文件记录采样点数量</item>
        <item id="53">MR采样点数量</item>
        <item id="54">偏离程度</item>
        <item id="55">对比方式</item>
        <item id="56">PRB0</item>
        <item id="57">PRB1</item>
        <item id="58">PRB2</item>
        <item id="59">PRB3</item>
        <item id="60">PRB4</item>
        <item id="61">PRB5</item>
        <item id="62">PRB6</item>
        <item id="63">PRB7</item>
        <item id="64">PRB8</item>
        <item id="65">PRB9</item>
        <item id="66">系统内邻区信息分项统计</item>
        <item id="67">系统内邻区参考信号接收功率</item>
        <item id="68">系统内邻区载波号</item>
        <item id="69">系统内邻区小区识别码</item>
        <item id="70">系统内邻区个数</item>
        <item id="71">备注</item>
        <item id="72">文件名称是否满足命名规则要求</item>
        <item id="73">文件格式是否正确</item>
        <item id="74">压缩文件格式是否正确</item>
        <item id="75">生成文件时间是否满足最大时延要求(南向)</item>
        <item id="76">XML文件结构是否正确</item>
        <item id="77">标签名称是否完整和正确</item>
        <item id="78">XML标签属性是否完整和正确</item>
        <item id="79">fileHeader标签属性是否完整和正确</item>
        <item id="80">皮基站标签属性是否完整和正确</item>
        <item id="81">object标签属性是否完整和正确</item>
        <item id="82">MRO最大样本数</item>
        <item id="83">MRO实际样本数</item>
        <item id="84">MRO样本数据是否按照时间先后顺序存储</item>
        <item id="85">MRO文件是否准确</item>
        <item id="86">内存占用情况</item>
        <item id="87">CPU利用率提升情况</item>
        <item id="88">对设备性能有重大影响的测量数据</item>
    </ITEM_NAME>
</configure>
'''

]
