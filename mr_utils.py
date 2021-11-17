
import os
import re
import time
import datetime
import xml
import mr_globel as gl
write_info = lambda info:gl.str_info.append(str(info))


#MR文件xml的初始化,读取xml的文件
def MR_xml_init():
    gl.MR_DICT.clear()
    file_list = os.listdir(gl.MR_TEST_PATH)
    re_search_str = gl.TEST_CONF['standard_LTE'] + '_MR'
    for file in file_list:
        full_file = os.path.join(gl.MR_TEST_PATH, file)
        if  os.path.isdir(full_file) == False and re.search(re_search_str, file) != None:
#TODO : 可以添加 文件命名检测, 或者将名字存储到内存中,之后对应file的内容
            MR_FILE = {}
            MR_LIST = [{'MRO':'','MRE':'','MRS':''},{}, {}, {}]
#这里之前没有换成局部变量,导致MR_LIST只能存储一个时间测量的MRO,MRE,MRS,现在改成局部变量

            if MR_xml_file_name_accuracy(file) == False :
                continue
            file_data_list = file.split('_')


            MR_FILE['standard_LTE'] = file_data_list[0]
            MR_FILE['type'] = file_data_list[1]
            MR_FILE['OEM'] = file_data_list[2]
            MR_FILE['OmcName'] = file_data_list[3]
            MR_FILE['eNodeB'] = file_data_list[len(file_data_list) - 2]
            MR_FILE['SampleBeginTime'] = file_data_list[len(file_data_list) - 1].split('.')[0]

            if gl.MR_DICT.get(MR_FILE['SampleBeginTime']) == None:
                gl.MR_DICT[MR_FILE['SampleBeginTime']] = MR_LIST

            gl.MR_DICT[MR_FILE['SampleBeginTime']][0][MR_FILE['type']] = full_file
            for mr_list_entity in gl.MR_DICT:
                list_entity = gl.MR_DICT[mr_list_entity]
                if mr_list_entity == MR_FILE['SampleBeginTime']:
                    #list_entity.append(MR_FILE)
                    list_entity[gl.MR_TYPE[MR_FILE['type']]] = MR_FILE
                    break

    return



def print_mr_dict():
    for time_str in gl.MR_DICT:
        list_entity = gl.MR_DICT[time_str]
        write_info ("sample time : " + time_str)
        write_info (list_entity[0])
        write_info (list_entity[1].keys())
        write_info (list_entity[1].values())
        write_info (list_entity[2].keys())
        write_info (list_entity[2].values())
        write_info (list_entity[3].keys())
        write_info (list_entity[3].values())


def MR_xml_file_name_accuracy(file_name):
    file_name_list = file_name.split('\\')
    filename = file_name_list[len(file_name_list) - 1]

    if gl.TEST_CONF['standard_LTE'] != filename.split('_')[0]:
        return False
    if re.search(filename.split('_')[1], gl.MR_CONF['MeasureType']) == None:
        return False
    if gl.TEST_CONF['OEM'] != filename.split('_')[2]:
        return False
    if re.search(filename.split('_')[3], gl.MR_CONF['OmcName']) == None:
        return False
    if re.search(filename.split('_')[len(filename.split('_')) - 2], gl.TEST_CONF['enbid']) == None:
        return False
    time_stamp_str = filename.split('_')[len(filename.split('_')) - 1].split('.')[0]
    time_array = time.strptime(time_stamp_str, "%Y%m%d%H%M%S")
    timestamp = int(time.mktime(time_array))
    if timestamp % (60) != 0:
        return False
    return True


def string_to_list(dict_name, key_name, str):
    if dict_name.__contains__(key_name) == False:
        dict_name[key_name] = []
    dict_name[key_name].append(str)

def add_digital_string(digital_string):
    temp_count = 0
    for number_string in digital_string.split(' '):
        if number_string.isdigit() == True:
            temp_count += int(number_string)
    return temp_count

def is_str_format_time(str, format):
    try:
        datetime.datetime.strptime(str, format)
        return True
    except:
        return False

def mr_file_path_init():
    if gl.TEST_CONF['file_path'] != '':
        gl.TEST_PATH = gl.TEST_CONF['file_path']


