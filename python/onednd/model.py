import PySimpleGUI as sg

class Model():
  def __init__(self, key):
    self.key = key
    self.view = None # view
    self.children = dict() # children models dict[str, Model]
    self.to_disabled = dict()
    #self.to_visible = {f"{self.key}/error": (lambda x: x._error())}
    #self.to_update = {f"{self.key}/error": (lambda x: x._error_msg())}
    self.to_visible = dict()
    self.to_update = dict()
  
  def __str__(self):
    return f"{self.__class__}({self.children})"

  def handler(self, event, values):
    print(f"{self.__class__}.handler({event}, {values})")
    for child in self.children.values():
      child.handler(event, values)
    
  def update(self, window):
    print(f"{self.__class__}.update()")
    for child in self.children.values():
      child.update(window)
    self.view.update(window)

  def _error(self):
    return False

  def _error_msg(self):
    return ''

class View():
  def __init__(self, key):
    self.key = key
    self.children = dict() # children dict[str, View]
    self.model = None # model
    self.label = ('', ('Arial', 28)) # (label, font)

  def content(self):
    return []
  
  def layout(self):
    layout = [
      [sg.Text(self.label[0], font=self.label[1])],
    #  [sg.Text('Error:', size=(50,5), font=('Arial'), text_color='#F00', 
    #         visible=False, key=f"{self.key}/error")]
    ]
    layout.extend(self.content())
    return layout
  
  def handler(self, window, event, values):
    print(f"{self.__class__}.handler(event={event}, values={values})")
    self.model.handler(event, values)
    #self.update(window)
      
  def update(self, window):
    print(f"{self.__class__}.update()")
    print(self.model.to_update)
    for key,func in self.model.to_update.items():
      window[key].update(func(self.model))
    for key,func in self.model.to_disabled.items():
      window[key].update(disabled=func(self.model))
    for key,func in self.model.to_visible.items():
      window[key].update(visible=func(self.model))
    for child in self.children.values():
      child.update(window)
  
  def _f(self):
    return ('Arial', 12)

  def _bold(self):
    return ('Arial', 12, 'bold')