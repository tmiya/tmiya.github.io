from model import Model, View
from levels import Levels, LevelsView

class Char(Model):
  def __init__(self):
    self.super().__init__(self, CharView(), [
      Levels(LevelsView()),
    ])

class CharView(View):
  def __init__(self):
    self.super().__init__()
    sg.theme('BlueMono')
    self.window = sg.Window('One D&D Character Builder', 
                            self.layout()).Finalize()
    self.window.Maximize()

  def layout(self):
    tabs = [
      sg.Tab("Race", race_page.RacePage.layout(ctx), key="tab:Race"),
      sg.Tab("Level", level_page.LevelPage.layout(ctx), key="tab:Level")
    ]
  for cl in level_page.LevelPage.list_classes(1):
    tabs.append(
      sg.Tab(cl.name, cl.layout(ctx), key=f"tab:{cl.name}")
    )

  return [[
    sg.TabGroup([tabs])
  ]]


    