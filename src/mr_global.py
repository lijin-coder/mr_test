# encoding: utf-8


# mr_global.py: the global variable, include the config information, MR file information etd.

#===========================================================
#   file & path
#===========================================================
TEST_PATH = "..\\"
MR_TEST_PATH = "..\\mr\\"
PM_TEST_PATH = "..\\pm\\"
SOURCE_PATH = "..\\resource\\"
OUTPUT_PATH = "..\\output\\"
OUT_PATH = OUTPUT_PATH + "data.txt"
file_split_code = "\\"
XLS_NAME = "LTE数字蜂窝移动通信网无线操作维护中心（OMC-R）测量报告测试要求表格-V2.1.0.xlsx"
ONE_DIMENSION_NAME = "LTE一维测量报告统计数据"

#===========================================================
#   time
#===========================================================
test51_end_time_str = "2030-01-01T00:00:00Z"
TIME_OUTPUT_FORMAT = "%Y:%m:%d %H:%M:%S"
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"



#===========================================================
#   global vairable (information)
#===========================================================
MR_DICT = {}
PM_DICT = {}
MR_TYPE = {'MRO':1, 'MRE':2, 'MRS':3}
str_info = []
IS_SSH_CONN = 0
IS_LINUX = 0
IS_PY2 = 0

TEST_CONF = {   'test_total_time':'',      'cellid':'',        'enbid':'',         'event':'',         'standard_LTE':'',          'OEM':'',
                'file_delay_time':'',      'is_57_out_excel':'',    'is_58_out_excel':'',       'is_59_out_excel':'',
                'test_51':'',    'test_52':'',    'test_53':'',    'test_54':'',    'test_55':'',    'test_56':'',    'test_57':'',    'test_58':'',
                'test_59':'',    'test_61':'',    'test_62':'',    'test_63':'',    'test_71':'',    'test_72':'',    'test_73':'',    
                'ue_meas_id':'',        'nc_pci_earfcn':'',     'ue_log_file_name': '',         'phr_file_name':'',     'mr_path':'',           
                'pm_path':''}
MR_CONF = { 'MrEnable':'',  'MrUrl':"",     'MrUsername':"",    'MrPassword': "",   'MeasureType':"", 
            'OmcName': "",  'SamplePeriod': '',     'UploadPeriod':'',  'SampleBeginTime':"",   'SampleEndTime': "", 
            'PrbNum': "",   'SubFrameNum':"",       'MRECGIList':'',    'MeasureItems':''}
TEST_OUT = {'test_51' : [], 'test_52' : [], 'test_53' : [], 'test_54':[], 'test_55':[], 'test_56':[], 'test_57':[],'test_58':[],
            'test_59':[],'test_61':[],'test_62':[],'test_63':[],'test_71':[],'test_72':[],'test_73':[], 'test_81':[]}
PM_CONF = {'Enable':'', 'Alias':'', 'URL':'', 'Username':'', 'Password':'', 'PeriodicUploadInterval':'', 'PeriodicUploadTime':''}
TEST_ITEM_LIST = []
# OUT_LIST_NAME = ['conf_xml_parse', 'MR_xml_init', 'test 51','test 52','test 53','test 54','test 55','test 56','test 57','test 58','test 59','test 61',
#                  'test 62','test 63','test 71','test 72','test 73','test_add_timestamp','end']
INFORM_DICT = {}
dom = []

mr_create_time_dict = {}
MR_REMOTE_FILE_TIME_DIST = {}
MR_DOWNLOAD_IP = ''

#user-func global:
test_mre_event_num_dict = {'A1':{'num':0, 'time_str':[]}, 'A2':{'num':0, 'time_str':[]}, 'A3':{'num':0, 'time_str':[]}, 'A4':{'num':0, 'time_str':[]}, 'A5':{'num':0, 'time_str':[]},
                      'A6':{'num':0, 'time_str':[]}, 'B1':{'num':0, 'time_str':[]}, 'B2':{'num':0, 'time_str':[]}}
