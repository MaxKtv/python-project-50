from json import loads
from yaml import safe_load
from typing import Dict, Any


EXTENSIONS = {
    'json': loads,
    'yaml': safe_load,
    'yml': safe_load
}


def parse_data(data, ext: str) -> Dict[str, Any]:
    if ext in EXTENSIONS:
        data = EXTENSIONS[ext](data)
        return data
    else:
        extensions = ', '.join(EXTENSIONS.keys())
        raise KeyError(f'Unsupported extension: "{ext}"'
                       f' Supported extensions are:'
                       f' >>> {extensions}')
