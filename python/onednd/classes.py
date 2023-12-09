from abc import ABC, abstractmethod
import PySimpleGUI as sg
from typing import Dict, List, Tuple, Any, Callable, Self

from model import Model, View

  
class Clazz(ABC):
  def __init__(self, name:str,
               primary_ability:List[str]) -> None:
    self._name: str = name
    self._primary_ability: List[str] = primary_ability

class Bard(Clazz):
  def __init__(self) -> None:
    super().__init__(name='Bard',
                     primary_ability=['Cha'])

class Ranger(Clazz):
  def __init__(self) -> None:
    super().__init__(name='Ranger',
                     primary_ability=['Dex', 'Wis'])


class Classes():
  _list:List[Clazz] = [Bard(), Ranger()]

  @staticmethod
  def by_name(name:str) -> Clazz:
    for c in Classes._list:
      if name == c._name:
        return c
    raise KeyError(name)
  
  @staticmethod
  def classes_by_primal_ability(abi:str) -> List[str]:
    ret = []
    for c in Classes._list:
      if abi in c._primary_ability:
        ret.append(c._name)
    return ret