import PySimpleGUI as sg

from model import Model, View
from levels import Levels, LevelsView

class Root(Model):
  def __init__(self):
    super().__init__("/")
    self.children = {
      '/level': Levels()
    }

class RootView(View):
  def __init__(self):
    super().__init__("/")
    self.children = {
      '/level': LevelsView()
    }

  def layout(self):
    print(self.children)
    tabs = [
      sg.Tab("Level", self.children['/level'].layout(), key="/level"),
    ]
    return [[sg.TabGroup([tabs])]]
