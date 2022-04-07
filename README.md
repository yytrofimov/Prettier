# Prettier

If you are trying to output nested data structures, each of which is individually displayed as a dictionary representation, the nesting levels are not separated, such an output is difficult to perceive.
```
class DefaultPrintMixin:
    def __repr__(self):
        return pprint.pformat(self.__dict__)


class A(DefaultPrintMixin):
    def __init__(self):
        self.attrs = ('b', 'c', 'd')
        self.b = 20
        self.c = 30
        self.d = B()


class B(DefaultPrintMixin):
    def __init__(self):
        self.attrs = ('b', 'aba \n caba', 'd')
        self.b = 'aba \n caba'
        setattr(self, 'aba \n caba', 2000)
        self.d = C()


class C(DefaultPrintMixin):
    def __init__(self):
        self.a = 'aba \n caba'
        self.b = 2000
        self.c = 3000
```
You can expect the following output:
```
{'attrs': ('b', 'c', 'd'),
 'b': 20,
 'c': 30,
 'd': {'aba \n caba': 2000,
 'attrs': ('b', 'aba \n caba', 'd'),
 'b': 'aba \n caba',
 'd': {'a': 'aba \n caba', 'b': 2000, 'c': 3000}}}
```
But if you use a ```PrintMixin``` instead of the standard one, then you can expect the following output:
```
{'attrs': ('b', 'c', 'd'),
 'b': 20,
 'c': 30,
 'd': {'attrs': ('b', 'aba \n caba', 'd'),
       'b': 'aba \n caba',
       'aba \n caba': 2000,
       'd': {'a': 'aba \n caba',
             'b': 2000,
             'c': 3000}}}
```
It is also possible to use ```EndpointPrintMixin```. As an endpoint, specify the name of the attribute, the contents of the list of attributes to display.
```
_PRINT_MIXIN_ENDPOINT = 'attrs'
```
You can expect the following output:
```
{'b': 20,
 'c': 30,
 'd': {'b': 'aba \n caba',
       'aba \n caba': 2000,
       'd': {}}}
```
