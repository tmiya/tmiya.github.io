import PySimpleGUI as sg
from typing import Dict, List, Tuple, Any, Callable, Self

from model import Model, View

class Levels(Model):
  def __init__(self) -> None:
    super().__init__('/levels/', {})
    self._progress:List[str] = []
    self._choices = ['Bard', 'Ranger']

class LevelsView(View):
  def __init__(self) -> None:
    super().__init__('/levels/', {})
    self._rules_disabled = {
      '/levels/add': (lambda m: len(m._progress)>=20),
      '/levels/remove': (lambda m: len(m._progress)<=0)
    }
    self._rules_update = {
      '/levels/progress': 
      (lambda m: "\n".join([f"Lv {i+1}: {s}" for i,s in enumerate(m._progress)]))
    }

  def handler(self, event:str, values:Dict[str,Any]) -> None:
    match event:
      case '/levels/add':
        if len(values['/levels/choice'])==1 and len(self._model._progress)<20:
          self._model._progress.append(values['/levels/choice'][0])
        else:
          print(f"ERROR: {self}.handler({event},{values})")
      case '/levels/remove':
        if len(self._model._progress)>0:
          self._model._progress.pop()
        else:
          print(f"ERROR: {self}.handler({event},{values})")
      case _:
        print(f"ERROR: {self}.handler({event},{values})")
    super().handler(event, values)

  def layout(self) -> List[List[Any]]:
    return [
      [ sg.Text('Levels', font=self._h1()) ],
      [
        sg.Text('Current Level:', font=self._bold()),
        sg.Multiline(size=(20,20), key='/levels/progress'),
        sg.Button('Remove Level', key='/levels/remove',
                  disabled=(len(self._model._progress)==0)
                  )
      ],
      [
        sg.Listbox(self._model._choices, 
                   size=(10, len(self._model._choices)), 
                   key="/levels/choice"),
        sg.Button('Add Level', key='/levels/add',
                  disabled=(len(self._model._progress)==20)),
      ],
    ]
  
  def update(self, model:Model) -> None:
    super().update(model)

