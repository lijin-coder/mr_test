# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys

import user

import mr_qt
import mr_globel



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('mr test ...')
    app = mr_qt.create_qt_application()
    ui = mr_qt.mr_ui_window()
    # user.mr_test_process()
    mr_qt.exit_qt_application(app.exec_())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
