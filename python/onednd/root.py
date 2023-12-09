import PySimpleGUI as sg
from typing import Dict, List, Tuple, Any, Callable

from model import Model, View

class Root(Model):
  def __init__(self) -> None:
    super().__init__('/', {
    })

class RootView(View):
  def __init__(self) -> None:
    super().__init__('/', {
    })

  def handler(self, event, values) -> None:
    """Update self._model, and call self._model.notify()"""
    super().andler(event, values)

  def layout(self) -> List[List[Any]]:
    return [
      [sg.Text('Root')]
    ]

  def update(self, model:Model) -> None:
    """Self view update out of rules be done in ConcreteView class."""
    pass
