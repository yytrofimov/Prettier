# Prettier - properly pprint of nested objects

If you are trying to output nested data structures, each of which is individually displayed as a dictionary
representation, the nesting levels are not separated, such an output is difficult to perceive.

```
class PPrintMixin:
    def __str__(self):
        return str(self.__dict__)


SAMPLE_DICT = {'a': None}
SAMPLE_DICT['a'] = SAMPLE_DICT


class A(PPrintMixin):
    def __init__(self):
        self.attrs = ('a', 'b', 'c')
        self.a = 10
        self.b = B()
        self.c = {'a': 1, 'b': 2, 'c': 3}
        setattr(self, 'd\nd', {'a': 1, 'b': 2, 'c': 3})
        self.e = 'a\na'
        self.f = 'a' * 100
        self.g = self
        self.h = SAMPLE_DICT


class B(PPrintMixin):
    def __init__(self):
        setattr(self, 'a \n a', {'a': 1, 'b': {'a': 1, 'b': 2, 'c': 3}, 'c\nc': C()})
        self.b = [C(), 1]
        self.c = C()


class C(PPrintMixin):
    def __init__(self):
        self.a = ('b', 'c')
        self.b = 'a \n a'
        self.c = {}
```

You can expect the following output:

```
{'attrs': ('a', 'b', 'c'), 'a': 10, 'b': <__main__.B object at 0x1034b74c0>, 'c': {'a': 1, 'b': 2, 'c': 3}, 'd\nd': {'a': 1, 'b': 2, 'c': 3}, 'e': 'a\na', 'f': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'g': <__main__.A object at 0x1033fb3a0>, 'h': {'a': {...}}}
```

But if you use a ```PPrintMixin``` instead of the standard one, then you can expect the following output:

```
{'a': 10,
 'd
   d': {'a': 1,
        'b': 2,
        'c': 3},
 'e': 'a
       a',
 'c': {'a': 1,
       'b': 2,
       'c': 3},
 'h': {'a': <RecursionError on 4304997312>},
 'b': {'a 
           a': {'a': 1,
                'b': {'a': 1,
                      'b': 2,
                      'c': 3},
                'c
                  c': {'a': ('b', 'c'),
                       'c': {},
                       'b': 'a 
                              a'}},
       'c': {'a': ('b', 'c'),
             'c': {},
             'b': 'a 
                    a'},
       'b': [<__main__.C object at 0x100bf3a60>, 1]},
 'attrs': ('a', 'b', 'c'),
 'f': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
       aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
 'g': <RecursionError on 4307498032>}
```

If you want to create an own Mixin, just import MixinFactory. For example, you can use the ```endpoint``` argument. This
is the name of the attribute that stores the list of arguments to
print. Let's combine some Mixins, like this:

```
from prettier import MixinFactory

AttrsPrintMixin = MixinFactory(endpoint='attrs')
APrintMixin = MixinFactory(endpoint='a')


class A(AttrsPrintMixin):
    ...


class B(PrintMixin):
    ...


class C(APrintMixin):
    ...
```

The output will be:

```
{'a': 10,
 'b': {'c': {'b': 'a 
                    a',
             'c': {}},
       'b': [<__main__.C object at 0x100b478b0>, 1],
       'a 
           a': {'a': 1,
                'b': {'a': 1,
                      'b': 2,
                      'c': 3},
                'c
                  c': {'b': 'a 
                              a',
                       'c': {}}}},
 'c': {'a': 1,
       'b': 2,
       'c': 3}}
 ```