def conf_xml_parse():
    full_file_name = os.path.join(gl.SOURCE_PATH, "conf.xml")
    #print (full_file_name)
    if os.path.exists(full_file_name):
        conf_dom = xml.dom.minidom.parse(full_file_name)
        conf_root = conf_dom.documentElement
        #print (conf_root.nodeName)

        #解析TEST_CONF, 就是手动输入测试相关的信息,包括测试的总时间, 小区, 邻区id等
        test_conf_list = conf_root.getElementsByTagName("TEST_CONF")
        for test_conf_entity in test_conf_list:
            for test_conf_dict_key_entity in gl.TEST_CONF:
                gl.TEST_CONF[test_conf_dict_key_entity] = test_conf_entity.getElementsByTagName(test_conf_dict_key_entity)[0].firstChild.data
                #print (test_conf_dict_key_entity + TEST_CONF[test_conf_dict_key_entity])

        #解析MR_CONF, 这个是下发的MR的测试命令
        mr_conf_list = conf_root.getElementsByTagName("MR_CONF")
        for mr_conf_entity in mr_conf_list:
            for mr_conf_dict_key_entity in gl.MR_CONF:
                gl.MR_CONF[mr_conf_dict_key_entity] = mr_conf_entity.getElementsByTagName(mr_conf_dict_key_entity)[0].firstChild.data
                #print( mr_conf_dict_key_entity + " - " + MR_CONF[mr_conf_dict_key_entity])

        #解析TEST_OUT, 这个是最后输出的项 分别对应测试文档中的每个项
        test_out_list = conf_root.getElementsByTagName("TEST_OUT")
        for test_out_entity in test_out_list:
            for test_out_dict_key_entity in gl.TEST_OUT:
                tmp_list = []
                tmp_list.append( int(test_out_entity.getElementsByTagName(test_out_dict_key_entity)[0].getAttribute("item_num") ) )
                for i in range(tmp_list[0]):
                    tmp_list.append(int(test_out_entity.getElementsByTagName(test_out_dict_key_entity)[0].getAttribute("item" + '%d'%(i+1)) ))
                gl.TEST_OUT[test_out_dict_key_entity] = tmp_list
                #print (TEST_OUT[test_out_dict_key_entity])

        #解析ITEM_NAME, 这个是输出项需要对应的测试项,也就是测试文档中每个测试表中的列
        item_name_list = conf_root.getElementsByTagName("ITEM_NAME")
        for item_name_entity in item_name_list:
            item_entity_list = item_name_entity.getElementsByTagName("item")
            gl.TEST_ITEM_LIST.append(len(item_entity_list))
            for i in range(len(item_entity_list)):
                gl.TEST_ITEM_LIST.append(item_entity_list[i].firstChild.data )
                #print (TEST_ITEM_LIST[i+1])


    else:
        write_info ('no conf.xml file')

def get_time_format(format="%Y:%m:%d %H:%M:%S"):
    temp_time = time.time()
    localtime = time.localtime(temp_time)
    date_time = time.strftime(format, localtime)
    return date_time

def get_time_format_by_timestamp(time_stamp, format="%Y-%m-%dT%H:%M:%S.%f"):
    d = datetime.datetime.fromtimestamp(time_stamp/1000)
    date_time = d.strftime(format)
    return date_time

def get_timestamp_by_str_format(time_str, format="%Y-%m-%dT%H:%M:%S.%f"):
    time_array = datetime.datetime.strptime(time_str, format)
    timestamp = int(time.mktime(time_array.timetuple())*1000.0 + time_array.microsecond/1000.0)
    return timestamp


def is_mro_correct(full_file_name):

    smr_target_list = ['MR.LteScEarfcn MR.LteScPci MR.LteScRSRP MR.LteScRSRQ MR.LteScPHR MR.LteScSinrUL MR.LteNcEarfcn MR.LteNcPci MR.LteNcRSRP MR.LteNcRSRQ', 'MR.LteScRIP']

    if re.search(r'MRO', full_file_name) == None:
        return True, 'file name not mro'
    mro_dom = xml.dom.minidom.parse(full_file_name)
    mro_root = mro_dom.documentElement
    if mro_root.nodeName != 'bulkPmMrDataFile':
        return False,'bulkPmMrDataFile'
    fileHeader_list = mro_root.getElementsByTagName('fileHeader')
    if len(fileHeader_list) != 1:
        return False,'fileHeader'
    eNB_list = mro_root.getElementsByTagName('eNB')
    if len(eNB_list) != len(gl.TEST_CONF['cellid'].split(',')):
        return False,'eNB_id not match'
    if len(eNB_list) == 0 and (len(mro_root.getElementsByTagName('measurement')) != 0 or len(mro_root.getElementsByTagName('smr')) != 0 or len(mro_root.getElementsByTagName('object')) != 0):
        return False, 'format error enb'
    elif len(eNB_list) == 0:
        return True,'no enb'

    for eNB_entity in eNB_list:
        if re.search(eNB_entity.getAttribute('id') , gl.TEST_CONF['cellid']) == None:
            return False, 'eNB_id not match'
        measurement_list = eNB_entity.getElementsByTagName('measurement')
        if len(measurement_list) == 0 and (len(mro_root.getElementsByTagName('smr')) != 0 or len(mro_root.getElementsByTagName('object')) != 0):
            return False, 'format error measurement'
        elif len(measurement_list) == 0:
            return True,'correct'
        for measurement_entity in measurement_list:
            smr_list = measurement_entity.getElementsByTagName('smr')
            if len(smr_list) != 1 and len(smr_list) != 0:
                return False, 'smr format error'+str(len(smr_list))
            for mr_item in smr_list[0].firstChild.data.strip().split(' '):
                if re.search(mr_item, smr_target_list[0]) == None and re.search(mr_item, smr_target_list[1]) == None and is_mr_item_need_exist(mr_item) == True:
                    return False, 'smr not match  <%s>'%(mr_item)

    return True,'correct'


