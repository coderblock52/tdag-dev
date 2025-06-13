python3 -i -c '
import os, sys
from meta.utils import *
from importlib import reload as r
current_dir = os.path.join("c:/", "Users", "stevenb", "Documents", "onering", "repos", "tdag-dev", "active", "tdag")

import_all_modules_from_dir(os.path.join(current_dir, "generators"), globals())
import_all_modules_from_dir(os.path.join(current_dir, "helpers"), globals())
paths = get_common_paths()
root_dir = paths["root"]
reference_dir = paths["reference"]
validators_dir = paths["validators"]
ctx = GenerationContext()
print("Hello, dev!")
'