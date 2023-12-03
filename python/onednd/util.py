def model_and_view(model, view):
  print(f"model_and_view({model}, {view})")
  view.model = model
  model.view = view
  for k in set(model.children.keys()) & set(view.children.keys()):
    print(f"model_and_view: k={k}")
    model.children[k].view = view.children[k].model
    view.children[k].model = model.children[k].view
    model_and_view(model.children[k], view.children[k])
  return (model, view)