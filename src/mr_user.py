
import mr_global as gl
import mr_utils as uts
import mr_test as mt
import io
import os

def linux_initial():
    gl.IS_LINUX = 1
    gl.file_split_code = '/'
    gl.TEST_PATH = gl.TEST_PATH.replace("\\", gl.file_split_code)
    gl.MR_TEST_PATH = gl.MR_TEST_PATH.replace("\\", gl.file_split_code)
    gl.PM_TEST_PATH = gl.PM_TEST_PATH.replace("\\", gl.file_split_code)
    gl.SOURCE_PATH = gl.SOURCE_PATH.replace("\\", gl.file_split_code)
    gl.OUTPUT_PATH = gl.OUTPUT_PATH.replace("\\", gl.file_split_code)
    gl.OUT_PATH = gl.OUT_PATH.replace("\\", gl.file_split_code)

def mr_test_process():
    # read conf.xml, store information in TEST_CONF,MR_CONF,PM_CONF etd.
    uts.conf_xml_parse()
    # get mr file information in MR_DICT
    uts.MR_xml_init()
    # get pm file information in PM_DICT
    uts.PM_xml_init()
    # write in output data.txt head
    uts.mr_out_file_data_head()


    # -------------------------------------------------------------------
    # MR test function
    # -------------------------------------------------------------------
    uts.mr_function_process(mt.test51_file_integrity, 'test_51')
    uts.mr_function_process(mt.test52_file_integrity, 'test_52')
    uts.mr_function_process(mt.test53_file_integrity, 'test_53')
    uts.mr_function_process(mt.test54_file_integrity, 'test_54')
    uts.mr_function_process(mt.test55_file_integrity, 'test_55')
    uts.mr_function_process(mt.test56_file_integrity, 'test_56')
    uts.mr_function_process(mt.test57_file_integrity, 'test_57')
    uts.mr_function_process(mt.test58_file_integrity, 'test_58')
    uts.mr_function_process(mt.test59_file_integrity, 'test_59')
    uts.mr_function_process(mt.test61_file_accuracy,  'test_61')
    uts.mr_function_process(mt.test62_file_accuracy,  'test_62')
    uts.mr_function_process(mt.test63_file_accuracy,  'test_63')
    uts.mr_function_process(mt.test71_file_accuracy,  'test_71')
    uts.mr_function_process(mt.test72_file_accuracy,  'test_72')
    uts.mr_function_process(mt.test73_file_accuracy,  'test_73')
    
    
    # -------------------------------------------------------------------
    #TODO: when other test function can put here: 
    # if use mr_function_process, don't forget add function_name in TEST_CONF  both at mr_global.py and conf.xml
    # -------------------------------------------------------------------
    
    
    
    # write the output information
    uts.write_output_file_text()
    



    
        