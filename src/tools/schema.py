"""
Event schema objects.

Loads a JSON schema (dict / YAML|JSON string / Path), validates it against the
Jupyter Events metaschema, and provides a validator for incoming event payloads.
"""
from __future__ import annotations

import json
from pathlib import Path, PurePath
from typing import Any, Union, cast

from jsonschema import FormatChecker, validators
from referencing import Registry
from referencing.jsonschema import DRAFT7

try:
    from jsonschema.protocols import Validator
except ImportError:  # pragma: no cover
    Validator = Any  # type: ignore[assignment, misc]

from jupyter_events import yaml
from jupyter_events.validators import draft7_format_checker, validate_schema

class EventSchemaUnrecognized(Exception):
    """Raised when the schema input type is not supported."""


class EventSchemaLoadingError(Exception):
    """Raised when the schema cannot be deserialized into a dict."""


class EventSchemaFileAbsent(Exception):
    """Raised when a schema file path is provided but does not exist."""


SchemaType = Union[dict[str, Any], str, PurePath]


class EventSchema:
    """A validated schema used to validate event payloads.

    Parameters
    ----------
    schema:
        A JSON schema provided as a dict, a YAML/JSON serialized string, or a
        Pathlib object pointing to a .yml/.yaml/.json file.

    validator_class:
        jsonschema validator class used to validate payload instances.

    format_checker:
        jsonschema FormatChecker used by the validator.

    registry:
        Registry for resolving nested JSON schema references ($ref).
    """

    def __init__(
        self,
        schema: SchemaType,
        validator_class: type[Validator] = validators.Draft7Validator,  # type: ignore[assignment]
        format_checker: FormatChecker = draft7_format_checker,
        registry: Registry[Any] | None = None,
    ) -> None:
        loaded = self._load_schema(schema)

        # Validate the schema against Jupyter Events metaschema.
        validate_schema(loaded)

        if registry is None:
            registry = DRAFT7.create_resource(loaded) @ Registry()

        self._schema: dict[str, Any] = loaded
        self._validator = validator_class(  # type: ignore[call-arg]
            loaded,
            registry=registry,
            format_checker=format_checker,
        )

    def __repr__(self) -> str:
        return json.dumps(self._schema, indent=2)

    @staticmethod
    def _is_probably_a_path(s: str) -> bool:
        p = Path(s)
        return p.match("*.yml") or p.match("*.yaml") or p.match("*.json")

    @classmethod
    def _ensure_dict_loaded(cls, loaded: Any, *, was_str: bool) -> dict[str, Any]:
        if isinstance(loaded, dict):
            return cast(dict[str, Any], loaded)

        msg = "Could not deserialize schema into a dictionary."
        if was_str and isinstance(loaded, (str, bytes)) and cls._is_probably_a_path(str(loaded)):
            msg += " Paths to schema files must be explicitly wrapped in a Pathlib object."
        else:
            msg += " Double check the schema and ensure it is in the proper form."
        raise EventSchemaLoadingError(msg)

    @classmethod
    def _load_schema(cls, schema: SchemaType) -> dict[str, Any]:
        """Load a schema from dict / Path / YAML|JSON string into a dict."""

        if isinstance(schema, dict):
            return schema

        if isinstance(schema, PurePath):
            path = Path(schema)
            if not path.exists():
                raise EventSchemaFileAbsent(f'Schema file not present at path "{schema}".')

            loaded = yaml.load(path)
            return cls._ensure_dict_loaded(loaded, was_str=False)

        if isinstance(schema, str):
            loaded = yaml.loads(schema)
            return cls._ensure_dict_loaded(loaded, was_str=True)

        raise EventSchemaUnrecognized(
            f"Expected a dictionary, string, or PurePath, but instead received {schema.__class__.__name__}."
        )
