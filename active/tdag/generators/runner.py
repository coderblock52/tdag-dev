# generators/runner.py
from generators.registry import get_generator, list_generators

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