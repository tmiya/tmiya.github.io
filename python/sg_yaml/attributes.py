import PySimpleGUI as sg

from sg_yaml import SgYaml

#sg.theme('Dark Amber')  # Let's set our own color theme

attr_names = ["str", "dex", "con", "int", "wis", "cha"]
point_need = {8:0, 9:1, 10:2, 11:3, 12:4, 13:5, 14:7, 15:9}
point_max = 27
attr_value = {k:8 for k in attr_names}
point_used = sum([point_need[attr_value[k]] for k in attr_names])

s = """
title: Attributes
layout:
  - - Text:
        _: Attribute
        size: [6, 1]
    - Text:
        _: Value
        size: [6, 1]
    - Text:
        _: Points
        size: [6, 1]
    - Text:
        _: Up
        size: [4, 1]
    - Text:
        _: Down
        size: [4, 1]
"""

for attr in attr_names:
  s += f"""
  - - Text:
        _: {attr.capitalize()}
        size: [4, 1]
        font: ["Helvetica", 14]
    - Text:
        _: {str(attr_value[attr])}
        size: [7, 1]
        k: attr.{attr}.value
    - Text:
        _: {str(point_need[attr_value[attr]])}
        size: [6, 1]
        k: attr.{attr}.point
    - Button:
        _: "+"
        size: [3, 1]
        k: attr.{attr}.plus
        disabled: false
    - Button:
        _: "-"
        size: [3, 1]
        k: attr.{attr}.minus
        disabled: true
  """

s += f"""
  - - Text:
        _: "Total point:"
    - Text:
        _: "{point_used}/{point_max}"
        k: attr.total.point
    - Button:
        _: "Finish"
        disabled: true
        k: attr.finish
"""

d = SgYaml.load_yaml(s)
window, rules = SgYaml.to_window(d)
for k,v in rules.widgets.items():
   print((k, v))

while True:
    event, values = window.read()   # Read the event that happened and the values dictionary
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':     # If user closed window with X or if user clicked "Exit" button then exit
      break
    if event == 'attr.finish':
      break
    if event.startswith('attr.'):
      es = event.split('.')
      attr, sign = es[1], es[2]
      match sign:
        case "plus":
          if attr_value[attr] < 15:
            attr_value[attr] += 1
        case "minus":
          if attr_value[attr] > 8:
            attr_value[attr] -= 1
        case _:
          print(f"unknown event: {event}")
      for attr in attr_names:
        rules.widgets[f"attr.{attr}.value"].update(value=str(attr_value[attr]))
        rules.widgets[f"attr.{attr}.point"].update(value=str(point_need[attr_value[attr]]))
        rules.widgets[f"attr.{attr}.plus"].update(disabled=(attr_value[attr] == 15))
        rules.widgets[f"attr.{attr}.minus"].update(disabled=(attr_value[attr] == 8))
      total = sum([point_need[attr_value[k]] for k in attr_names])
      rules.widgets['attr.total.point'].update(value=f"{total}/{point_max}")
      rules.widgets['attr.finish'].update(disabled=(not total == point_max))
    if event == 'Button':
      print('You pressed the button')
window.close()