OUT_STR_LIST = []
OUT_DEBUG_LIST = []



# standard str
mrs_smr_target_dict = {'MR.RSRP':'MR.RSRP.00 MR.RSRP.01 MR.RSRP.02 MR.RSRP.03 MR.RSRP.04 MR.RSRP.05 MR.RSRP.06 MR.RSRP.07 MR.RSRP.08 MR.RSRP.09 MR.RSRP.10 MR.RSRP.11 MR.RSRP.12 MR.RSRP.13 MR.RSRP.14 MR.RSRP.15 MR.RSRP.16 MR.RSRP.17 MR.RSRP.18 MR.RSRP.19 MR.RSRP.20 MR.RSRP.21 MR.RSRP.22 MR.RSRP.23 MR.RSRP.24 MR.RSRP.25 MR.RSRP.26 MR.RSRP.27 MR.RSRP.28 MR.RSRP.29 MR.RSRP.30 MR.RSRP.31 MR.RSRP.32 MR.RSRP.33 MR.RSRP.34 MR.RSRP.35 MR.RSRP.36 MR.RSRP.37 MR.RSRP.38 MR.RSRP.39 MR.RSRP.40 MR.RSRP.41 MR.RSRP.42 MR.RSRP.43 MR.RSRP.44 MR.RSRP.45 MR.RSRP.46 MR.RSRP.47 ',\
                         'MR.RSRQ':'MR.RSRQ.00 MR.RSRQ.01 MR.RSRQ.02 MR.RSRQ.03 MR.RSRQ.04 MR.RSRQ.05 MR.RSRQ.06 MR.RSRQ.07 MR.RSRQ.08 MR.RSRQ.09 MR.RSRQ.10 MR.RSRQ.11 MR.RSRQ.12 MR.RSRQ.13 MR.RSRQ.14 MR.RSRQ.15 MR.RSRQ.16 MR.RSRQ.17 ',\
                         'MR.ReceivedIPower':'MR.ReceivedIPower.00 MR.ReceivedIPower.01 MR.ReceivedIPower.02 MR.ReceivedIPower.03 MR.ReceivedIPower.04 MR.ReceivedIPower.05 MR.ReceivedIPower.06 MR.ReceivedIPower.07 MR.ReceivedIPower.08 MR.ReceivedIPower.09 MR.ReceivedIPower.10 MR.ReceivedIPower.11 MR.ReceivedIPower.12 MR.ReceivedIPower.13 MR.ReceivedIPower.14 MR.ReceivedIPower.15 MR.ReceivedIPower.16 MR.ReceivedIPower.17 MR.ReceivedIPower.18 MR.ReceivedIPower.19 MR.ReceivedIPower.20 MR.ReceivedIPower.21 MR.ReceivedIPower.22 MR.ReceivedIPower.23 MR.ReceivedIPower.24 MR.ReceivedIPower.25 MR.ReceivedIPower.26 MR.ReceivedIPower.27 MR.ReceivedIPower.28 MR.ReceivedIPower.29 MR.ReceivedIPower.30 MR.ReceivedIPower.31 MR.ReceivedIPower.32 MR.ReceivedIPower.33 MR.ReceivedIPower.34 MR.ReceivedIPower.35 MR.ReceivedIPower.36 MR.ReceivedIPower.37 MR.ReceivedIPower.38 MR.ReceivedIPower.39 MR.ReceivedIPower.40 MR.ReceivedIPower.41 MR.ReceivedIPower.42 MR.ReceivedIPower.43 MR.ReceivedIPower.44 MR.ReceivedIPower.45 MR.ReceivedIPower.46 MR.ReceivedIPower.47 MR.ReceivedIPower.48 MR.ReceivedIPower.49 MR.ReceivedIPower.50 MR.ReceivedIPower.51 MR.ReceivedIPower.52 ',\
                         'MR.RIPPRB':'MR.RIPPRB.00 MR.RIPPRB.01 MR.RIPPRB.02 MR.RIPPRB.03 MR.RIPPRB.04 MR.RIPPRB.05 MR.RIPPRB.06 MR.RIPPRB.07 MR.RIPPRB.08 MR.RIPPRB.09 MR.RIPPRB.10 MR.RIPPRB.11 MR.RIPPRB.12 MR.RIPPRB.13 MR.RIPPRB.14 MR.RIPPRB.15 MR.RIPPRB.16 MR.RIPPRB.17 MR.RIPPRB.18 MR.RIPPRB.19 MR.RIPPRB.20 MR.RIPPRB.21 MR.RIPPRB.22 MR.RIPPRB.23 MR.RIPPRB.24 MR.RIPPRB.25 MR.RIPPRB.26 MR.RIPPRB.27 MR.RIPPRB.28 MR.RIPPRB.29 MR.RIPPRB.30 MR.RIPPRB.31 MR.RIPPRB.32 MR.RIPPRB.33 MR.RIPPRB.34 MR.RIPPRB.35 MR.RIPPRB.36 MR.RIPPRB.37 MR.RIPPRB.38 MR.RIPPRB.39 MR.RIPPRB.40 MR.RIPPRB.41 MR.RIPPRB.42 MR.RIPPRB.43 MR.RIPPRB.44 MR.RIPPRB.45 MR.RIPPRB.46 MR.RIPPRB.47 MR.RIPPRB.48 MR.RIPPRB.49 MR.RIPPRB.50 MR.RIPPRB.51 MR.RIPPRB.52 ',\
                         'MR.PowerHeadRoom':'MR.PowerHeadRoom.00 MR.PowerHeadRoom.01 MR.PowerHeadRoom.02 MR.PowerHeadRoom.03 MR.PowerHeadRoom.04 MR.PowerHeadRoom.05 MR.PowerHeadRoom.06 MR.PowerHeadRoom.07 MR.PowerHeadRoom.08 MR.PowerHeadRoom.09 MR.PowerHeadRoom.10 MR.PowerHeadRoom.11 MR.PowerHeadRoom.12 MR.PowerHeadRoom.13 MR.PowerHeadRoom.14 MR.PowerHeadRoom.15 MR.PowerHeadRoom.16 MR.PowerHeadRoom.17 MR.PowerHeadRoom.18 MR.PowerHeadRoom.19 MR.PowerHeadRoom.20 MR.PowerHeadRoom.21 MR.PowerHeadRoom.22 MR.PowerHeadRoom.23 MR.PowerHeadRoom.24 MR.PowerHeadRoom.25 MR.PowerHeadRoom.26 MR.PowerHeadRoom.27 MR.PowerHeadRoom.28 MR.PowerHeadRoom.29 MR.PowerHeadRoom.30 MR.PowerHeadRoom.31 MR.PowerHeadRoom.32 MR.PowerHeadRoom.33 MR.PowerHeadRoom.34 MR.PowerHeadRoom.35 MR.PowerHeadRoom.36 MR.PowerHeadRoom.37 MR.PowerHeadRoom.38 MR.PowerHeadRoom.39 MR.PowerHeadRoom.40 MR.PowerHeadRoom.41 MR.PowerHeadRoom.42 MR.PowerHeadRoom.43 MR.PowerHeadRoom.44 MR.PowerHeadRoom.45 MR.PowerHeadRoom.46 MR.PowerHeadRoom.47 MR.PowerHeadRoom.48 MR.PowerHeadRoom.49 MR.PowerHeadRoom.50 MR.PowerHeadRoom.51 MR.PowerHeadRoom.52 MR.PowerHeadRoom.53 MR.PowerHeadRoom.54 MR.PowerHeadRoom.55 MR.PowerHeadRoom.56 MR.PowerHeadRoom.57 MR.PowerHeadRoom.58 MR.PowerHeadRoom.59 MR.PowerHeadRoom.60 MR.PowerHeadRoom.61 MR.PowerHeadRoom.62 MR.PowerHeadRoom.63 ',
                         'MR.SinrUL': 'MR.SinrUL.00 MR.SinrUL.01 MR.SinrUL.02 MR.SinrUL.03 MR.SinrUL.04 MR.SinrUL.05 MR.SinrUL.06 MR.SinrUL.07 MR.SinrUL.08 MR.SinrUL.09 MR.SinrUL.10 MR.SinrUL.11 MR.SinrUL.12 MR.SinrUL.13 MR.SinrUL.14 MR.SinrUL.15 MR.SinrUL.16 MR.SinrUL.17 MR.SinrUL.18 MR.SinrUL.19 MR.SinrUL.20 MR.SinrUL.21 MR.SinrUL.22 MR.SinrUL.23 MR.SinrUL.24 MR.SinrUL.25 MR.SinrUL.26 MR.SinrUL.27 MR.SinrUL.28 MR.SinrUL.29 MR.SinrUL.30 MR.SinrUL.31 MR.SinrUL.32 MR.SinrUL.33 MR.SinrUL.34 MR.SinrUL.35 MR.SinrUL.36 '
                    }

