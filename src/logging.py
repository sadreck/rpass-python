import os
import numpy


class Logging:
    quiet: bool = False

    is_verbose: bool = False

    @staticmethod
    def write(message: str, eol: bool):
        if Logging.quiet:
            return

        if message is None:
            message = ''
        print(message, end=(None if eol else ''))

    @staticmethod
    def error(message: str, eol: bool = True):
        Logging.write(message, eol)

    @staticmethod
    def info(message: str, eol: bool = True):
        Logging.write(message, eol)

    @staticmethod
    def verbose(message: str, eol: bool = True):
        if Logging.is_verbose is False:
            return
        Logging.write(message, eol)

    @staticmethod
    def table(data: [str], padding: int = 1, separator: str = '|'):
        if len(data) == 0:
            Logging.info("Dataset is empty")
            return

        # First calculate the longest values for each column.
        widths = Logging.get_column_widths(data)

        # Create format.
        format = Logging.generate_print_format(widths, padding, separator)

        # Show table.
        dotted_row = ''
        for i, item in enumerate(data):
            line = format.format(*item)
            if i == 0:
                # This is the header, add a line.
                dotted_row = separator + ('-' * (len(line) - 2)) + separator
                Logging.info(dotted_row)
            Logging.info(line)
            if i == 0:
                Logging.info(dotted_row)
        Logging.info(dotted_row)

    @staticmethod
    def get_column_widths(data: [str]) -> [int]:
        widths = numpy.full(len(data[0]), 0)
        for item in data:
            for i, value in enumerate(item):
                item = [str(s) for s in item]
                if len(str(value)) > widths[i]:
                    widths[i] = len(str(value))

        return widths

    @staticmethod
    def generate_print_format(widths: [int], padding: int, separator: str) -> str:
        format = []
        for i, width in enumerate(widths):
            width += padding
            format.append("{:" + str(width) + "}")

        return separator + (separator + ' ').join(format) + separator
