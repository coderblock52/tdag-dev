# generators/runner.py
############ generator imports ############
# Add imports for all generators here
from generators.bloodline_generator import generate_bloodline
from generators.cultivation_technique_generator import generate_cultivation_technique
from generators.cultivation_technique_name_generator import generate_technique_name
from generators.cultivator_generator import generate_cultivator
from generators.demon_beast_generator import generate_demon_beast
from generators.element_generator import generate_element
from generators.soul_color_generator import generate_soul_color
from generators.soul_force_generator import generate_soul_force
from generators.soul_form_generator import generate_soul_form
from generators.soul_generator import generate_soul
from generators.soul_rank_generator import generate_soul_rank

# import pkgutil
# import importlib
# import generators

# # Auto-import all submodules of generators
# package_path = generators.__path__
# for finder, name, ispkg in pkgutil.iter_modules(package_path):
#     importlib.import_module(f"generators.{name}")

from .registry import list_generators, get_generator

def generate(name: str, *args, **kwargs):
    """
    Lookup the right generator by name and call it.
    """
    fn = get_generator(name)
    return fn(*args, **kwargs)

def generate_all(ctx=None):
    results = {}
    for name in list_generators():
        results[name] = generate(name, ctx=ctx)
    return results