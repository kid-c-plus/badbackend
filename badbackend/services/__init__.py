"""Using a very aggressive import policy, import all .py files in this 
directory and add all BaseService subclass definitions to the
`service_classes` dictionary, which external scripts will then 
interact with to create Service objects."""

import os
import glob
import importlib

from .baseservice import BaseService

# As the docstring states, this is a *very* aggressive import policy
# and kinda runs counter to standard namespace practices. My reasoning
# for doing things this way is that I want creating a BaseService
# subclass in this directory to be the only step required to add a new
# service to this API's repertoire, and I want supplying the subclass
# name to config.yaml's EnabledServices stanza to be the only step
# required to enable it. I also *don't* want to assume that the
# ExampleService class definition is stored in the exampleservice.py
# file, as that's kind of a flimsy and counterintuitive assumption.
# So, I'm happy to do a bit of dirty work behind the scenes to make
# things easier for users hoping to expand this API's functionality,

service_classes = {}

modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
for module in [os.path.basename(module)[:-3] for module in modules 
               if not module.endswith("__init__.py")]:

    module_obj = importlib.import_module("services.%s" % module)
    bs_subclasses = dict((name, obj) for name, obj in 
                         module_obj.__dict__.items() if
                         type(obj) == type(object) and
                         obj != BaseService and
                         issubclass(obj, BaseService))
    service_classes.update(bs_subclasses)
