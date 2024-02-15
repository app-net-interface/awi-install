from typing import List

import yaml


def _replace_placeholders(file_content, vars):
    if isinstance(file_content, dict):
        return {k: _replace_placeholders(v, vars) for k, v in file_content.items()}
    elif isinstance(file_content, list):
        return [_replace_placeholders(element, vars) for element in file_content]
    elif isinstance(file_content, str):
        return file_content.format(**vars)
    else:
        return file_content 


def render_from_yaml(filename, vars) -> List:
    """
    Returns a list of rendered documents from a given yaml file.

    Loads all documents from a single file and scans them looking
    for placeholders and replaces them with provided variables.
    As a result, a list of documents is created, which is later
    returned.
    """
    with open(filename) as f:
        data = f.read()
    documents = list(yaml.safe_load_all(data))
    print(documents)
    return [yaml.dump(_replace_placeholders(d, vars)) for d in documents]
