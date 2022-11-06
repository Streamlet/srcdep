import os, yaml, config.dep_def as dep_def

DEPS_YAML_FILE = 'SRCDEP.yaml'

def load(dir, optional):
    cfg_path = os.path.join(dir, DEPS_YAML_FILE)
    if not os.path.exists(cfg_path):
        if optional:
            return None
        else:
            assert False, 'There must be a file named "%s" in the root directory "%s"' % (DEPS_YAML_FILE, dir)
    with open(cfg_path, 'r') as f:
        content = f.read()
    dict = yaml.safe_load(content)
    return dep_def.dict_to_object(dict)
