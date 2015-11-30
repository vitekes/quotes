import pytest
from yaml import load
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


xfail = pytest.mark.xfail


class ConfigManager(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConfigManager, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def config_load(self, filename):
        if filename:
            stream = file(filename, 'r')
            utf8_dict = load(stream=stream, Loader=Loader)
            utf8_dict = self.convert(utf8_dict)
            return utf8_dict
        else:
            return pytest.xfail("can not read config")

    def convert(self, input):
        if isinstance(input, dict):
            return {self.convert(key): self.convert(value) for key, value in input.iteritems()}
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input