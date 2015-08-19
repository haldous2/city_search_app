
# city_search_app
City search app written in python running via uwsgi + nginx

### Problem Statement
read a partial city name, output a JSON list of cities that match search. This might be used as a return for an autocompleted city input or ajaxified return input.


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

0. install uwsgi, nginx - setup accordingly

0. install uwsgi.ini files, add nginx configurations for uwsgi

0. run test server via command line or run live
