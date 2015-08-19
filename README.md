
# city_search_app
City search app written in python running via uwsgi + nginx

```

# MuttSlicer
A list-like object that can apply list element methods across a slice

```python
>>> from muttslicer import Slicer
>>> x = Slicer( FooClass, [FooClass(),FooClass(),...] )
>>> x[1:100].foo_instance_func()
```

### Problem Statement
A creative and playful engineer once noted, "I can do this: `alist[1].method_call()`. I want to do this: `alist[1:100].method_call()`". And thus a mildly-useful-but-still-absurd data type was born.


### Example
Given classes that hold state and functions that mutate state below. Do stuff like [this over here](docs/muttslicer_example.ipynb)

```python
class AbstractBase(object):

    def combine(self,update_dict):
        raise NotImplemented('you must implement combine')

    def flatten(self):
        raise NotImplemented('you must implement flatten')

    def merge(self,update_dict):
        raise NotImplemented('you must implement merges')

class Foo(AbstractBase):

    def __init__(self,data_dict):
        self.data_dict = data_dict

    def __str__(self):
        return "{}{}".format(
            type(self).__name__,
            self.data_dict
        )

    def __repr__(self):
        return "{}{}".format(
            type(self).__name__,
            self.data_dict
        )

    def combine(self,update_dict):
        self.data_dict['combine'] = zip(self.data_dict.keys(),update_dict.values())

    def flatten(self):
        self.data_dict['flatten'] = self.data_dict.items()

    def merge(self,update_dict):
        self.data_dict.update(**update_dict)

class Bar(AbstractBase):

    def __init__(self,data_list):
        self.data_list = data_list

    def __str__(self):
        return "{}{}".format(
            type(self).__name__,
            self.data_list
        )

    def __repr__(self):
        return "{}{}".format(
            type(self).__name__,
            self.data_list
        )

    def combine(self,update_dict):
        self.data_list.append(
            zip(self.data_list,update_dict.keys())
        )

    def flatten(self):
        pass

    def merge(self,update_dict):
        self.data_list.extend(update_dict.keys())
        self.data_list.extend(update_dict.values())
```


### Installation
0. clone the repsitory

0. run `python setup.py develop`. Requires `setuptools` to be installed

0. look at the tests
