from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Any, Callable, Self

class Subject(ABC):
  def notify(self) -> None:
    raise NotImplementedError

class Observable(ABC):
  def update(self) -> None:
    raise NotImplementedError
  

class Model(Subject):
  def __init__(self, key:str, children:List[Self]) -> None:
    super(Model, self).__init__()
    self._key: str = key
    self._view: View = None
    self._children: Dict[str,Self] = dict()

  def __str__(self):
    return f"{self.__class__}(\'{self._key}\', {list(self._children.keys())})"

  def notify(self) -> None:
    self._view.update(self)
    for o in self._children:
      o.update(self)


class View(Observable):
  def __init__(self, key:str, children:Dict[str,Self]) -> None:
    super(View, self).__init__()
    self._key: str = key
    self._model: Model = None
    self._window: Any = None
    self._children: Dict[str,Self] = children
    self.rules_disabled: Dict[str, Callable[[Model], bool]] = dict()
    self.rules_visible: Dict[str, Callable[[Model], bool]] = dict()
    self.rules_update: Dict[str, Callable[[Model], Any]] = dict()

  def __str__(self):
    return f"{self.__class__}(\'{self._key}\', {list(self._children.keys())})"

  def set_window(self, window:Any) -> None:
    """Set self._window"""
    self._window = window
    for v in self._children:
      v.set_window(window)

  def handler(self, event, values) -> None:
    """Update self._model, and call self._model.notify()"""
    self._model.notify()

  def layout(self) -> List[List[Any]]:
    raise NotImplementedError

  def update(self, model:Model) -> None:
    """Self view update out of rules be done in ConcreteView class."""
    for key,func in self._rules_update.items():
      self._window[key].update(func(self._model))
    for key,func in self._rules_disabled.items():
      self._window[key].update(disabled=func(self._model))
    for key,func in self._rules_visible.items():
      self._window[key].update(visible=func(self._model))
    for v in self._children:
      v.update(model)


def matching_model_and_view(model:Model, view:View):
  """couples models and views recursively"""
  print(f"matching_model_and_view({model}, {view})")
  view._model = model
  model._view = view
  for k in set(model._children.keys()) & set(view._children.keys()):
    matching_model_and_view(model._children[k], view._children[k])
  return (model, view)
