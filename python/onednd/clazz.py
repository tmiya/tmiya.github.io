import PySimpleGUI as sg

from model import Model, View

class Clazz(Model):
  def __init__(self, name, atLv):
    super().__init__(f"/{name.lower()}")
    self.name = name
    self.atLv = atLv

class Bard(Clazz):
  def __init__(self, atLv):
    super().__init__("Bard", atLv)

class Ranger(Clazz):
  def __init__(self, atLv):
    super().__init__("Ranger", atLv)

class ClazzView(View):
  def __init__(self, name):
    super().__init__(f"/{name.lower()}")
    pass