def is_mre_correct(full_file_name):
    smr_target_str = 'MR.LteScRSRP MR.LteNcRSRP MR.LteScRSRQ MR.LteNcRSRQ MR.LteScEarfcn MR.LteScPci MR.LteNcEarfcn MR.LteNcPci MR.GsmNcellBcch MR.GsmNcellCarrierRSSI MR.GsmNcellNcc MR.GsmNcellBcc'

    if re.search(r'MRE', full_file_name) == None:
        return True, 'file name not mre'
    mre_dom = xml.dom.minidom.parse(full_file_name)
    mre_root = mre_dom.documentElement
    if mre_root.nodeName != 'bulkPmMrDataFile':
        return False, 'bulkPmMrDataFile'
    fileHeader_list = mre_root.getElementsByTagName('fileHeader')
    if len(fileHeader_list) != 1:
        return False, 'fileHeader'
    eNB_list = mre_root.getElementsByTagName('eNB')
    if len(eNB_list) != len(gl.TEST_CONF['cellid'].split(',')):
        return False, 'eNB id not match'
    if len(eNB_list) == 0 and (len(mre_root.getElementsByTagName('measurement')) != 0 or len(mre_root.getElementsByTagName('smr')) != 0 or len(mre_root.getElementsByTagName('object')) != 0):
        return False, 'format error'
    elif len(eNB_list) == 0:
        return True,'correct'

    for eNB_entity in eNB_list:
        if re.search(eNB_entity.getAttribute('id') , gl.TEST_CONF['cellid']) == None:
            return False, 'eNB id not match'
        measurement_list = eNB_entity.getElementsByTagName('measurement')
        if len(measurement_list) == 0 and (len(mre_root.getElementsByTagName('smr')) != 0 or len(mre_root.getElementsByTagName('object')) != 0):
            return False, 'format error'
        elif len(measurement_list) == 0:
            return True,'correct'
        for measurement_entity in measurement_list:
            smr_list = measurement_entity.getElementsByTagName('smr')
            if len(smr_list) != 1 and len(smr_list) != 0:
                return False, 'smr error'
            for mr_item in smr_list[0].firstChild.data.strip().split(' '):
                if re.search(mr_item, smr_target_str) == None and is_mr_item_need_exist(mr_item) == True:
                    return False, 'smr not match <%s>' % (mr_item)

    return True,'correct'

