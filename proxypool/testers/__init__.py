import pkgutil
from .base import BaseTester
import importlib
from importlib import util
import inspect


# load classes subclass of BaseCrawler
classes = []
for module_info in pkgutil.walk_packages(__path__):
    name = module_info.name
    module_spec = util.find_spec(name)
    if module_spec is None:
        continue
    module = importlib.import_module(name)
    for name, value in inspect.getmembers(module):
        globals()[name] = value
        if inspect.isclass(value) and issubclass(value, BaseTester) and value is not BaseTester \
                and not getattr(value, 'ignore', False):
            classes.append(value)
__all__ = __ALL__ = classes