import PySimpleGUI as sg

from view import View

class CharView(View):
  def __init__(self):
    self.super().__init__()
    sg.theme('BlueMono')
    self.window = sg.Window('One D&D Character Builder', 
                            self.layout()).Finalize()
    self.window.Maximize()

  def layout(self):
    layout = []

