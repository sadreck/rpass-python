import os
import json
from typing import Union


class PasswordStorage:
    __password_file: str = None

    __data: dict = {}

    def __init__(self, password_file: str):
        self.__password_file = password_file
        self.__data = self.__load(self.__password_file)

    def __load(self, password_file: str):
        if not os.path.isfile(password_file):
            return {}
        elif not os.access(password_file, os.R_OK):
            raise Exception("Password storage file {0} is not readable".format(password_file))
        elif not os.access(password_file, os.W_OK):
            raise Exception("Password storage file {0} is not writable".format(password_file))

        with open(password_file) as f:
            data = json.load(f)

        return data if data else {}

    def add(self, name: str, token1: str, token2: str, checksum: str, key: str) -> bool:
        self.__data[name] = {
            'name': name,
            'token1': token1,
            'token2': token2,
            'checksum': checksum,
            'key': key
        }
        return self.__save()

    def all(self):
        return self.__data

    def get_by_name(self, name: str) -> Union[dict, None]:
        return self.__data[name] if name in self.__data else None

    def getByTokens(self, token1: str, token2: str) -> Union[dict, None]:
        for name, password in self.__data.items():
            if password['token1'] == token1 and password['token2'] == token2:
                return password
        return None

    def delete(self, name: str) -> bool:
        self.__data.pop(name, None)
        return self.__save()

    def clear(self) -> bool:
        self.__data = {}
        return self.__save()

    def __save(self) -> bool:
        with open(self.__password_file, 'w+') as f:
            f.write(json.dumps(self.__data))
        return True
