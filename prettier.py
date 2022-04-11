import pprint


class Printer:
    @classmethod
    def print(cls, obj) -> None:
        print(cls.repr(obj))

    @classmethod
    def handle_endpoint(cls, obj, endpoint: str) -> dict:
        if isinstance(obj, dict):
            return cls.handle_dict_endpoint(obj, endpoint)
        out = {}
        if not hasattr(obj, endpoint):
            return {}
        attrs = getattr(obj, endpoint)
        for attr in attrs:
            if not hasattr(obj, attr):
                continue
            out[attr] = getattr(obj, attr)
        return out

    @classmethod
    def handle_dict_endpoint(cls, obj: dict, endpoint: str) -> dict:
        out = {}
        if endpoint not in obj:
            return {}
        attrs = obj[endpoint]
        if not any(isinstance(attrs, _) for _ in (list, tuple, set)):
            return {}
        for attr in attrs:
            if attr not in obj:
                continue
            out[attr] = obj[attr]
        return out

    @classmethod
    def repr(cls, obj) -> str:
        if isinstance(obj, dict):
            return cls.repr_dict(obj)
        return pprint.pformat(obj)

    @classmethod
    def get_dict_lines(cls, obj, indent: str = '', pp: bool = True) -> list:
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
                    if not isinstance(value, dict):
                        value_lines = pprint.pformat(value, compact=True).split('\n')
                    else:
                        value_lines = cls.get_dict_lines(value)
                else:
                    if not isinstance(value, dict):
                        value_lines = str(value).split('\n')
                    else:
                        value_lines = cls.get_dict_lines(value)
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
    def join_lines(cls, lines: list) -> str:
        return '\n'.join(lines)

    @classmethod
    def repr_dict(cls, obj, indent: str = '', pp: bool = True) -> str:
        return cls.join_lines(cls.get_dict_lines(obj, indent, pp))

    @classmethod
    def get_indented_string(cls, obj, indent: str = '', indents: int = 1, skip_first: bool = False) -> str:
        lines = cls.get_indented_lines(obj.split('\n'), indent, indents, skip_first)
        return cls.join_lines(lines)

    @classmethod
    def get_indented_lines(cls, lines, indent: str = '', indents: int = 1, skip_first: bool = False) -> list:
        lines = [_ for _ in lines]
        for index in range(len(lines)) if skip_first is False else range(1, len(lines)):
            lines[index] = indent * indents + lines[index]
        return lines


class PPrintMixin:
    def __repr__(self):
        return Printer.repr_dict(self.__dict__)


class PrintMixin:
    def __repr__(self):
        return pprint.pformat(self.__dict__)


class MixinFactory:
    def __new__(cls, indent: str = '', pp: bool = True, endpoint: str = None, name: str = 'PrintMixin'):
        if endpoint is None:
            return type(name, (), {
                '__repr__': lambda _: Printer.repr_dict(_.__dict__, indent, pp)
            })
        return type(name, (), {
            '__repr__': lambda _: Printer.repr_dict(Printer.handle_endpoint(_, endpoint), indent, pp)
        })
