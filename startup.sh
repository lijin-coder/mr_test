#!/bin/bash

package_file_path="./build/linux/package/"
setup_tool_filename="setuptools-36.6.0.zip"
pip_filename="pip-9.0.1.tar.gz"
pip_package_path="./build/linux/package/pip_src/"
requirement_path="./build/linux/package/requirement.txt"
current_path=$(pwd)

function get_setup_tool() {
    cd $package_file_path
    unzip $setup_tool_filename
    cd setuptools-36.6.0
    python setup.py install
    cd $current_path
}

function get_pip_tool() {
    cd $package_file_path
    tar -zxvf pip-9.0.1.tar.gz
    cd pip-9.0.1
    python setup.py install
    cd $current_path
}

function check_pip() {
    pip --version
    if [ $? != 0 ]
    then 
        read -p "pip Not exist: do you want to install now?(y or n)" choice_user
        if [ "$choice_user" = "n" ]
        then
            echo "now exit the shell..."
            exit 0
        fi

        if [ -e $package_file_path$setup_tool_filename ]
        then
            get_setup_tool
        else
            echo "Fail to install Python Setup-Tool: no such file:" $package_file_path$setup_tool_filename 
        fi

        if [ -e $package_file_path$pip_filename ]
        then
            get_pip_tool
        else
            echo "Fail to install Python Pip-Tool: no such file:" $package_file_path$pip_filename
        fi 

        echo "-------------------------------------"
        pip --version
        if [ $? != 0 ]
        then
            echo "install pip Error!!!"
        else
            echo "install pip Successful!"
            exit -1
        fi
    else
        echo "pip exists"
    fi
    pip install --upgrade pip
}


function get_package() {
    pip install Colorama
    if [ $? != 0 ]
    then
        pip install --no-index --find-links=$pip_package_path -r $requirement_path
    else
        echo 'y' | pip uninstall Colorama
        pip install openpyxl
    fi
}

check_pip
get_package
cd src
python mr_main.py
