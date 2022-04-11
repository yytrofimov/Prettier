import pprint


class Printer:
    @classmethod
    def repr(cls, obj):
        if isinstance(obj, dict):
            return cls.repr_dict(dict)
        return pprint.pformat(obj)

    @classmethod
    def get_dict_lines(cls, obj, indent='\t'):
        lines = []
        for index, (key, value) in enumerate(obj.items()):
            line_prefix = f"{pprint.pformat(key, compact=True)}: "
            buffer = []
            if isinstance(value, dict):
                dict_lines = cls.get_dict_lines(value, indent)
                buffer.append(line_prefix + dict_lines[0])
                buffer.extend(cls.get_indented_lines(dict_lines[1:], len(line_prefix) * ' '))
            else:
                value_lines = pprint.pformat(value, compact=True).split('\n')
                value_lines = cls.get_indented_lines(value_lines, len(line_prefix) * ' ',
                                                     skip_first=True)
                value_lines[0] = line_prefix + value_lines[0]
                buffer.extend(value_lines)
            if index != len(obj) - 1 and len(buffer) == 1:
                buffer[-1] = buffer[-1] + ','
            lines.extend(buffer)
        if lines:
            lines[0] = '{' + lines[0]
            lines[-1] = lines[-1] + '}'
            for index in range(1, len(lines)):
                lines[index] = ' ' + lines[index]
        else:
            return ['{}']
        return lines

    @classmethod
    def join_lines(cls, lines):
        return '\n'.join(lines)

    @classmethod
    def repr_dict(cls, obj):
        return cls.join_lines(cls.get_dict_lines(obj))

    @classmethod
    def get_indented_string(cls, obj, indent='\t', indents=1, skip_first=False):
        lines = cls.get_indented_lines(obj.split('\n'), indent, indents, skip_first)
        return cls.join_lines(lines)

    @classmethod
    def get_indented_lines(cls, lines, indent='\t', indents=1, skip_first=False):
        lines = [_ for _ in lines]
        for index in range(len(lines)) if skip_first is False else range(1, len(lines)):
            lines[index] = indent * indents + lines[index]
        return lines


class EndpointPrintMixin:
    _PRINT_MIXIN_ENDPOINT = None

    def __repr__(self):
        out = {}
        if self._PRINT_MIXIN_ENDPOINT is None:
            endpoint = '__dict__'
        else:
            endpoint = self._PRINT_MIXIN_ENDPOINT
        if not hasattr(self, endpoint):
            return pprint.pformat(out)
        attrs = getattr(self, endpoint)
        for attr in attrs:
            if not hasattr(self, attr):
                continue
            out[attr] = getattr(self, attr)
        return Printer.repr_dict(out)


class PrintMixin:
    def __repr__(self):
        return Printer.repr_dict(self.__dict__)


class DefaultPrintMixin:
    def __repr__(self):
        return pprint.pformat(self.__dict__)
