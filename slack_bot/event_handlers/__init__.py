import importlib
import os
import glob
import re


for module in glob.glob(f"{os.path.dirname(__file__)}/**/*.py", recursive=True):
  path = re.sub(r".+(?=slack_bot)|\.py", "", module)

  path_parts = re.split(r"\\|\/", path)
  if path_parts[-1] == '__init__':
    continue

  module_name = '.'.join(path_parts)
  importlib.import_module(module_name)

  print(f"Event listener <{module_name}> imported!")
