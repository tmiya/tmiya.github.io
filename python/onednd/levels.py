import PySimpleGUI as sg
from typing import Dict, List, Tuple, Any, Callable, Self

from model import Model, View
from classes import Classes

class Levels(Model):
  _choices:List[str] = [c._name for c in Classes._list]

  def __init__(self) -> None:
    super().__init__('/levels/', {})
    self._progress:List[str] = []

  def is_multiclassed(self) -> bool:
    return len(set(self._progress)) > 1
  
  def satisfy_primal_ability(self) -> bool:
    return True

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
    m = self._model
    match event:
      case '/levels/add':
        if len(values['/levels/choice'])==1 and len(m._progress)<20:
          m._progress.append(values['/levels/choice'][0])
          if m.is_multiclassed():
            if not m.satisfy_primal_ability():
              m._progress.pop()
        else:
          print(f"ERROR: {self}.handler({event},{values})")
      case '/levels/remove':
        if len(m._progress)>0:
          m._progress.pop()
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
                   size=(10, len(Levels._choices)), 
                   key="/levels/choice"),
        sg.Button('Add Level', key='/levels/add',
                  disabled=(len(self._model._progress)==20)),
      ],
    ]
  
  def update(self, model:Model) -> None:
    super().update(model)

