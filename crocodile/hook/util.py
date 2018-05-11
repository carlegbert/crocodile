import yaml


def load_hooks(yaml_path):
    with open(yaml_path) as f:
        document = f.read()
    hook_list = yaml.load(document, Loader=yaml.Loader)
    return hook_list
