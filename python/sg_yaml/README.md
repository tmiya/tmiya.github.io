# `sg_yaml`

Simple `PySimpleGUI` wrapper to construct widgets from YAML file.

## Design rule

Each widget elements are described in YAML as follows. Keys and values are parameters of the widgets constructor.

```yaml
Widget:
  key1: value1
  key2: value2
```

For Widget classnames and their parameters, see https://docs.pysimplegui.com/en/latest/call_reference/tkinter/ .

### handling Tuples

Default way is using PyYaml tuple tag as follows:

```yaml
Text:
  _: 'sample text'
  font: !!python/tuple ['Arial', 24, 'bold']
```

For frequently used keys (`font`, `size`), list are automatically converted to tuple, so following notation is available:

```yaml
Text:
  _: 'sample text'
  font: ['Arial', 24, 'bold']
```

## Widget Elements

Most of widgets are generated dynamically by classnames, so I have not tested all of widgets.

### Parameters Shortnames

Some frequently used parameter names can be shortened as `_`:

* `Button`: `_` as `button_text`
* `Checkbox`, `Text`: `_` as `text`
* `Combo`, `Listbox`: `_` as `values`
* `Input`, `Multiline`: `_` as `default_text`
* `pin`: `_` as `elem`

### `pin`

`elem` parameter requires one widget `Element`. See https://docs.pysimplegui.com/en/latest/call_reference/tkinter/elements/layout_helpers/ .

### `Pane`

`pane_list` parameter requires list of `Column` widgets. See https://docs.pysimplegui.com/en/latest/call_reference/tkinter/elements/pane/ .

### `Window`, `Column`, `Frame`

`layout` parameter requires list of list of `Element`. See each documents.  Also `sample.yml` shows how to write `layout` parameter for `Window` widgets.


## Example: `sample.yml`

Sample for define `Window` widget.

```yaml
title: My new window
layout:
  - - Text:
        _: This is a very basic PySimpleGUI layout
  - - Input:
  - - Button:
        button_text: Button
    - Button:
        _: Exit
```

To create `Window` widget, do as follows:

```python
from sg_yaml import SgYaml

d = None
with open('sample.yml') as yml:
  d = SgYaml.load_yaml(yml)
window = SgYaml.to_window(d)
```

