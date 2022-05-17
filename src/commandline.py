class CommandLine:
    __action: str = ''

    __name: str = ''

    __token1: str = ''

    __token2: str = ''

    __value: str = ''

    __checksum: str = ''

    __format: str = ''

    __verbose: bool = False

    __list: bool = False

    __key: str = ''

    __valid_actions: [str] = [
        'add',
        'clear',
        'config',
        'delete',
        'get',
        'help',
        'list',
        'version',
        'view'
    ]

    @property
    def action(self) -> str:
        return self.__action

    @action.setter
    def action(self, value: str):
        self.__action = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def token1(self) -> str:
        return self.__token1

    @token1.setter
    def token1(self, value: str):
        self.__token1 = value

    @property
    def token2(self) -> str:
        return self.__token2

    @token2.setter
    def token2(self, value: str):
        self.__token2 = value

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = value

    @property
    def checksum(self) -> str:
        return self.__checksum

    @checksum.setter
    def checksum(self, value: str):
        self.__checksum = value

    @property
    def format(self) -> str:
        return self.__format

    @format.setter
    def format(self, value: str):
        self.__format = value

    @property
    def verbose(self) -> bool:
        return self.__verbose

    @verbose.setter
    def verbose(self, value: bool):
        self.__verbose = value

    @property
    def list(self) -> bool:
        return self.__list

    @list.setter
    def list(self, value: bool):
        self.__list = value

    @property
    def key(self) -> str:
        return self.__key

    @key.setter
    def key(self, value: str):
        self.__key = value

    def is_valid_action(self, action: str) -> bool:
        return action in self.__valid_actions

    def __init__(self, args: [str]):
        self.__parse(args)

    def __parse(self, args: [str]):
        if len(args) == 0:
            return

        if self.is_valid_action(args[0]):
            # Remove the first element from the array.
            self.action = args.pop(0)
        else:
            # Assume it's ./rpass <name>
            self.action = 'get'
            self.name = args.pop(0)

        while len(args) > 0:
            current_arg = args.pop(0)

            # First check if there is an argument AFTER the argument that begins with "--".
            if current_arg[:2] == '--' and len(args) == 0:
                # These are the switches.
                if current_arg not in ['--verbose', '--list']:
                    raise Exception('Argument {0} has no value set'.format(current_arg))

            # And now continue with everything else.
            if current_arg == '--name':
                self.name = args.pop(0)
            elif current_arg == '--token1':
                self.token1 = args.pop(0)
            elif current_arg == '--token2':
                self.token2 = args.pop(0)
            elif current_arg == '--value':
                self.value = args.pop(0)
            elif current_arg == '--checksum':
                self.checksum = args.pop(0)
            elif current_arg == '--key':
                self.key = args.pop(0)
            elif current_arg == '--format':
                self.format = args.pop(0)
            elif current_arg == '--verbose':
                self.verbose = True
            elif current_arg == '--list':
                self.list = True
            else:
                raise Exception('Unknown argument: {0}'.format(current_arg))

    def validate(self):
        if self.action == 'add':
            if len(self.name) == 0:
                raise Exception('--name not specified')
            elif len(self.token1) == 0:
                raise Exception('--token1 not specified')
            elif len(self.token2) == 0:
                raise Exception('--token2 not specified')
            elif len(self.key) == 0:
                raise Exception('--key not specified')
        elif self.action == 'config':
            if not self.list:
                if len(self.name) == 0:
                    raise Exception('--name not specified')
        elif self.action in ['delete', 'view']:
            if len(self.name) == 0:
                raise Exception('--name not specified')
        elif self.action == 'get':
            #
            # Can be:
            # --name NAME
            # --token1 AAA --token2 BBB
            if len(self.name) == 0:
                if len(self.token1) == 0 and len(self.token2) == 0:
                    raise Exception('Please specify either the name or the 2 tokens')

                if len(self.token1) == 0 or len(self.token2) == 0:
                    raise Exception('Please specify both tokens')
        elif self.action in ['clear', 'list']:
            # Nothing to do here.
            pass
