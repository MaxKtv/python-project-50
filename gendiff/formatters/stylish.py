from itertools import chain
from typing import Dict, Any, Tuple, List


REPLACER = ' '
SPACE_COUNT = 4
STYLISH_META = {
    'added': '+ ',
    'original': '  ',
    'removed': '- ',
    'updated': ('- ', '+ '),
    'nested': '  '
}


def get_inborn_indent_count():
    any_stylish_meta = next(iter(STYLISH_META))
    inborn_indent_count = len(STYLISH_META[any_stylish_meta])
    return inborn_indent_count


def format_stylish_diff(node: Any, depth: int = 0) -> str:
    """
    Turns node to "stylish" style string

    Args:
        node (Any): variable to be stringified
        depth (int, optional): Dictionary's level of depth. Defaults to 0.

    Returns:
        str: "stylish" style difference
    """
    if not isinstance(node, dict):
        return normalize_value(node, depth)
    lines = []
    base_indent = get_indents(depth + 1)
    for key, (meta, val) in sorted(node.items()):
        if meta == 'nested':
            formatted_value = format_stylish_diff(val, depth + 1)
            lines.append(f"{base_indent}{STYLISH_META[meta]}{key}: "
                         f"{formatted_value}")
        elif meta == 'updated':
            old_val, new_val = val
            old_meta, new_meta = STYLISH_META[meta]
            lines.append(f"{base_indent}{old_meta}{key}: "
                         f"{normalize_value(old_val, depth + 1)}")
            lines.append(f"{base_indent}{new_meta}{key}: "
                         f"{normalize_value(new_val, depth + 1)}")
        elif meta in {'added', 'removed', "original"}:
            formatted_value = normalize_value(val, depth + 1)
            lines.append(f"{base_indent}{STYLISH_META[meta]}{key}: "
                         f"{formatted_value}")

    result = stringify_stylish_lines(lines, depth)
    return result


def normalize_value(obj: Any, depth: int) -> str:
    """
    Converts object(values) to string

    Args:
        obj (Any): Object to be converted
        depth (int, optional): Dictionary's level of depth

    Returns:
        str: Converted string
    """
    if isinstance(obj, bool):
        return str(obj).lower()
    elif obj is None:
        return 'null'
    elif isinstance(obj, (str | int | float)):
        return str(obj)
    elif isinstance(obj, dict):
        lines = []
        inborn_indent = REPLACER * get_inborn_indent_count()
        for key, val in obj.items():
            formatted_value = normalize_value(val, depth + 1)
            lines.append(f"{get_indents(depth + 1)}{inborn_indent}"
                         f"{key}: {formatted_value}")
        result = stringify_stylish_lines(lines, depth)
        return result


def get_indents(depth: int) -> str:
    """
    Builds indent in accordance with depth

    Args:
        depth (int, optional): Dictionary's level of depth

    Returns:
        str: indent
    """
    inborn_indent = get_inborn_indent_count()
    if depth <= 0:
        return ''
    return REPLACER * (depth * SPACE_COUNT - inborn_indent)


def stringify_stylish_lines(lines: List[str], depth: int) -> str:
    """
    Builds string from lines in stylish style

    Args:
        lines (List[str]): Object to be converted
        depth (int): Dictionary's level of depth

    Returns:
        str: stringified lines in stylish style
    """
    indent = get_indents(depth)
    result = chain('{', lines, [(indent + '}') if len(indent) < 1
                                else (indent + '  ' + '}')])
    return '\n'.join(result)


def get_stylish_diff(diff: Dict[str, Tuple[str, Any]]) -> str:
    """
    Formats diff dictionary to "stylish" style string

    Args:
        diff (Dict[str, Tuple[str, Tuple[str, Any]]): Dictionary of difference

    Returns:
        str: "stylish" styled difference
    """
    return format_stylish_diff(diff)
