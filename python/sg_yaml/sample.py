import PySimpleGUI as sg

from sg_yaml import SgYaml

sg.theme('Dark Amber')  # Let's set our own color theme

d = None
with open('sample.yml') as yml:
  d = SgYaml.load_yaml(yml)
window = SgYaml.to_window(d)

while True:
    event, values = window.read()   # Read the event that happened and the values dictionary
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':     # If user closed window with X or if user clicked "Exit" button then exit
      break
    if event == 'Button':
      print('You pressed the button')
window.close()
