import PySimpleGUI as pg

from guiLayout import homeLayout, createVolumnLayout, openVolumnLayout
from utilities import isNumber
from Volumn import Volumn as Vol

class MyFileSystem:
    # Khai báo các màn hình
    __homeWindow = None
    __createWindow = None
    __openWindow = None

    # Khởi tạo chương trình
    def __init__(self):
        self.__homeWindow = pg.Window("MyFS", homeLayout, finalize=True)

    # Màn hình home
    def start(self):
        while True:
            event, values = self.__homeWindow.read()
            if event in ("Exit", pg.WIN_CLOSED):
                self.__homeWindow.Hide()
                break
            if event == "Create new volumn":
                self.__homeWindow.Hide()
                self.__createVolumn()
                break
            
            if event == "Open volumn":
                self.__homeWindow.Hide()
                self.__openVolumn()

    # Màn hình create volumn
    def __createVolumn(self):
        if self.__createWindow == None:
            self.__createWindow = pg.Window("Create new volumn", createVolumnLayout, finalize=True)
        else:
            self.__createWindow.UnHide()

        while True:
            event, values = self.__createWindow.read()
            if event == pg.WIN_CLOSED:
                self.__createWindow.Hide()
                break
            if event == "Back":
                self.__createWindow.Hide()
                self.__homeWindow.UnHide()
                break
            if event == "Create":
                name = values['_name_']
                password = values['_pass_']
                confirmPass = values['_confirm_']
                sc = values['_sc_']
                size = values['_size_']

                if "" in [name, password, confirmPass]:
                    self.__createWindow['_fill_in_all_'].update(visible = True)
                    continue
                self.__createWindow['_fill_in_all_'].update(visible = False)
                if confirmPass != password:
                    self.__createWindow['_not_match_'].update(visible = True)
                    continue
                self.__createWindow['_not_match_'].update(visible = False)
                if not isNumber(size):
                    self.__createWindow['_must_be_number_'].update(visible = True)
                    continue
                self.__createWindow['_must_be_number_'].update(visible = False)

                vol = Vol(password,name, sc, size)
                vol.create()
    
    # Màn hình open volumn
    def __openVolumn(self):
        if self.__openWindow == None:
            self.__openWindow = pg.Window("Open volumn", openVolumnLayout, finalize=True)
        else:
            self.__openWindow.UnHide()

        while True:
            event, values = self.__openWindow.read()
            if event == pg.WIN_CLOSED:
                self.__openWindow.Hide()
                break
            if event == "Back":
                self.__openWindow.Hide()
                self.__homeWindow.UnHide()
                break
            if event == "Open":
                filepath = values['_input_']
                password = values['_pass_']

                if "" in [filepath, password]:
                    self.__openWindow['_fill_in_all_'].update(visible = True)
                    continue
                self.__openWindow['_fill_in_all_'].update(visible = False)
                try:
                    vol = Vol(password=password, filepath=filepath)
                    print(vol)
                except:
                    self.__openWindow['_wrong_'].update(visible = True)
                    continue
                self.__openWindow['_wrong_'].update(visible = False)
                
myFs = MyFileSystem()
myFs.start()
