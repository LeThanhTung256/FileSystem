import PySimpleGUI as pg

pg.theme('DarkGrey5')

homeLayout = [
    [pg.T("")],
    [pg.Text("My file system", font="Any 30", size=(30, 0), justification="center")],
    [pg.T(size=(0, 3))],
    [pg.T(size=(7, 0), font="Any 30"), pg.Button("Create new Volume", font="Any 22", size=(20, 0))],
    [pg.T(size=(7, 0), font="Any 30"),pg.Button("Open Volume", font="Any 22", size=(20, 0))],
    [pg.T(size=(0, 3))],
    [pg.T(size=(22, 0), font="Any 30"), pg.Button("Exit", font="Any 17", size=(10, 0))],
    [pg.T()],
]

Sc = [1, 2, 3]
createVolumeLayout = [
    [pg.T("")],
    [pg.Text("Create a Volume", font="Any 30", size=(30, 0), justification="center")],
    [pg.T(size=(0, 3))],
    [pg.T(size=(2, 0), font="Any 30"), pg.Text("Name of Volume", font="Any 20", size=(15, 0)), pg.InputText(font="Any 18", size=(20, 0), key="_name_")],
    [pg.T("")],
    [pg.T(size=(2, 0), font="Any 30"), pg.Text("Password", font="Any 20", size=(15, 0)), pg.InputText(password_char="*", font="Any 18", size=(20, 0), key="_pass_")],
    [pg.T("")],
    [pg.T(size=(2, 0), font="Any 30"), pg.Text("Confirm password", font="Any 20", size=(15, 0)), pg.InputText(password_char="*", font="Any 18", size=(20, 0), key="_confirm_")],
    [pg.T("")],
    [pg.Text("Confirm password not match with password", font="Any 18", text_color="red", size=(50, 0), justification="center", visible=False, key='_not_match_')],
    [pg.T(size=(2, 0), font="Any 30"), pg.Text("Sectors per cluster", font="Any 20", size=(15, 0)), pg.OptionMenu(values=Sc, default_value=Sc[0], key="_sc_")],
    [pg.T("")],
    [pg.T(size=(2, 0), font="Any 30"), pg.Text("Size of Volume", font="Any 20", size=(15, 0)), pg.InputText(font="Any 18", size=(16, 0), key="_size_"), pg.T("GB", font="Any 20")],
    [pg.Text("Size of Volume must be a float", font="Any 18", text_color="red", size=(50, 0), justification="center", visible=False, key='_must_be_number_')],
    [pg.Text("Please fill in all fields", font="Any 18", text_color="red", size=(50, 0), justification="center", visible=False, key='_fill_in_all_')],
    [pg.T(size=(0, 1))],
    [pg.T(size=(15, 0), font="Any 30"), pg.Button("Create", font="Any 17", size=(10, 0)), pg.Button("Back", font="Any 17", size=(10, 0))],
    [pg.T()],
]

openVolumeLayout = [
    [pg.T("")],
    [pg.Text("Open Volume", font="Any 30", size=(30, 0), justification="center")],
    [pg.T(size=(0, 3))],
    [pg.T(size=(2, 0), font="Any 30"), pg.FileBrowse(button_text="Select Volume", font="Any 18", pad=(0, 0), size=(11, 0), target='_input_'), pg.T(size=(3, 0), font="Any 31"), pg.Input(font="Any 18", size=(20, 0), key="_input_", readonly=True)],
    [pg.T("")],
    [pg.T(size=(2, 0), font="Any 30"), pg.Text("Password", font="Any 20", size=(15, 0)), pg.InputText(password_char="*", font="Any 18", size=(20, 0), key="_pass_")],
    [pg.T("")],
    [pg.Text("Wrong password", font="Any 18", text_color="red", size=(50, 0), justification="center", visible=False, key='_wrong_')],
    [pg.Text("Please fill in all fields", font="Any 18", text_color="red", size=(50, 0), justification="center", visible=False, key='_fill_in_all_')],
    [pg.T(size=(0, 1))],
    [pg.T(size=(13, 0), font="Any 30"), pg.Button("Open", font="Any 17", size=(10, 0)), pg.Button("Back", font="Any 17", size=(10, 0))],
    [pg.T()],
]

volumeLayout = [
    [pg.T("")],
    [pg.Text("", font="Any 30", size=(30, 0), justification="left", key="_name_")],
    [pg.T(size=(0, 3))],
    [pg.T(size=(13, 0), font="Any 30"), pg.Button("Import", font="Any 17", size=(10, 0)), pg.Button("Export", font="Any 17", size=(10, 0))],
    [pg.T()],
    [pg.T(size=(13, 0), font="Any 30"), pg.Button("Back", font="Any 17", size=(10, 0)), pg.Button("Exit", font="Any 17", size=(10, 0))],
    [pg.T()],
]