def is_mrs_correct(full_file_name):
    smr_target_list = ['MR.RSRP.00 MR.RSRP.01 MR.RSRP.02 MR.RSRP.03 MR.RSRP.04 MR.RSRP.05 MR.RSRP.06 MR.RSRP.07 MR.RSRP.08 MR.RSRP.09 MR.RSRP.10 MR.RSRP.11 MR.RSRP.12 MR.RSRP.13 MR.RSRP.14 MR.RSRP.15 MR.RSRP.16 MR.RSRP.17 MR.RSRP.18 MR.RSRP.19 MR.RSRP.20 MR.RSRP.21 MR.RSRP.22 MR.RSRP.23 MR.RSRP.24 MR.RSRP.25 MR.RSRP.26 MR.RSRP.27 MR.RSRP.28 MR.RSRP.29 MR.RSRP.30 MR.RSRP.31 MR.RSRP.32 MR.RSRP.33 MR.RSRP.34 MR.RSRP.35 MR.RSRP.36 MR.RSRP.37 MR.RSRP.38 MR.RSRP.39 MR.RSRP.40 MR.RSRP.41 MR.RSRP.42 MR.RSRP.43 MR.RSRP.44 MR.RSRP.45 MR.RSRP.46 MR.RSRP.47 ',
                       'MR.RSRQ.00 MR.RSRQ.01 MR.RSRQ.02 MR.RSRQ.03 MR.RSRQ.04 MR.RSRQ.05 MR.RSRQ.06 MR.RSRQ.07 MR.RSRQ.08 MR.RSRQ.09 MR.RSRQ.10 MR.RSRQ.11 MR.RSRQ.12 MR.RSRQ.13 MR.RSRQ.14 MR.RSRQ.15 MR.RSRQ.16 MR.RSRQ.17 ',
                       'MR.SinrUL.00 MR.SinrUL.01 MR.SinrUL.02 MR.SinrUL.03 MR.SinrUL.04 MR.SinrUL.05 MR.SinrUL.06 MR.SinrUL.07 MR.SinrUL.08 MR.SinrUL.09 MR.SinrUL.10 MR.SinrUL.11 MR.SinrUL.12 MR.SinrUL.13 MR.SinrUL.14 MR.SinrUL.15 MR.SinrUL.16 MR.SinrUL.17 MR.SinrUL.18 MR.SinrUL.19 MR.SinrUL.20 MR.SinrUL.21 MR.SinrUL.22 MR.SinrUL.23 MR.SinrUL.24 MR.SinrUL.25 MR.SinrUL.26 MR.SinrUL.27 MR.SinrUL.28 MR.SinrUL.29 MR.SinrUL.30 MR.SinrUL.31 MR.SinrUL.32 MR.SinrUL.33 MR.SinrUL.34 MR.SinrUL.35 MR.SinrUL.36',
                       'MR.ReceivedIPower.00 MR.ReceivedIPower.01 MR.ReceivedIPower.02 MR.ReceivedIPower.03 MR.ReceivedIPower.04 MR.ReceivedIPower.05 MR.ReceivedIPower.06 MR.ReceivedIPower.07 MR.ReceivedIPower.08 MR.ReceivedIPower.09 MR.ReceivedIPower.10 MR.ReceivedIPower.11 MR.ReceivedIPower.12 MR.ReceivedIPower.13 MR.ReceivedIPower.14 MR.ReceivedIPower.15 MR.ReceivedIPower.16 MR.ReceivedIPower.17 MR.ReceivedIPower.18 MR.ReceivedIPower.19 MR.ReceivedIPower.20 MR.ReceivedIPower.21 MR.ReceivedIPower.22 MR.ReceivedIPower.23 MR.ReceivedIPower.24 MR.ReceivedIPower.25 MR.ReceivedIPower.26 MR.ReceivedIPower.27 MR.ReceivedIPower.28 MR.ReceivedIPower.29 MR.ReceivedIPower.30 MR.ReceivedIPower.31 MR.ReceivedIPower.32 MR.ReceivedIPower.33 MR.ReceivedIPower.34 MR.ReceivedIPower.35 MR.ReceivedIPower.36 MR.ReceivedIPower.37 MR.ReceivedIPower.38 MR.ReceivedIPower.39 MR.ReceivedIPower.40 MR.ReceivedIPower.41 MR.ReceivedIPower.42 MR.ReceivedIPower.43 MR.ReceivedIPower.44 MR.ReceivedIPower.45 MR.ReceivedIPower.46 MR.ReceivedIPower.47 MR.ReceivedIPower.48 MR.ReceivedIPower.49 MR.ReceivedIPower.50 MR.ReceivedIPower.51 MR.ReceivedIPower.52 ',
                       'MR.RIPPRB.00 MR.RIPPRB.01 MR.RIPPRB.02 MR.RIPPRB.03 MR.RIPPRB.04 MR.RIPPRB.05 MR.RIPPRB.06 MR.RIPPRB.07 MR.RIPPRB.08 MR.RIPPRB.09 MR.RIPPRB.10 MR.RIPPRB.11 MR.RIPPRB.12 MR.RIPPRB.13 MR.RIPPRB.14 MR.RIPPRB.15 MR.RIPPRB.16 MR.RIPPRB.17 MR.RIPPRB.18 MR.RIPPRB.19 MR.RIPPRB.20 MR.RIPPRB.21 MR.RIPPRB.22 MR.RIPPRB.23 MR.RIPPRB.24 MR.RIPPRB.25 MR.RIPPRB.26 MR.RIPPRB.27 MR.RIPPRB.28 MR.RIPPRB.29 MR.RIPPRB.30 MR.RIPPRB.31 MR.RIPPRB.32 MR.RIPPRB.33 MR.RIPPRB.34 MR.RIPPRB.35 MR.RIPPRB.36 MR.RIPPRB.37 MR.RIPPRB.38 MR.RIPPRB.39 MR.RIPPRB.40 MR.RIPPRB.41 MR.RIPPRB.42 MR.RIPPRB.43 MR.RIPPRB.44 MR.RIPPRB.45 MR.RIPPRB.46 MR.RIPPRB.47 MR.RIPPRB.48 MR.RIPPRB.49 MR.RIPPRB.50 MR.RIPPRB.51 MR.RIPPRB.52 ',
                       'MR.PowerHeadRoom.00 MR.PowerHeadRoom.01 MR.PowerHeadRoom.02 MR.PowerHeadRoom.03 MR.PowerHeadRoom.04 MR.PowerHeadRoom.05 MR.PowerHeadRoom.06 MR.PowerHeadRoom.07 MR.PowerHeadRoom.08 MR.PowerHeadRoom.09 MR.PowerHeadRoom.10 MR.PowerHeadRoom.11 MR.PowerHeadRoom.12 MR.PowerHeadRoom.13 MR.PowerHeadRoom.14 MR.PowerHeadRoom.15 MR.PowerHeadRoom.16 MR.PowerHeadRoom.17 MR.PowerHeadRoom.18 MR.PowerHeadRoom.19 MR.PowerHeadRoom.20 MR.PowerHeadRoom.21 MR.PowerHeadRoom.22 MR.PowerHeadRoom.23 MR.PowerHeadRoom.24 MR.PowerHeadRoom.25 MR.PowerHeadRoom.26 MR.PowerHeadRoom.27 MR.PowerHeadRoom.28 MR.PowerHeadRoom.29 MR.PowerHeadRoom.30 MR.PowerHeadRoom.31 MR.PowerHeadRoom.32 MR.PowerHeadRoom.33 MR.PowerHeadRoom.34 MR.PowerHeadRoom.35 MR.PowerHeadRoom.36 MR.PowerHeadRoom.37 MR.PowerHeadRoom.38 MR.PowerHeadRoom.39 MR.PowerHeadRoom.40 MR.PowerHeadRoom.41 MR.PowerHeadRoom.42 MR.PowerHeadRoom.43 MR.PowerHeadRoom.44 MR.PowerHeadRoom.45 MR.PowerHeadRoom.46 MR.PowerHeadRoom.47 MR.PowerHeadRoom.48 MR.PowerHeadRoom.49 MR.PowerHeadRoom.50 MR.PowerHeadRoom.51 MR.PowerHeadRoom.52 MR.PowerHeadRoom.53 MR.PowerHeadRoom.54 MR.PowerHeadRoom.55 MR.PowerHeadRoom.56 MR.PowerHeadRoom.57 MR.PowerHeadRoom.58 MR.PowerHeadRoom.59 MR.PowerHeadRoom.60 MR.PowerHeadRoom.61 MR.PowerHeadRoom.62 MR.PowerHeadRoom.63 ']

    if re.search(r'MRS', full_file_name) == None:
        return True, 'file name not MRS'
    mrs_dom = xml.dom.minidom.parse(full_file_name)
    mrs_root = mrs_dom.documentElement
    if mrs_root.nodeName != 'bulkPmMrDataFile':
        return False, 'bulkPmMrDataFile'
    fileHeader_list = mrs_root.getElementsByTagName('fileHeader')
    if len(fileHeader_list) != 1:
        return False, 'fileHeader'
    eNB_list = mrs_root.getElementsByTagName('eNB')
    if len(eNB_list) != len(gl.TEST_CONF['cellid'].split(',')):
        return False, 'eNB_id not match'
    if len(eNB_list) == 0 and (len(mrs_root.getElementsByTagName('measurement')) != 0 or len(mrs_root.getElementsByTagName('smr')) != 0 or len(mrs_root.getElementsByTagName('object')) != 0):
        return False, 'format error'
    elif len(eNB_list) == 0:
        return True,'correct'

    for eNB_entity in eNB_list:
        if re.search(eNB_entity.getAttribute('id') , gl.TEST_CONF['cellid']) == None:
            return False, 'eNB_id not match'
        measurement_list = eNB_entity.getElementsByTagName('measurement')
        if len(measurement_list) == 0 and (len(mrs_root.getElementsByTagName('smr')) != 0 or len(mrs_root.getElementsByTagName('object')) != 0):
            return False, 'format error1'
        elif len(measurement_list) == 0:
            return True,'correct'
        for measurement_entity in measurement_list:
            smr_list = measurement_entity.getElementsByTagName('smr')
            if len(smr_list) != 1 and len(smr_list) != 0:
                return False, 'smr error'
            if smr_list[0].firstChild.data not in  smr_target_list and is_mr_item_need_exist(measurement_entity.getAttribute('mrName')) == True:
                return False, 'smr not match <%s>'%( measurement_entity.getAttribute('mrName'))

    return True,'correct'

