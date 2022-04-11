# Prettier - properly pprint of nested objects

If you are trying to output nested data structures, each of which is individually displayed as a dictionary representation, the nesting levels are not separated, such an output is difficult to perceive.
```
from prettier import PrintMixin, PPrintMixin


class A(PrintMixin):
    def __init__(self):
        self.attrs = ('a', 'b', 'c')
        self.a = 10
        self.b = {'a': 1, 'b': 2, 'c': 3}
        self.c = B()


class B(PrintMixin):
    def __init__(self):
        self.b = 200
        self.c = C()
        self.d = 10
        setattr(self, 'a \n a', {'a': 1, 'b': C(), 'c': 3})


class C(PrintMixin):
    def __init__(self):
        self.a = ('b', 'c')
        self.b = 'a \n a'
        self.c = {}
```
You can expect the following output:
```
{'a': 10,
 'attrs': ('a', 'b', 'c'),
 'b': {'a': 1, 'b': 2, 'c': 3},
 'c': {'a \n a': {'a': 1, 'b': {'a': ('b', 'c'), 'b': 'a \n a', 'c': {}}, 'c': 3},
 'b': 200,
 'c': {'a': ('b', 'c'), 'b': 'a \n a', 'c': {}},
 'd': 10}}
```
But if you use a ```PPrintMixin``` instead of the standard one, then you can expect the following output:
```
{'attrs': ('a', 'b', 'c'),
 'a': 10,
 'b': {'a': 1,
       'b': 2,
       'c': 3},
 'c': {'b': 200,
       'c': {'a': ('b', 'c'),
             'b': 'a \n a',
             'c': {}},
       'd': 10,
       'a \n a': {'a': 1,
                  'b': {'a': ('b', 'c'),
                        'b': 'a \n a',
                        'c': {}},
                  'c': 3}}}
```
Note that the string keys and values are processed using ```pprint```. If you want to change the behavior using the ```str``` function, you can use ```MixinFactory``` and specify the ```pp``` parameter. Like this:
```
from prettier import MixinFactory


MyMixin = MixinFactory(pp=False)
```
You can expect the following output:
```
{'attrs': ('a', 'b', 'c'),
 'a': 10,
 'b': {'a': 1,
       'b': 2,
       'c': 3},
 'c': {'b': 200,
       'c': {'a': ('b', 'c'),
             'b': 'a 
                    a',
             'c': {}},
       'd': 10,
       'a 
         a': {'a': 1,
              'b': {'a': ('b', 'c'),
                    'b': 'a 
                           a',
                    'c': {}},
              'c': 3}}}
```
You can even use the ```endpoint``` argument. This is the name of the attribute that stores the list of arguments to print. Lets comnibe som Mixins, like this:
```
from prettier import MixinFactory

AttrsPrintMixin = MixinFactory(pp=False, endpoint='attrs')
APrintMixin = MixinFactory(pp=False, endpoint='a')
PrintMixin = MixinFactory(pp=False)


class A(AttrsPrintMixin):
    def __init__(self):
        self.attrs = ('a', 'b', 'c')
        self.a = 10
        self.b = {'a': 1, 'b': 2, 'c': 3}
        self.c = B()


class B(PrintMixin):
    def __init__(self):
        self.b = 200
        self.c = C()
        self.d = 10
        setattr(self, 'a \n a', {'a': 1, 'b': C(), 'c': 3})


class C(APrintMixin):
    def __init__(self):
        self.a = ('b', 'c')
        self.b = 'a \n a'
        self.c = {}
```
 
The output will be:
```
{'a': 10,
 'b': {'a': 1,
       'b': 2,
       'c': 3},
 'c': {'b': 200,
       'c': {'b': 'a 
                    a',
             'c': {}},
       'd': 10,
       'a 
         a': {'a': 1,
              'b': {'b': 'a 
                           a',
                    'c': {}},
              'c': 3}}}
 ```
