#!/usr/bin/env python3
"""
Schema Validator Helper for TDAG Simulation

Location: <root_directory>/helpers/schema_validator.py

Provides a simple `validate(obj, schema_path)` function to check
JSON-serializable objects against a JSON Schema file using the
`jsonschema` library.

Usage:
    from helpers.schema_validator import validate
    validate(
        beast_obj,
        'meta/templates/object_schemas/demon_beast_schema.json'
    )

Raises RuntimeError on validation failure.
"""
import json
import os
from jsonschema import validate as jsonschema_validate
from jsonschema.exceptions import ValidationError


def load_json(path: str) -> dict:
    """Load and parse JSON from a file path."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate(obj: dict, schema_path: str) -> None:
    """
    Validate `obj` against the JSON Schema at `schema_path`.
    Raises RuntimeError if the object does not conform.
    """
    # Resolve absolute path for schema
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))
    abs_schema = (
        schema_path
        if os.path.isabs(schema_path)
        else os.path.join(root_dir, schema_path)
    )

    schema = load_json(abs_schema)
    try:
        jsonschema_validate(instance=obj, schema=schema)
    except ValidationError as e:
        # Raise as RuntimeError for simplicity
        raise RuntimeError(f"Schema validation failed for {abs_schema}: {e.message}")