def test_out_data_item_header(out_type):
    with open(gl.OUT_PATH, 'a') as file_object:
        file_object.write("\n<----------------------->\n\n---------" + out_type + "---------\n")

        for i in range( gl.TEST_OUT[out_type][0]):
            file_object.write(gl.TEST_ITEM_LIST[gl.TEST_OUT[out_type][i+1]])
            file_object.write(" | ");
        file_object.write("\n")


def is_cell_id_exist(eciid):
    cell_id = eciid & 0xff
    if str(cell_id) in gl.TEST_CONF['cellid'].split(','):
        return True, cell_id
    else:
        return False,cell_id

def is_eci_correct_by_MRECGIList(eciid):
    if gl.MR_CONF['MRECGIList'] == 'all':
        return True
    ecgi_list = gl.MR_CONF['MRECGIList'].split(',')
    for ecgi_entity in ecgi_list:
        eci = int(ecgi_entity.split('-')[1])
        if int(eciid) == eci:
            return True
    return False

def is_eci_correct(eci_id):
    cell_id_list = gl.TEST_CONF['cellid'].split(',')
    enb_id_list = gl.TEST_CONF['enbid'].split(',')

    eci_id_list = []
    for i in range(len(cell_id_list)):
        for j in range(len(enb_id_list)):
            temp_eci_id = (int(enb_id_list[j]) << 8) | int(cell_id_list[i])
            eci_id_list.append(temp_eci_id)
    if eci_id in eci_id_list and is_eci_correct_by_MRECGIList(eci_id):
        return True
    return False



