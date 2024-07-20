from os import path
import os
import re
from typing import TypedDict
from gi.repository import GLib


class ScriptMetadata(TypedDict):
    name: str
    script_name: str
    description: str


def parse_metadata(metadata: str) -> ScriptMetadata:
    """Parse the metadata from a script file."""
    header_regex = re.compile(r"^(#.*\n)+", re.MULTILINE)
    field_regex = re.compile(r"#\s*([a-zA-Z]+):\s*(.*)\n*[^#]", re.MULTILINE)
    header = header_regex.match(metadata).group(0)
    data = {}
    for match in field_regex.finditer(header):
        data[match.group(1).lower()] = match.group(2)
    return data


def get_scripts():
    """Get the list of available scripts."""
    scripts = []
    script_dir = f"{GLib.get_user_config_dir()}/cute_lights/scripts"

    for file in os.listdir(script_dir):
        if file.endswith(".cutie"):
            with open(path.join(script_dir, file)) as f:
                metadata = f.read()
                data = parse_metadata(metadata)
                data["script_name"] = file
                scripts.append(data)

    return scripts
