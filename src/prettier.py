import inspect


class NoSuchEndpoint(Exception):
    pass


class InvalidEndpoint(Exception):
    pass


class NoSuchAttribute(Exception):
    pass


class Printer:
    @classmethod
    def get_endpoint_attrs(cls, obj, endpoint: str, raises: bool = False) -> tuple:
        if isinstance(obj, dict):
            return cls.get_dict_endpoint_attrs(obj, endpoint, raises)
        if not hasattr(obj, endpoint):
            if raises is True:
                raise NoSuchEndpoint
            return ()
        attrs = getattr(obj, endpoint)
        if not any(isinstance(attrs, _) for _ in (set, tuple, list)):
            if raises is True:
                raise InvalidEndpoint
            return ()
        return attrs

    @classmethod
    def get_dict_endpoint_attrs(cls, obj: dict, endpoint: str, raises: bool = False) -> tuple:
        if endpoint not in obj:
            if raises is True:
                raise NoSuchEndpoint
            return ()
        attrs = obj[endpoint]
        if not any(isinstance(attrs, _) for _ in (list, tuple, set)):
            if raises is True:
                raise InvalidEndpoint
            return ()
        return attrs

    @classmethod
    def str(cls, obj, indent: str = '', attrs: tuple = (), raises: bool = False) -> str:
        if isinstance(obj, dict):
            return cls.str_dict(obj, indent, attrs, raises)
        out = {}
        for attr in attrs:
            if not hasattr(obj, attr):
                if raises is True:
                    raise NoSuchAttribute
                else:
                    continue
            out[attr] = getattr(obj, attr)
        return cls.str_dict(out, indent)

    @classmethod
    def str_dict(cls, obj, indent: str = '', attrs: tuple = (), raises: bool = False) -> str:
        out = {}
        if not attrs:
            attrs = tuple(obj.keys())
        for attr in attrs:
            if attr not in obj:
                if raises is True:
                    raise NoSuchAttribute
                else:
                    continue
            out[attr] = obj[attr]
        return cls.join_lines(cls.get_dict_lines(out, indent))

    @classmethod
    def get_dict_lines(cls, obj, indent: str = '') -> list:
        lines = []
        for index, (key, value) in enumerate(obj.items()):
            buffer = []
            line_prefix_lines = f"'{str(key)}': ".split('\n')
            line_prefix_lines = cls.get_indented_lines(line_prefix_lines, ' ', skip_first=True)
            line_prefix_lines = cls.get_indented_lines(line_prefix_lines, (len(line_prefix_lines[0]) - 1) * ' ',
                                                       skip_first=True)
            buffer.extend(line_prefix_lines)
            if isinstance(value, dict):
                value_lines = cls.get_dict_lines(value, indent)
            elif isinstance(value, str):
                value_lines = f"'{str(value)}'".split('\n')
                value_lines = cls.get_indented_lines(value_lines, len(value_lines[0]) * ' ', skip_first=True)
            else:
                value_lines = str(value).split('\n')
            value_lines = cls.get_indented_lines(value_lines, len(line_prefix_lines[-1]) * ' ',
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
    def get_indented_string(cls, obj, indent: str = '', indents: int = 1, skip_first: bool = False) -> str:
        lines = cls.get_indented_lines(obj.split('\n'), indent, indents, skip_first)
        return cls.join_lines(lines)

    @classmethod
    def get_indented_lines(cls, lines, indent: str = '', indents: int = 1, skip_first: bool = False) -> list:
        lines = [_ for _ in lines]
        for index in range(len(lines)) if skip_first is False else range(1, len(lines)):
            lines[index] = indent * indents + lines[index]
        return lines

    @classmethod
    def get_dict_or_slots_attrs(cls, obj, raises):
        if hasattr(obj, '__dict__'):
            return tuple(obj.__dict__)
        elif hasattr(obj, '__slots__'):
            return tuple(obj.__slots__)
        elif raises is True:
            raise NoSuchEndpoint
        return tuple()

    @classmethod
    def shortify(cls, obj, limit=80):
        out = []
        if len(obj) < limit:
            return obj
        for _ in range(0, len(obj), limit):
            out.append(obj[_:_ + limit])
        return '\n'.join(out)

    @classmethod
    def filter_attrs(cls, obj, attrs, key):
        return tuple(attr for attr in attrs if key(getattr(obj, attr)))

    @classmethod
    def get_attrs(cls, obj):
        return tuple(_[0] for _ in inspect.getmembers(obj))

    @classmethod
    def get_added_attrs(cls, obj):
        return tuple(set(cls.get_attrs(obj)) - set(cls.get_attrs(object())) - {'__weakref__', '__module__', '__dict__'})


class MixinFactory:
    def __new__(cls, indent: str = '', attrs: tuple = (), endpoint: str = None,
                dict_or_slots_only: bool = False, methods_and_funcs: bool = False, raises: bool = False,
                name: str = 'PrintMixin'):
        return type(name, (), {
            '__str__': lambda _: Printer.str(_, indent,
                                             cls.get_attrs(_, attrs, endpoint, dict_or_slots_only, methods_and_funcs,
                                                           raises), raises)
        })

    @classmethod
    def get_attrs(cls, obj, attrs: tuple = (), endpoint: str = None, dict_or_slots_only: bool = False,
                  methods_and_funcs: bool = False, raises: bool = False):
        if endpoint is not None:
            attrs = Printer.get_endpoint_attrs(obj, endpoint, raises)
        elif dict_or_slots_only is True:
            attrs = Printer.get_dict_or_slots_attrs(obj, raises)
        elif attrs:
            attrs = attrs
        else:
            attrs = Printer.get_added_attrs(obj)
        if methods_and_funcs is False:
            attrs = Printer.filter_attrs(obj, attrs, lambda _: not (inspect.ismethod(_) or inspect.isfunction(_)))
        return attrs


PPrintMixin = MixinFactory()
