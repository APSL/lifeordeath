from importlib import import_module


def load_backend(path):
    module, func = path.rsplit('.', 1)
    module = import_module(module)
    return getattr(module, func)
