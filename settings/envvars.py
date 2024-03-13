import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def load_envars(BASE_DIR):
    try:
        yaml_file=open("./.envvars.yaml", "r")        
    except:
        yaml_file=open(str(BASE_DIR.parent) + "/.envvars.yaml", "r")
        
    return yaml.load(yaml_file, Loader=Loader)
