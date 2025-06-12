python3 -i -c '
import os, sys
from meta.utils import *
current_dir = os.path.join("c:/", "Users", "stevenb", "Documents", "onering", "repos", "tdag-dev", "active", "tdag")

import_all_modules_from_dir(os.path.join(current_dir, "generators"), globals())
import_all_modules_from_dir(os.path.join(current_dir, "helpers"), globals())
# paths = get_common_paths()
# def hello(): print('Hello, dev!')
'