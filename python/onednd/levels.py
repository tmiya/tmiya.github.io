import PySimpleGUI as sg

from model import Model, View
from clazz import Bard, Ranger

class Levels(Model):
  def __init__(self):
    super().__init__("/level")
    self.classes = []
    self.to_disabled |= {
      '/level/remove': (lambda x: len(x.classes)==0),
      '/level/add': (lambda x: len(x.classes)==20),
    }
    self.to_update |= {
      '/level/progress':
       (lambda x: "\n".join([f"Lv {i+1}: {c.name}" for i,c 
                             in enumerate(x.classes)])),
    }
  
  def handler(self, event, values):
    print("Levels.handler")
    match event:
      case '/level/add':
        print(f"/level/add: {self.classes}")
        self.classes.extend(
          [c for c in self.choice() if c.name == values['/level/choice'][0]]
        )
        print(f"/level/add: {self.classes}")
      case '/level/remove':
        self.classes.pop()
      case _:
        print(f"ERROR: event={event}, values={values}")
  
  def level_to_go(self):
    return len(self.classes)+1
  
  def choice(self):
    return [
      Bard(atLv=self.level_to_go()),
      Ranger(atLv=self.level_to_go())
    ]

class LevelsView(View):
  def __init__(self):
    super().__init__("/level")
    self.label = ('Level', ('Arial', 28)) # (label, font)
    self.key = '/level'

  def content(self):
    return [
      [
        sg.Text('Current Level:', font=self._bold()),
        sg.Multiline(size=(20,20), key='/level/progress'),
        sg.Button('Remove Level', key='/level/remove',
                  disabled=(len(self.model.classes)==0)
                  )
      ],
      [
        sg.Listbox([c.name for c in self.model.choice()], 
                   size=(10, len(self.model.choice())), 
                   key="/level/choice"),
        sg.Button('Add Level', key='/level/add',
                  disabled=(len(self.model.classes)==20)),
      ],
    ]