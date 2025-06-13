# generators/registry.py
from typing import Callable

_generators: dict[str, Callable] = {}

def register(name: str):
    """
    Decorator to register a generator function under `name`.
    """
    def decorator(fn: Callable) -> Callable:
        _generators[name] = fn
        return fn
    return decorator

def get_generator(name: str) -> Callable:
    return _generators[name]

def list_generators() -> list[str]:
    return list(_generators.keys())