mre_smr_target_str = 'MR.LteScRSRP MR.LteNcRSRP MR.LteScRSRQ MR.LteNcRSRQ MR.LteScEarfcn MR.LteScPci MR.LteNcEarfcn MR.LteNcPci MR.GsmNcellBcch MR.GsmNcellCarrierRSSI MR.GsmNcellNcc MR.GsmNcellBcc'

mro_smr_target_list = ['MR.LteScEarfcn MR.LteScPci MR.LteScRSRP MR.LteScRSRQ MR.LteScPHR MR.LteScSinrUL MR.LteNcEarfcn MR.LteNcPci MR.LteNcRSRP MR.LteNcRSRQ', 'MR.LteScRIP']

global_rsrp_list = [
    (0, 0, "MR.RSRP.00"),
    (1, 0, "MR.RSRP.00"),
    (2, 0, "MR.RSRP.00"),
    (3, 0, "MR.RSRP.00"),
    (4, 0, "MR.RSRP.00"),
    (5, 0, "MR.RSRP.00"),
    (6, 0, "MR.RSRP.00"),
    (7, 0, "MR.RSRP.00"),
    (8, 0, "MR.RSRP.00"),
    (9, 0, "MR.RSRP.00"),
    (10, 0, "MR.RSRP.00"),
    (11, 0, "MR.RSRP.00"),
    (12, 0, "MR.RSRP.00"),
    (13, 0, "MR.RSRP.00"),
    (14, 0, "MR.RSRP.00"),
    (15, 0, "MR.RSRP.00"),
    (16, 0, "MR.RSRP.00"),
    (17, 0, "MR.RSRP.00"),
    (18, 0, "MR.RSRP.00"),
    (19, 0, "MR.RSRP.00"),
    (20, 0, "MR.RSRP.00"),
    (21, 1, "MR.RSRP.01"),
    (22, 1, "MR.RSRP.01"),
    (23, 1, "MR.RSRP.01"),
    (24, 1, "MR.RSRP.01"),
    (25, 1, "MR.RSRP.01"),
    (26, 2, "MR.RSRP.02"),
    (27, 3, "MR.RSRP.03"),
    (28, 4, "MR.RSRP.04"),
    (29, 5, "MR.RSRP.05"),
    (30, 6, "MR.RSRP.06"),
    (31, 7, "MR.RSRP.07"),
    (32, 8, "MR.RSRP.08"),
    (33, 9, "MR.RSRP.09"),
    (34, 10, "MR.RSRP.10"),
    (35, 11, "MR.RSRP.11"),
    (36, 12, "MR.RSRP.12"),
    (37, 13, "MR.RSRP.13"),
    (38, 14, "MR.RSRP.14"),
    (39, 15, "MR.RSRP.15"),
    (40, 16, "MR.RSRP.16"),
    (41, 17, "MR.RSRP.17"),
    (42, 18, "MR.RSRP.18"),
    (43, 19, "MR.RSRP.19"),
    (44, 20, "MR.RSRP.20"),
    (45, 21, "MR.RSRP.21"),
    (46, 22, "MR.RSRP.22"),
    (47, 23, "MR.RSRP.23"),
    (48, 24, "MR.RSRP.24"),
    (49, 25, "MR.RSRP.25"),
    (50, 26, "MR.RSRP.26"),
    (51, 27, "MR.RSRP.27"),
    (52, 28, "MR.RSRP.28"),
    (53, 29, "MR.RSRP.29"),
    (54, 30, "MR.RSRP.30"),
    (55, 31, "MR.RSRP.31"),
    (56, 32, "MR.RSRP.32"),
    (57, 33, "MR.RSRP.33"),
    (58, 34, "MR.RSRP.34"),
    (59, 35, "MR.RSRP.35"),
    (60, 36, "MR.RSRP.36"),
    (61, 37, "MR.RSRP.37"),
    (62, 37, "MR.RSRP.37"),
    (63, 38, "MR.RSRP.38"),
    (64, 38, "MR.RSRP.38"),
    (65, 39, "MR.RSRP.39"),
    (66, 39, "MR.RSRP.39"),
    (67, 40, "MR.RSRP.40"),
    (68, 40, "MR.RSRP.40"),
    (69, 41, "MR.RSRP.41"),
    (70, 41, "MR.RSRP.41"),
    (71, 42, "MR.RSRP.42"),
    (72, 42, "MR.RSRP.42"),
    (73, 43, "MR.RSRP.43"),
    (74, 43, "MR.RSRP.43"),
    (75, 44, "MR.RSRP.44"),
    (76, 44, "MR.RSRP.44"),
    (77, 45, "MR.RSRP.45"),
    (78, 45, "MR.RSRP.45"),
    (79, 46, "MR.RSRP.46"),
    (80, 46, "MR.RSRP.46"),
    (81, 47, "MR.RSRP.47"),
    (82, 47, "MR.RSRP.47"),
    (83, 47, "MR.RSRP.47"),
    (84, 47, "MR.RSRP.47"),
    (85, 47, "MR.RSRP.47"),
    (86, 47, "MR.RSRP.47"),
    (87, 47, "MR.RSRP.47"),
    (88, 47, "MR.RSRP.47"),
    (89, 47, "MR.RSRP.47"),
    (90, 47, "MR.RSRP.47"),
    (91, 47, "MR.RSRP.47"),
    (92, 47, "MR.RSRP.47"),
    (93, 47, "MR.RSRP.47"),
    (94, 47, "MR.RSRP.47"),
    (95, 47, "MR.RSRP.47"),
    (96, 47, "MR.RSRP.47"),
    (97, 47, "MR.RSRP.47")
]


