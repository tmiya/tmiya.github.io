import PySimpleGUI as sg
from typing import Dict, List, Tuple, Any, Callable, Self

from model import Model, View

class Attributes(Model):
  _attr_names:List[str] = ['Str', 'Dex', 'Con', 'Int', 'Wis', 'Cha']
  _point_use:Dict[int, int] = {
      8:0, 9:1, 10:2, 11:3, 12:4, 13:5, 14:7, 15:9
  }

  def __init__(self) -> None:
    super().__init__('/attributes/', {})
    self._attributes:Dict[str,int] = {
      'Str':8, 'Dex':8, 'Con':8, 'Int':8, 'Wis':8, 'Cha':8
    }
    self._points_left:int = 27

  def points_used(self, attrs:Dict[str,int]) -> int:
    pt = 0
    for v in attrs.values():
      pt += Attributes._point_use[v]
    return pt
  
  def disabled(self, attr:str, op:str) -> bool:
    if (op not in ['+', '-']) or (attr not in Attributes._attr_names):
      raise ValueError(f"attr={attr}, op={op}")
    attrs = self._attributes.copy()
    attrs[attr] += (1 if op=='+' else -1)
    for v in attrs.values():
      if (v < 8) or (15 < v):
        return True
    return self.points_used(attrs)>27

class AttributesView(View):
  def __init__(self) -> None:
    super().__init__('/attributes/', {})
    for s in Attributes._attr_names:
      self._rules_update[f"/attributes/{s}/value"] = \
        (lambda m, s=s: str(m._attributes[s]))
    self._rules_update['/attributes/points_left'] = \
      (lambda m: str(27-m.points_used(m._attributes)))
    self._rules_disabled = dict()
    for attr in Attributes._attr_names:
      for op in ['+', '-']:
        self._rules_disabled[f"/attributes/{attr}/{op}"] = \
          (lambda m, attr=attr, op=op: m.disabled(attr, op))

  def handler(self, event:str, values:Dict[str,Any]) -> None:
    ss = event[1:].split('/')
    if len(ss) != 3:
      print(f"ERROR: {self}.handler({event},{values})")
    else:
      match ss:
        case 'attributes', attr, op:
          if (attr not in Attributes._attr_names) or (op not in ['+', '-']):
            print(f"ERROR: {self}.handler({event},{values})")
          else:
            self._model._attributes[attr] += (1 if op=='+' else -1)
            self._model.points_left = 27 - self._model.points_used(self._model._attributes)
        case _:
          print(f"ERROR: {self}.handler({event},{values})")
    super().handler(event, values)

  def layout(self) -> List[List[Any]]:
    ret = [
      [ sg.Text('Attributes', font=self._h1()) ],
      [
        sg.Text('Points Left:', font=self._bold()),
        sg.Text('27', key='/attributes/points_left'),
      ]
    ]
    ret.extend([
      [
        sg.Text(s, size=(5, 1), font=self._bold()),
        sg.Text('8', size=(3, 1), font=('Arial', 12), key=f"/attributes/{s}/value"),
        sg.Button('+', key=f"/attributes/{s}/+",
                  disabled=(self._model.disabled(s, '+'))),
        sg.Button('-', key=f"/attributes/{s}/-",
                  disabled=(self._model.disabled(s, '-'))),
      ]
      for s in ['Str', 'Dex', 'Con', 'Int', 'Wis', 'Cha']
    ])
    return ret
  
  def update(self, model:Model) -> None:
    super().update(model)