def is_mr_item_need_exist(mr_name):
    if gl.MR_CONF['MeasureItems'] == 'all':
        return True
    elif re.search(mr_name, gl.MR_CONF['MeasureItems']) != None:
        return True
    return False

def is_enb_id_exist(enb_id):
    if re.search(str(enb_id), gl.TEST_CONF['enbid']) == None:
        return False
    else:
        return True


def get_mr_item_pos(mr_name_dict, smr_str):
    smr_list = smr_str.split(' ')
    for mr_name in mr_name_dict:
        temp_flag = 0
        for i in range(len(smr_list)):
            if mr_name == smr_list[i]:
                if mr_name_dict.__contains__(mr_name) == False:
                    mr_name_dict[mr_name] = {'pos':0}
                if mr_name_dict[mr_name].__contains__('pos') == False:
                    mr_name_dict[mr_name]['pos'] = 0
                mr_name_dict[mr_name]['pos'] = i
                temp_flag = 1
                break
        if temp_flag == 0:
            if mr_name_dict.__contains__(mr_name) == False:
                mr_name_dict[mr_name] = {'pos':0}
            if mr_name_dict[mr_name].__contains__('pos') == False:
                mr_name_dict[mr_name]['pos'] = 0
            mr_name_dict[mr_name]['pos'] = 0

def get_mre_pos_list_by_mapping(mre_conf_dict, smr_str):
    standard_smr_str_list = ['MR.LteScRSRP','MR.LteNcRSRP', 'MR.LteScRSRQ', 'MR.LteNcRSRQ', 'MR.LteScEarfcn', 'MR.LteScPci', 'MR.LteNcEarfcn',\
                             'MR.LteNcPci', 'MR.GsmNcellBcch', 'MR.GsmNcellCarrierRSSI', 'MR.GsmNcellNcc', 'MR.GsmNcellBcc']
    mre_smr_head = 'MR.LteScRSRP MR.LteNcRSRP MR.LteScRSRQ MR.LteNcRSRQ MR.LteScEarfcn MR.LteScPci MR.LteNcEarfcn MR.LteNcPci MR.GsmNcellBcch MR.GsmNcellCarrierRSSI MR.GsmNcellNcc MR.GsmNcellBcc'
    if smr_str == mre_smr_head:
        return
    smr_list = smr_str.split(' ')
    for mre_event in mre_conf_dict:
        temp_pos_list = mre_conf_dict[mre_event]['pos'][:]
        mre_conf_dict[mre_event]['pos'].clear()
        for i in range(len(smr_list)):
            for j in range(len(temp_pos_list)):
                if standard_smr_str_list[temp_pos_list[j]] == smr_list[i]:
                    mre_conf_dict[mre_event]['pos'].append(i)
                    break
def get_mro_pos_list_by_mapping(mro_conf_dict, smr_str):
    standard_smr_str_list = ['MR.LteScEarfcn', 'MR.LteScPci', 'MR.LteScRSRP', 'MR.LteScRSRQ', 'MR.LteScPHR', 'MR.LteScSinrUL', 'MR.LteNcEarfcn', 'MR.LteNcPci',\
                             'MR.LteNcRSRP', 'MR.LteNcRSRQ' ]
    mro_smr_head = 'MR.LteScEarfcn MR.LteScPci MR.LteScRSRP MR.LteScRSRQ MR.LteScPHR MR.LteScSinrUL MR.LteNcEarfcn MR.LteNcPci MR.LteNcRSRP MR.LteNcRSRQ '
    if mro_smr_head.strip() == smr_str.strip():
        return
    smr_list = smr_str.split(' ')
    for mr_name in mro_conf_dict:
        if mro_conf_dict[mr_name].__contains__('pos') == False:
            continue
        temp_flag = 0
        for i in range(len(smr_list)):
            if smr_list[i] == mr_name:
                mro_conf_dict[mr_name]['pos'] = i
                temp_flag = 1
                break
        if temp_flag == 0:
            mro_conf_dict[mr_name]['pos'] = -1


def out_text_dict_append_list(out_dict, key, str):
    if out_dict.__contains__(key) == False:
        out_dict[key] = []
    out_dict[key].append(str)

def get_measureItem_list(mr_dict):
    measure_item_list = ['MR.RSRP','MR.RSRQ','MR.ReceivedIPower','MR.PowerHeadRoom','MR.SinrUL','MR.RIPPRB','MR.RsrpRsrq','MR.RipRsrp','MR.RipRsrq','MR.SinrULRip',\
        'MR.LteScRSRP','MR.LteNcRSRP','MR.LteScRSRQ','MR.LteNcRSRQ','MR.LteScPHR','MR.LteScRIP','MR.LteScSinrUL','MR.LteScEarfcn','MR.LteScPci','MR.LteNcEarfcn',\
                         'MR.LteNcPci','MR.GsmNcellBcch','MR.GsmNcellCarrierRSSI','MR.GsmNcellNcc','MR.GsmNcellBcc']
    if gl.MR_CONF['MeasureItems'] == 'all':
        for i in range(len(measure_item_list)):
            mr_dict[measure_item_list[i]] = 0
    else:
        meas_list = gl.MR_CONF['MeasureItems'].split(',')
        for i in range(len(meas_list)):
            for j in range(len(measure_item_list)):
                if meas_list[i] == measure_item_list[j]:
                    mr_dict[meas_list[i]] = 0

