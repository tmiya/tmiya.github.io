import PySimpleGUI as sg
from typing import Dict, List, Tuple, Any, Callable

from model import Model, View
from levels import Levels, LevelsView
from abilities import Abilities, AbilitiesView

class Root(Model):
  def __init__(self) -> None:
    super().__init__('/', {
      '/levels/': Levels(),
      '/abilities/': Abilities()
    })

class RootView(View):
  def __init__(self) -> None:
    super().__init__('/', {
      '/levels/': LevelsView(),
      '/abilities/': AbilitiesView()
    })

  def handler(self, event:str, values:Dict[str,Any]) -> None:
    """Update self._model, and call self._model.notify()"""
    super().handler(event, values)

  def layout(self) -> List[List[Any]]:
    tabs = [
      sg.Tab("Abilities", self._children['/abilities/'].layout(), 
             key="/abilities/"),
      sg.Tab("Levels", self._children['/levels/'].layout(), 
             key="/levels/"),
    ]
    return [[sg.TabGroup([tabs])]]

  def update(self, model:Model) -> None:
    """Self view update out of rules be done in ConcreteView class."""
    pass
