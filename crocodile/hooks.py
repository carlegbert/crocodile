import yaml
from os import path


def _load_hooks():
    fpath = path.join(path.dirname(path.dirname(__file__)), 'hooks.yml')
    with open(fpath) as f:
        document = f.read()
    hook_list = yaml.load(document, Loader=yaml.Loader)
    return hook_list

hooks = _load_hooks()