def is_mr_value_correct(smr_str, value_str):
    smr_list = smr_str.strip().split(' ')
    value_list = value_str.strip().split(' ')
    range_dict = {'MR.LteScRSRP':[0, 97],'MR.LteNcRSRP':[0, 97],'MR.LteScRSRQ':[0, 34],'MR.LteNcRSRQ':[0, 34],'MR.LteScPHR':[0, 63],'MR.LteScRIP':[0, 511],\
                  'MR.LteScSinrUL':[0, 36],'MR.LteScEarfcn':[0, 41589],'MR.LteScPci':[0, 503],'MR.LteNcEarfcn':[0, 41589],\
                         'MR.LteNcPci':[0, 503],'MR.GsmNcellBcch':[0, 1023],'MR.GsmNcellCarrierRSSI':[0, 63],'MR.GsmNcellNcc':[0, 7],'MR.GsmNcellBcc':[0, 7]}
    if len(smr_list) != len(value_list):
        return False
    for i in range(len(smr_list)):
        if range_dict.__contains__(smr_list[i]) == False:
            return False
        if value_list[i].isdigit() == False:
            continue
        if int(value_list[i]) < range_dict[smr_list[i]][0] or int(value_list[i]) > range_dict[smr_list[i]][1]:
            return False
    return True

