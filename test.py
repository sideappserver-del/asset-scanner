import PySimpleGUI as sg

# Set theme
sg.theme('Dark')

# Create window
window = sg.Window('?? Asset Scanner - Test', [
    [sg.Text('Welcome to Asset Scanner!', font=('Arial', 14))],
    [sg.Text('If you see this, Python is working! ?')],
    [sg.Button('Close')]
])

# Run
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Close':
        break

window.close()