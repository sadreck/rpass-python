import hashlib
import base64
import json
from xml.etree.ElementTree import XML, fromstring
from typing import Union


class PasswordValidator:
    def validate(self, password: dict, data: str, format: str) -> Union[None, str]:
        if len(password['checksum']) == 0:
            return data

        if format == 'raw' or format == '':
            if hashlib.sha256(data.encode()).hexdigest() == password['checksum']:
                return data
        elif format == 'base64':
            if hashlib.sha256(base64.b64decode(data)).hexdigest() == password['checksum']:
                return base64.b64decode(data).decode()
        elif format == 'json':
            try:
                json_data = json.loads(data)
                if 'password' in json_data:
                    if hashlib.sha256(json_data['password'].encode()).hexdigest() == password['checksum']:
                        return json_data['password']
            except Exception as e:
                # Something went wrong, treat as invalid.
                pass
        elif format == 'xml':
            try:
                tree = fromstring(data)
                element = tree.find('password')
                if element is not None:
                    # Line breaks can be a bit weird, so check with both versions.
                    text = element.text
                    if hashlib.sha256(text.encode()).hexdigest() == password['checksum']:
                        return text
                    if "\r\n" in text:
                        text = text.replace("\r\n", "\n")
                    else:
                        text = text.replace("\n", "\r\n")

                    if hashlib.sha256(text.encode()).hexdigest() == password['checksum']:
                        return text

            except Exception as e:
                # Something went wrong, treat as invalid.
                pass

        # Invalid.
        return None
