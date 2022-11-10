import PySimpleGUI as pg
import os

import constants
from guiLayout import homeLayout, createVolumeLayout, openVolumeLayout, volumeLayout
from utilities import isNumber
from Volume import Volume as Vol

class MyFileSystem:
    # Khai báo các màn hình
    __homeWindow = None
    __createWindow = None
    __openWindow = None
    __volumeWindow = None

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
            if event == "Create new Volume":
                self.__homeWindow.Hide()
                self.__createVolume()
                break
            
            if event == "Open Volume":
                self.__homeWindow.Hide()
                self.__openVolume()
                break

    # Màn hình create Volume
    def __createVolume(self):
        if self.__createWindow == None:
            self.__createWindow = pg.Window("Create new Volume", createVolumeLayout, finalize=True)
        else:
            self.__createWindow.UnHide()

        while True:
            event, values = self.__createWindow.read()
            if event == pg.WIN_CLOSED:
                break
            if event == "Back":
                self.__createWindow.Hide()
                self.__homeWindow.UnHide()
                self.start()
                break
            if event == "Create":
                name = values['_name_']
                password = values['_pass_']
                confirmPass = values['_confirm_']
                sc = int(values['_sc_'])
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
                vol = Vol(password=password, name=name, sc=sc, size=float(size))
                vol.create()
                self.__createWindow.Hide()
                self.__workWithVolume(vol, name)
                break
    
    # Màn hình open Volume
    def __openVolume(self):
        if self.__openWindow == None:
            self.__openWindow = pg.Window("Open Volume", openVolumeLayout, finalize=True)
        else:
            self.__openWindow.UnHide()

        while True:
            event, values = self.__openWindow.read()
            if event == pg.WIN_CLOSED:
                break
            if event == "Back":
                self.__openWindow.Hide()
                self.__homeWindow.UnHide()
                self.start()
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
                    self.__openWindow.hide()
                    self.__workWithVolume(vol, filepath)
                    break
                except:
                    self.__openWindow['_wrong_'].update(visible = True)
                    continue
                self.__openWindow['_wrong_'].update(visible = False)

    # Màn hình giao diện chính
    def __workWithVolume(self, vol: Vol, volPath: str):
        volPath = os.path.abspath(volPath)
        volName = os.path.splitext(volPath)[0].split('/')[-1]
        if self.__volumeWindow == None:
            self.__volumeWindow = pg.Window(volPath, volumeLayout, finalize=True)
        else:
            self.__volumeWindow.UnHide()
        self.__volumeWindow['_name_'].update(f'Volume: {volName}')

        while True:
            event, values = self.__volumeWindow.read()
            if event in (pg.WIN_CLOSED, 'Exit'):
                break
            if event == 'Import':
                print('import file: test')
                vol.importFile('test')