def is_mrs_measurement_smr_value_correct(mr_name, smr_str, value_str):
    smr_standard_dict = {'MR.RSRP':'MR.RSRP.00 MR.RSRP.01 MR.RSRP.02 MR.RSRP.03 MR.RSRP.04 MR.RSRP.05 MR.RSRP.06 MR.RSRP.07 MR.RSRP.08 MR.RSRP.09 MR.RSRP.10 MR.RSRP.11 MR.RSRP.12 MR.RSRP.13 MR.RSRP.14 MR.RSRP.15 MR.RSRP.16 MR.RSRP.17 MR.RSRP.18 MR.RSRP.19 MR.RSRP.20 MR.RSRP.21 MR.RSRP.22 MR.RSRP.23 MR.RSRP.24 MR.RSRP.25 MR.RSRP.26 MR.RSRP.27 MR.RSRP.28 MR.RSRP.29 MR.RSRP.30 MR.RSRP.31 MR.RSRP.32 MR.RSRP.33 MR.RSRP.34 MR.RSRP.35 MR.RSRP.36 MR.RSRP.37 MR.RSRP.38 MR.RSRP.39 MR.RSRP.40 MR.RSRP.41 MR.RSRP.42 MR.RSRP.43 MR.RSRP.44 MR.RSRP.45 MR.RSRP.46 MR.RSRP.47 ',\
                         'MR.RSRQ':'MR.RSRQ.00 MR.RSRQ.01 MR.RSRQ.02 MR.RSRQ.03 MR.RSRQ.04 MR.RSRQ.05 MR.RSRQ.06 MR.RSRQ.07 MR.RSRQ.08 MR.RSRQ.09 MR.RSRQ.10 MR.RSRQ.11 MR.RSRQ.12 MR.RSRQ.13 MR.RSRQ.14 MR.RSRQ.15 MR.RSRQ.16 MR.RSRQ.17 ',\
                         'MR.ReceivedIPower':'MR.ReceivedIPower.00 MR.ReceivedIPower.01 MR.ReceivedIPower.02 MR.ReceivedIPower.03 MR.ReceivedIPower.04 MR.ReceivedIPower.05 MR.ReceivedIPower.06 MR.ReceivedIPower.07 MR.ReceivedIPower.08 MR.ReceivedIPower.09 MR.ReceivedIPower.10 MR.ReceivedIPower.11 MR.ReceivedIPower.12 MR.ReceivedIPower.13 MR.ReceivedIPower.14 MR.ReceivedIPower.15 MR.ReceivedIPower.16 MR.ReceivedIPower.17 MR.ReceivedIPower.18 MR.ReceivedIPower.19 MR.ReceivedIPower.20 MR.ReceivedIPower.21 MR.ReceivedIPower.22 MR.ReceivedIPower.23 MR.ReceivedIPower.24 MR.ReceivedIPower.25 MR.ReceivedIPower.26 MR.ReceivedIPower.27 MR.ReceivedIPower.28 MR.ReceivedIPower.29 MR.ReceivedIPower.30 MR.ReceivedIPower.31 MR.ReceivedIPower.32 MR.ReceivedIPower.33 MR.ReceivedIPower.34 MR.ReceivedIPower.35 MR.ReceivedIPower.36 MR.ReceivedIPower.37 MR.ReceivedIPower.38 MR.ReceivedIPower.39 MR.ReceivedIPower.40 MR.ReceivedIPower.41 MR.ReceivedIPower.42 MR.ReceivedIPower.43 MR.ReceivedIPower.44 MR.ReceivedIPower.45 MR.ReceivedIPower.46 MR.ReceivedIPower.47 MR.ReceivedIPower.48 MR.ReceivedIPower.49 MR.ReceivedIPower.50 MR.ReceivedIPower.51 MR.ReceivedIPower.52 ',\
                         'MR.RIPPRB':'MR.RIPPRB.00 MR.RIPPRB.01 MR.RIPPRB.02 MR.RIPPRB.03 MR.RIPPRB.04 MR.RIPPRB.05 MR.RIPPRB.06 MR.RIPPRB.07 MR.RIPPRB.08 MR.RIPPRB.09 MR.RIPPRB.10 MR.RIPPRB.11 MR.RIPPRB.12 MR.RIPPRB.13 MR.RIPPRB.14 MR.RIPPRB.15 MR.RIPPRB.16 MR.RIPPRB.17 MR.RIPPRB.18 MR.RIPPRB.19 MR.RIPPRB.20 MR.RIPPRB.21 MR.RIPPRB.22 MR.RIPPRB.23 MR.RIPPRB.24 MR.RIPPRB.25 MR.RIPPRB.26 MR.RIPPRB.27 MR.RIPPRB.28 MR.RIPPRB.29 MR.RIPPRB.30 MR.RIPPRB.31 MR.RIPPRB.32 MR.RIPPRB.33 MR.RIPPRB.34 MR.RIPPRB.35 MR.RIPPRB.36 MR.RIPPRB.37 MR.RIPPRB.38 MR.RIPPRB.39 MR.RIPPRB.40 MR.RIPPRB.41 MR.RIPPRB.42 MR.RIPPRB.43 MR.RIPPRB.44 MR.RIPPRB.45 MR.RIPPRB.46 MR.RIPPRB.47 MR.RIPPRB.48 MR.RIPPRB.49 MR.RIPPRB.50 MR.RIPPRB.51 MR.RIPPRB.52 ',\
                         'MR.PowerHeadRoom':'MR.PowerHeadRoom.00 MR.PowerHeadRoom.01 MR.PowerHeadRoom.02 MR.PowerHeadRoom.03 MR.PowerHeadRoom.04 MR.PowerHeadRoom.05 MR.PowerHeadRoom.06 MR.PowerHeadRoom.07 MR.PowerHeadRoom.08 MR.PowerHeadRoom.09 MR.PowerHeadRoom.10 MR.PowerHeadRoom.11 MR.PowerHeadRoom.12 MR.PowerHeadRoom.13 MR.PowerHeadRoom.14 MR.PowerHeadRoom.15 MR.PowerHeadRoom.16 MR.PowerHeadRoom.17 MR.PowerHeadRoom.18 MR.PowerHeadRoom.19 MR.PowerHeadRoom.20 MR.PowerHeadRoom.21 MR.PowerHeadRoom.22 MR.PowerHeadRoom.23 MR.PowerHeadRoom.24 MR.PowerHeadRoom.25 MR.PowerHeadRoom.26 MR.PowerHeadRoom.27 MR.PowerHeadRoom.28 MR.PowerHeadRoom.29 MR.PowerHeadRoom.30 MR.PowerHeadRoom.31 MR.PowerHeadRoom.32 MR.PowerHeadRoom.33 MR.PowerHeadRoom.34 MR.PowerHeadRoom.35 MR.PowerHeadRoom.36 MR.PowerHeadRoom.37 MR.PowerHeadRoom.38 MR.PowerHeadRoom.39 MR.PowerHeadRoom.40 MR.PowerHeadRoom.41 MR.PowerHeadRoom.42 MR.PowerHeadRoom.43 MR.PowerHeadRoom.44 MR.PowerHeadRoom.45 MR.PowerHeadRoom.46 MR.PowerHeadRoom.47 MR.PowerHeadRoom.48 MR.PowerHeadRoom.49 MR.PowerHeadRoom.50 MR.PowerHeadRoom.51 MR.PowerHeadRoom.52 MR.PowerHeadRoom.53 MR.PowerHeadRoom.54 MR.PowerHeadRoom.55 MR.PowerHeadRoom.56 MR.PowerHeadRoom.57 MR.PowerHeadRoom.58 MR.PowerHeadRoom.59 MR.PowerHeadRoom.60 MR.PowerHeadRoom.61 MR.PowerHeadRoom.62 MR.PowerHeadRoom.63 '}
    for mr_entity in smr_standard_dict:
        if mr_entity == mr_name:
            smr_standard_list = smr_standard_dict[mr_entity].strip().split(' ')
            smr_list = smr_str.strip().split(' ')
            value_list = value_str.strip().split(' ')
            if len(smr_standard_list) != len(smr_list):
                return False
            if len(smr_list) != len(value_list):
                return False