global_rsrq_list = [

    (0, 0, "MR.RSRQ.00"),
    (1, 1, "MR.RSRQ.01"),
    (2, 1, "MR.RSRQ.01"),
    (3, 2, "MR.RSRQ.02"),
    (4, 2, "MR.RSRQ.02"),
    (5, 3, "MR.RSRQ.03"),
    (6, 3, "MR.RSRQ.03"),
    (7, 4, "MR.RSRQ.04"),
    (8, 4, "MR.RSRQ.04"),
    (9, 5, "MR.RSRQ.05"),
    (10, 5, "MR.RSRQ.05"),
    (11, 6, "MR.RSRQ.06"),
    (12, 6, "MR.RSRQ.06"),
    (13, 7, "MR.RSRQ.07"),
    (14, 7, "MR.RSRQ.07"),
    (15, 8, "MR.RSRQ.08"),
    (16, 8, "MR.RSRQ.08"),
    (17, 9, "MR.RSRQ.09"),
    (18, 9, "MR.RSRQ.09"),
    (19, 10, "MR.RSRQ.10"),
    (20, 10, "MR.RSRQ.10"),
    (21, 11, "MR.RSRQ.11"),
    (22, 11, "MR.RSRQ.11"),
    (23, 12, "MR.RSRQ.12"),
    (24, 12, "MR.RSRQ.12"),
    (25, 13, "MR.RSRQ.13"),
    (26, 13, "MR.RSRQ.13"),
    (27, 14, "MR.RSRQ.14"),
    (28, 14, "MR.RSRQ.14"),
    (29, 15, "MR.RSRQ.15"),
    (30, 15, "MR.RSRQ.15"),
    (31, 16, "MR.RSRQ.16"),
    (32, 16, "MR.RSRQ.16"),
    (33, 17, "MR.RSRQ.17"),
    (34, 17, "MR.RSRQ.17")

]

