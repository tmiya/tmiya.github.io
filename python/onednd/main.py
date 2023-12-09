import PySimpleGUI as sg

from root import Root, RootView
from model import matching_model_and_view

def main():
  root, root_view = matching_model_and_view(Root(), RootView())
  sg.theme('BlueMono')
  window = sg.Window('One D&D Character Builder', 
                      root_view.layout()).Finalize()
  root_view.set_window(window)
  window.Maximize()

  while True:
    event, values = window.read()
    print(f"main loop: event={event}, values={values}")
    match event:
      case sg.WIN_CLOSED:
        break
      case _:
        print(f"dispatch({event}, {values})")
        root_view.handler(event, values)
    root.notify()
    #print(root)

if __name__ == '__main__':
  main()