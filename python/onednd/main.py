import PySimpleGUI as sg

from root import Root, RootView
import util

def main():
  root, root_view = util.model_and_view(Root(), RootView())
  #del root.to_update['//error']
  sg.theme('BlueMono')
  window = sg.Window('One D&D Character Builder', 
                      root_view.layout()).Finalize()
  window.Maximize()

  while True:
    event, values = window.read()
    print(f"main loop: event={event}, values={values}")
    match event:
      case sg.WIN_CLOSED:
        break
      case _:
        print(f"dispatch({event}, {values})")
        root_view.handler(window, event, values)
    root.update(window)
    print(root)

if __name__ == '__main__':
  main()