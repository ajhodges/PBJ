# -*- coding: utf-8 -*-
"""
    jinja2
    ~~~~~~

    Jinja2 is a template engine written in pure Python.  It provides a
    Django inspired non-XML syntax but supports inline expressions and
    an optional sandboxed environment.

    Nutshell
    --------

    Here a small example of a Jinja2 template::

        {% extends 'base.html' %}
        {% block title %}Memberlist{% endblock %}
        {% block content %}
          <ul>
          {% for user in users %}
            <li><a href="{{ user.url }}">{{ user.username }}</a></li>
          {% endfor %}
          </ul>
        {% endblock %}


    :copyright: (c) 2010 by the Jinja Team.
    :license: BSD, see LICENSE for more details.
"""
__docformat__ = 'restructuredtext en'
__version__ = '2.6'

# high level interface
from environment import Environment, Template

# loaders
from loaders import BaseLoader, FileSystemLoader, PackageLoader, \
     DictLoader, FunctionLoader, PrefixLoader, ChoiceLoader, \
     ModuleLoader

# bytecode caches
from bccache import BytecodeCache, FileSystemBytecodeCache, \
     MemcachedBytecodeCache

# undefined types
from runtime import Undefined, DebugUndefined, StrictUndefined

# exceptions
from exceptions import TemplateError, UndefinedError, \
     TemplateNotFound, TemplatesNotFound, TemplateSyntaxError, \
     TemplateAssertionError

# decorators and public utilities
from filters import environmentfilter, contextfilter, \
     evalcontextfilter
from utils import Markup, escape, clear_caches, \
     environmentfunction, evalcontextfunction, contextfunction, \
     is_undefined

__all__ = [
    'Environment', 'Template', 'BaseLoader', 'FileSystemLoader',
    'PackageLoader', 'DictLoader', 'FunctionLoader', 'PrefixLoader',
    'ChoiceLoader', 'BytecodeCache', 'FileSystemBytecodeCache',
    'MemcachedBytecodeCache', 'Undefined', 'DebugUndefined',
    'StrictUndefined', 'TemplateError', 'UndefinedError', 'TemplateNotFound',
    'TemplatesNotFound', 'TemplateSyntaxError', 'TemplateAssertionError',
    'ModuleLoader', 'environmentfilter', 'contextfilter', 'Markup', 'escape',
    'environmentfunction', 'contextfunction', 'clear_caches', 'is_undefined',
    'evalcontextfilter', 'evalcontextfunction'
]
