from abc import ABC, abstractmethod
import PySimpleGUI as sg
from typing import Dict, List, Tuple, Any, Callable, Self

from model import Model, View

  
class Clazz(ABC):
  def __init__(self, name:str, primary_ability:List[str]) -> None:
    self._name = name
    self._primary_ability = primary_ability
    pass

class Bard(Clazz):
  def __init__(self) -> None:
    super().__init__(name='Bard', primary_ability=['Cha'])

class Ranger(Clazz):
  def __init__(self) -> None:
    super().__init__(name='Ranger', primary_ability=['Dex', 'Wis'])


class Classes():
  _list:List[Clazz] = [Bard(), Ranger()]

  @staticmethod
  def by_name(name:str) -> Clazz:
    for c in Classes._list:
      if name == c._name:
        return c
    raise KeyError(name)
