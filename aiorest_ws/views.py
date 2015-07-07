# -*- coding: utf-8 -*-
"""
    This module provide a class-based views inspired by Django/Flask
    frameworks and can be used with aiorest-ws routers.

    :copyright: (c) 2015 by Savich Valeryi.
    :license: MIT, see LICENSE for more details.
"""

from exceptions import NotSpecifiedHandler, NotSpecifiedMethodName, \
    IncorrectMethodNameType


__all__ = ('http_methods', 'View', 'MethodViewMeta', 'MethodBasedView',)

http_methods = frozenset(['get', 'post', 'head', 'options', 'delete', 'put',
                          'trace', 'patch'])


class View(object):
    """Subclass for implementing class-based views."""
    @classmethod
    def as_view(cls, name, *class_args, **class_kwargs):
        """Converts the class into an actual view function that can be used
        with the routing system.
        """
        pass


class MethodViewMeta(type):
    """Metaclass, which helps to define list of supported methods in
    class-based views.
    """
    def __new__(cls, name, bases, attrs):
        obj = type.__new__(cls, name, bases, attrs)
        # if not defined 'method' attribute, then make and append him to
        # our class-based view
        if 'methods' not in attrs:
            methods = set(obj.methods or [])
            for key in attrs:
                if key in http_methods:
                    methods.add(key.upper())
            # this action necessary for appending list of supported methods
            if methods:
                obj.methods = sorted(methods)
        return obj


class MethodBasedView(View, metaclass=MethodViewMeta):
    """Class-based view for aiorest-ws framework."""

    def dispatch(self, request, *args, **kwargs):
        """Search the most suitable handler for request.

        :param request: passed request from user
        :param args: list of arguments passed from router
        :param kwargs: dictionary passed from router
        """

        method = request.pop('method', None)

        # invoked, when user not specified method in query (e.c. get, post)
        if not method:
            raise NotSpecifiedMethodName()

        # invoked, when user specified method name as not a string
        if not isinstance(method, str):
            raise IncorrectMethodNameType()

        # trying to find the most suitable handler
        method = method.lower().strip()
        handler = getattr(self, method, None)
        if not handler:
            raise NotSpecifiedHandler()
        return handler(request, *args, **kwargs)
