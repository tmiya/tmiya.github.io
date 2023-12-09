import PySimpleGUI as sg

from root import Root, RootView
from model import matching_model_and_view

def main():
  root, root_view = matching_model_and_view(Root(), RootView())
  sg.theme('BlueMono')
  window = sg.Window('One D&D Character Builder', 
                      root_view.layout()).Finalize()
  root.set_root(root)
  root_view.set_window(window)
  window.Maximize()

  print(f"{root}['/']={root['/']}")
  print(f"{root}['/levels/']={root['/levels/']}")
  print(f"{root}['/abilities/']={root['/abilities/']}")
  lv = root._children['/levels/']
  print(f"{lv}['/']={lv['/']}")
  print(f"{lv}['/levels/']={lv['/levels/']}")
  print(f"{lv}['/abilities/']={lv['/abilities/']}")
  ab = root._children['/abilities/']
  print(f"{ab}['/']={ab['/']}")
  print(f"{ab}['/levels/']={ab['/levels/']}")
  print(f"{ab}['/abilities/']={ab['/abilities/']}")

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