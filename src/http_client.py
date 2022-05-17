import platform
import requests
import urllib
from version import __VERSION__
from src.logging import Logging


class HttpClient:
    __hostname: str = 'www.remotepassword.com'

    __secure: bool = True

    __port: int = 443

    __method: str = 'post'

    __verify_host: bool = True

    __error: str = ''

    __send_hostname: bool = False

    __debug = None

    @property
    def debug(self):
        return self.__debug

    @property
    def error(self):
        return self.__error

    @property
    def send_hostname(self):
        return self.__send_hostname

    @send_hostname.setter
    def send_hostname(self, value: bool):
        self.__send_hostname = value

    def __get_user_agent(self) -> str:
        data = [
            platform.system(),
            'RPASS/{0}'.format(__VERSION__),
            'Python/{0}'.format(platform.python_version())
        ]
        if self.send_hostname:
            data.append('Hostname/{0}'.format(platform.node()))
        return '; '.join(data).strip()

    def __init__(self, hostname: str, port: int, https: bool, http_method: str, verify_host: bool):
        self.__hostname = hostname
        self.__port = port
        self.__secure = https
        self.__method = 'get' if http_method.lower() == 'get' else 'post';
        self.__verify_host = verify_host

    def __get_endpoint(self) -> str:
        url = [
            'https://' if self.__secure else 'http://',
            self.__hostname,
            '' if self.__port in [80, 443] else ':{0}'.format(self.__port),
            '/password'
        ]
        return ''.join(url)

    def __request(self, endpoint: str, post_params: dict) -> str:
        session = requests.Session()
        session.verify = self.__verify_host
        session.max_redirects = 3
        session.headers = {
            'User-Agent': self.__get_user_agent()
        }

        if not self.__verify_host:
            # Hide warnings only then verifySSL is set to False intentionally.
            requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

        try:
            response = session.get(endpoint) \
                if len(post_params) == 0 \
                else session.post(endpoint, data=post_params)
        except Exception as e:
            self.__debug = e
            Logging.verbose("Error making password request")
            Logging.verbose(str(e))
            return ''

        if response.status_code != 200:
            Logging.verbose("HTTP Response: {0}".format(response.status_code))

        return response.content.decode()

    def fetch(self, token1: str, token2: str, format: str = 'raw') -> str:
        endpoint = self.__get_endpoint()
        params = {
            'token1': token1,
            'token2': token2,
            'format': 'raw' if format and len(format) == 0 else format
        }

        if self.__method == 'get':
            return self.__request(endpoint + '?' + urllib.parse.urlencode(params), {})
        return self.__request(endpoint, params)
