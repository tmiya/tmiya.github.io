import PySimpleGUI as sg
from typing import Dict, List, Tuple, Any, Callable, Self

from model import Model, View

class Abilities(Model):
  _abi_names:List[str] = ['Str', 'Dex', 'Con', 'Int', 'Wis', 'Cha']
  _point_use:Dict[int, int] = {
      8:0, 9:1, 10:2, 11:3, 12:4, 13:5, 14:7, 15:9
  }
  _point_all:int = 27

  def __init__(self) -> None:
    super().__init__('/abilities/', {})
    self._abilities:Dict[str,int] = {
      'Str':8, 'Dex':8, 'Con':8, 'Int':8, 'Wis':8, 'Cha':8
    }

  def points_used(self, abis:Dict[str,int]) -> int:
    pt = 0
    for v in abis.values():
      pt += Abilities._point_use[v]
    return pt
  
  def points_left(self, abis:Dict[str,int]) -> int:
    return (Abilities._point_all - self.points_used(abis))
  
  def disabled(self, abi:str, op:str) -> bool:
    if (op not in ['+', '-']) or (abi not in Abilities._abi_names):
      raise ValueError(f"abi={abi}, op={op}")
    abis = self._abilities.copy()
    abis[abi] += (1 if op=='+' else -1)
    for v in abis.values():
      if (v < 8) or (15 < v):
        return True
    return self.points_used(abis) > 27

class AbilitiesView(View):
  def __init__(self) -> None:
    super().__init__('/abilities/', {})
    for s in Abilities._abi_names:
      self._rules_update[f"/abilities/{s}"] = \
        (lambda m, s=s: str(m._abilities[s]))
    self._rules_update['/abilities/points_left'] = \
      (lambda m: str(m.points_left(m._abilities)))
    self._rules_disabled = dict()
    for abi in Abilities._abi_names:
      for op in ['+', '-']:
        self._rules_disabled[f"/abilities/{abi}/{op}"] = \
          (lambda m, abi=abi, op=op: m.disabled(abi, op))

  def handler(self, event:str, values:Dict[str,Any]) -> None:
    ss = event[1:].split('/')
    m = self._model
    if len(ss) != 3:
      print(f"ERROR: {self}.handler({event},{values})")
    else:
      match ss:
        case 'abilities', attr, op:
          if (attr not in Abilities._abi_names) or (op not in ['+', '-']):
            print(f"ERROR: {self}.handler({event},{values})")
          else:
            m._abilities[attr] += (1 if op=='+' else -1)
        case _:
          print(f"ERROR: {self}.handler({event},{values})")
    super().handler(event, values)

  def layout(self) -> List[List[Any]]:
    m = self._model
    ret = [
      [ sg.Text('Abilities', font=self._h1()) ],
      [
        sg.Text('Points Left:', font=self._bold()),
        sg.Text('27', key='/abilities/points_left'),
      ]
    ]
    ret.extend([
      [
        sg.Text(s, size=(5, 1), font=self._bold()),
        sg.Text('8', size=(3, 1), font=('Arial', 12), 
                key=f"/abilities/{s}"),
        sg.Button('+', key=f"/abilities/{s}/+",
                  disabled=False),
        sg.Button('-', key=f"/abilities/{s}/-",
                  disabled=True),
      ]
      for s in Abilities._abi_names
    ])
    return ret
  
  def update(self, model:Model) -> None:
    super().update(model)