k_list = [  -12.6, -12.55, -12.45, -12.35, -12.25,  -12.15,   -12.05,   -11.95,
            -11.85,   -11.75,   -11.65,  -11.55,   -11.45,   -11.35,   -11.25,   -11.15,
            -11.05,   -10.95,   -10.85,   -10.75,   -10.65,   -10.55,   -10.45,   -10.35,
            -10.25,   -10.15,   -10.05,   -9.95,    -9.85,    -9.75,    -9.65,    -9.55,
            -9.45,    -9.35,    -9.25,    -9.15,    -9.05,    -8.95,    -8.85,    -8.75,
            -8.65,    -8.55,   -8.45,    -8.35,    -8.25,    -8.15,    -8.05,    -7.95,
            -7.85,    -7.75,    -7.65,    -7.55,    -7.5        ]
























































#===========================================================
#   conf.xml  
#===========================================================
CONF_XML_DATA = u'''<?xml version="1.0" encoding="UTF-8"?>
<configure>
    <TEST_CONF>
        <test_total_time>1</test_total_time>
        <cellid>115</cellid>
        <enbid>115</enbid>
        <event>A1,A2,A3,A4,A5,A6,B1,B2</event>
        <standard_LTE>FDD-LTE</standard_LTE>
        <OEM>CMCC</OEM>
        <file_delay_time>30</file_delay_time>
        <is_57_out_excel>0</is_57_out_excel>
        <is_58_out_excel>0</is_58_out_excel>
        <is_59_out_excel>0</is_59_out_excel>
        <test_51>1</test_51>
        <test_52>1</test_52>
        <test_53>1</test_53>
        <test_54>1</test_54>
        <test_55>1</test_55>
        <test_56>1</test_56>
        <test_57>1</test_57>
        <test_58>1</test_58>
        <test_59>1</test_59>
        <test_61>1</test_61>
        <test_62>1</test_62>
        <test_63>1</test_63>
        <test_71>1</test_71>
        <test_72>1</test_72>
        <test_73>1</test_73>
        <ue_meas_id>22,23</ue_meas_id>
        <nc_pci_earfcn>112-1310,17-1350,417-1350,59-1350</nc_pci_earfcn>
        <ue_log_file_name>UELog1.txt</ue_log_file_name>
        <phr_file_name>2.csv</phr_file_name>
        <mr_path>../mr/</mr_path>
        <pm_path>../pm/</pm_path>
    </TEST_CONF>
    <MR_CONF>
        <SampleEndTime>0001-01-01T00:00:00Z</SampleEndTime>
        <MrPassword>test_mr</MrPassword>
        <UploadPeriod>15</UploadPeriod>
        <MrUrl>http://10.110.38.214:9000/pm</MrUrl>
        <MrUsername>test_pm</MrUsername>
        <SubFrameNum>2,3,4,7,8,9</SubFrameNum>
        <PrbNum>0,1,2,3,4,5,6,7,8,9</PrbNum>
        <MeasureType>MRO,MRE,MRS</MeasureType>
        <SamplePeriod>5120</SamplePeriod>
        <OmcName>NanoCellTestTool</OmcName>
        <MrEnable>1</MrEnable>
        <SampleBeginTime>0001-01-01T00:00:00Z</SampleBeginTime>
        <MRECGIList>all</MRECGIList>
        <MeasureItems>all</MeasureItems>
    </MR_CONF>
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