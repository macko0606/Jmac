import PySimpleGUI as sg 
def areYouSure(title,text):
    page = [
            [sg.Text(text)],
            [sg.HSeparator()],
            [sg.Button("YES",size=(10,1),border_width = 10, enable_events = True,key="-YES-"),sg.Button("NO",size=(10,1),border_width = 10,enable_events=True,key="-NO-")]
    ]
    window = sg.Window(title,page)
    while True:
        event, values = window.read() 
        if event == "-YES-":
            return True
        elif event == "-NO-":
            return False
        else:
            return False
    window.close()
areYouSure("","")