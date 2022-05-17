import os
import json
from typing import Union


class Config:
    __config_file: str = ''

    __data: dict = {}

    __valid_options = [
        'storage',
        'hostname',
        'port',
        'https',
        'method',
        'verifySSL',
        'sendHostname',
        'gpgPath'
    ]

    def all(self):
        return self.__data

    def __init__(self, config_file: str):
        self.__config_file = config_file
        self.__data = self.__load(self.__config_file)

    def is_valid_option(self, name: str) -> bool:
        return name in self.__valid_options

    def __load(self, config_file: str) -> dict:
        if not os.path.isfile(config_file):
            return {}
        elif not os.access(config_file, os.R_OK):
            raise Exception("Config file {0} is not readable".format(config_file))
        elif not os.access(config_file, os.W_OK):
            raise Exception("Config file {0} is not writable".format(config_file))

        with open(config_file) as f:
            data = json.load(f)

        return data if data else {}

    def get(self, name: str, default: Union[str, bool, int, float] = None) -> Union[str, bool, int, float, None]:
        return self.__data[name] if name in self.__data else default

    def set(self, name: str, value: Union[str, bool, int, float, None]) -> bool:
        if not self.is_valid_option(name):
            raise Exception("Invalid option: {0}".format(name))

        if value.lower() in ['true', 'yes']:
            value = True
        elif value.lower() in ['false', 'no']:
            value = False
        elif isinstance(value, str) and value.isnumeric():
            f = float(value)
            i = int(f)
            value = i if i == f else f

        self.__data[name] = value
        with open(self.__config_file, 'w+') as f:
            f.write(json.dumps(self.__data))
        return True
