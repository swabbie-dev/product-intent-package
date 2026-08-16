"""Safe YAML 1.2 helpers for Product Intent Package files."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml
from yaml.composer import ComposerError
from yaml.events import AliasEvent
from yaml.nodes import MappingNode


class _Yaml12SafeLoader(yaml.SafeLoader):
    """Safe loader with strict, human-readable package semantics."""

    yaml_implicit_resolvers = {
        key: [item for item in resolvers if item[0] not in {
            "tag:yaml.org,2002:bool",
            "tag:yaml.org,2002:timestamp",
        }]
        for key, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
    }

    def compose_node(self, parent: Any, index: Any) -> Any:
        if self.check_event(AliasEvent):
            event = self.peek_event()
            raise ComposerError(
                None,
                None,
                "YAML aliases are not allowed",
                event.start_mark,
            )
        return super().compose_node(parent, index)

    def construct_mapping(self, node: MappingNode, deep: bool = False) -> dict[Any, Any]:
        if not isinstance(node, MappingNode):
            raise yaml.constructor.ConstructorError(
                None,
                None,
                f"expected a mapping node, found {node.id}",
                node.start_mark,
            )
        self.flatten_mapping(node)
        mapping: dict[Any, Any] = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str):
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    "mapping keys must be strings",
                    key_node.start_mark,
                )
            if key in mapping:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    f"found duplicate key ({key!r})",
                    key_node.start_mark,
                )
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


class _ReadableSafeDumper(yaml.SafeDumper):
    """Indent sequences so direct file reading stays clear."""

    def increase_indent(self, flow: bool = False, indentless: bool = False) -> Any:
        return super().increase_indent(flow, indentless=False)


_Yaml12SafeLoader.add_implicit_resolver(
    "tag:yaml.org,2002:bool",
    re.compile(r"^(?:true|True|TRUE|false|False|FALSE)$"),
    list("tTfF"),
)


def load_yaml(path: Path) -> Any:
    """Load one package YAML file with safe, strict semantics."""

    with path.open(encoding="utf-8") as stream:
        value = yaml.load(stream, Loader=_Yaml12SafeLoader)
    if not isinstance(value, dict):
        raise yaml.YAMLError("YAML document root must be a mapping")
    return value


def dump_yaml(value: Any) -> str:
    """Serialize one package value as readable YAML."""

    return yaml.dump(
        value,
        Dumper=_ReadableSafeDumper,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    )


def write_yaml(path: Path, value: Any) -> None:
    """Write one package value as readable YAML."""

    path.write_text(dump_yaml(value), encoding="utf-8")
