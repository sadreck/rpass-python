import os
import subprocess
from typing import Union


class PGP:
    __gpg_path: str = ''

    def __init__(self, gpg_path):
        if not os.path.isfile(gpg_path):
            raise Exception("GPG Path does not exist: {0}".format(gpg_path))
        elif not os.access(gpg_path, os.X_OK):
            raise Exception("GPG file is not executable: {0}".format(gpg_path))

        self.__gpg_path = gpg_path

    def decrypt(self, data: str, key: str) -> Union[None, str]:
        input = "{0}".format(data).encode()
        command = [
            self.__gpg_path,
            '--decrypt',
            '--quiet',
            '-r {0}'.format(key)
        ]
        output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, input=input)
        if int(output.returncode) != 0:
            return None
        return output.stdout.decode()
