import pprint


class Printer:
    @classmethod
    def repr(cls, obj):
        if isinstance(obj, dict):
            return cls.repr_dict(dict)
        return pprint.pformat(obj)

    @classmethod
    def get_dict_lines(cls, obj, indent='', pp=True):
        lines = []
        for index, (key, value) in enumerate(obj.items()):
            buffer = []
            if pp is True:
                line_prefix = f"{pprint.pformat(key, compact=True)}: "
            else:
                line_prefix = f"{str(key)}: "
            line_prefix_lines = line_prefix.split('\n')
            buffer.extend(line_prefix_lines)
            if isinstance(value, dict):
                dict_lines = cls.get_dict_lines(value, indent, pp)
                buffer.append(buffer.pop() + dict_lines[0])
                buffer.extend(cls.get_indented_lines(dict_lines[1:], len(line_prefix_lines[-1]) * ' '))
            else:
                if pp is True:
                    value_lines = pprint.pformat(value, compact=True).split('\n')
                else:
                    value_lines = str(value).split('\n')
                value_lines = cls.get_indented_lines(value_lines, len(line_prefix) * ' ',
                                                     skip_first=True)
                value_lines[0] = buffer.pop() + value_lines[0]
                buffer.extend(value_lines)
            if index != len(obj) - 1:
                buffer[-1] = buffer[-1] + ','
            lines.extend(buffer)
        if lines:
            for index in range(len(lines)):
                lines[index] = indent + lines[index]
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
    def repr_dict(cls, obj, indent='', pp=True):
        return cls.join_lines(cls.get_dict_lines(obj, indent, pp))

    @classmethod
    def get_indented_string(cls, obj, indent='', indents=1, skip_first=False):
        lines = cls.get_indented_lines(obj.split('\n'), indent, indents, skip_first)
        return cls.join_lines(lines)

    @classmethod
    def get_indented_lines(cls, lines, indent='', indents=1, skip_first=False):
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


class PPrintMixin:
    def __repr__(self):
        return Printer.repr_dict(self.__dict__)


class PrintMixin:
    def __repr__(self):
        return pprint.pformat(self.__dict__)


class MixinFactory:
    def __new__(cls, indent='', pp=True, name='PrinMixin'):
        return type(name, (), {
            '__repr__': lambda _: Printer.repr_dict(_.__dict__, indent, pp)
        })
