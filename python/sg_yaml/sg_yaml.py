import yaml
import PySimpleGUI as sg
from typing import Any, Dict, List, Tuple

class SgYaml():
  """Build PySimpleGUI widget from YAML definition

  For widget parameters, see https://docs.pysimplegui.com/en/latest/call_reference/tkinter/ .
  
  For usage, see README.md .
  """

  # Dict for key=widget_classname, value=named_parameters
  _shortname = {  'Button':'button_text',
              'Checkbox':'text', 'Text':'text',
              'Combo':'values', 'Listbox':'values',
              'Input':'default_text', 'Multiline':'default_text',
              'pin':'elem'
            }

  @staticmethod
  def load_yaml(doc: str) -> Any:
    """load YAML from string

    args:
      doc(str): YAML string
    returns:
      object written in YAML
    """
    return yaml.load(doc, Loader=yaml.FullLoader)
  
  @staticmethod
  def _to_element(d:Dict[str,Any]) -> sg.Element:
    """translate dict to widget

    args:
      d(dict): key=widget classname, value=parameters for widget (usually dict)
    returns:
      widget
    """
    if len(d) != 1:
      raise ValueError(f'#keys in {list(d.keys())}.')
    for k,v in d.items():
      for s in ['font', 'size']:
        if (v is not None) and (s in v.keys()):
          if isinstance(v[s], list):
            v[s] = tuple(v[s])
      if (k in SgYaml._shortname) and (v is not None) and ('_' in v):
        v[SgYaml._shortname[k]] = v.pop('_')
      match k:
        case 'pin':
          return SgYaml._to_pin(v)
        case 'Pane':
          return SgYaml._to_pane(v)
        case 'Window' | 'Column' | 'Frame':
          return SgYaml._to_widget_with_layout(k, v)
        case _:
          return SgYaml._to_widget(k, v)

  @staticmethod
  def to_window(d: Dict[str,Any]) -> sg.Window:
    """translate dict to sg.Window

    args:
      d(dict)
    returns:
      Window widget
    """
    return SgYaml._to_widget_with_layout('Window', d)

  @staticmethod
  def _to_pin(d: dict) -> sg.Column:
    elem = SgYaml._to_element(d.pop('elem'))
    return sg.pin(elem, **d)

  @staticmethod
  def _to_widget(cname:str, d: dict) -> sg.Element:
    cls = getattr(sg, cname)
    if d is not None:
      return cls(**d)
    else:
      return cls()

  @staticmethod
  def _to_widget_with_layout(cname:str, d: dict) -> sg.Element:
    d_layout = d.pop('layout')
    d['layout'] = SgYaml.to_layout(d_layout)
    cls = getattr(sg, cname)
    return cls(**d)

  @staticmethod
  def to_layout(l: List[List[Dict[str,Any]]]) -> List[List[sg.Element]]:
    r = [[SgYaml._to_element(e) for e in row] for row in l]
    return r

  @staticmethod
  def _to_pane(d: dict) -> sg.Pane:
    d_panes = d.pop('pane_list')
    d['pane_list'] = [SgYaml._to_element(column) for column in d_panes]
    return sg.Pane(**d)

  @staticmethod
  def to_output(d: dict, default:Dict[str, Dict[str, Any]]=None) -> sg.Output:
    dct = SgYaml._dict_rewrite(d, 'Output', {}, default)
    return sg.Output(**dct)







  
