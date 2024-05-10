import os


def get_root_dir():
    return os.path.dirname(os.path.abspath(__file__))

def join_to_root_dir(*args):
    return os.path.join(get_root_dir(), *args)