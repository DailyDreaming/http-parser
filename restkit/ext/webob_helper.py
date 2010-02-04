# -*- coding: utf-8 -
#
# This file is part of restkit released under the MIT license. 
# See the NOTICE for more information.


import restkit.errors
import webob.exc

class WebobResourceError(webob.exc.WSGIHTTPException):

    def __init__(self, msg=None, http_code=None, response=None):
        webob.exc.WSGIHTTPException.__init__(self)
        
        http_code = http_code or 500
        klass = webob.exc.status_map[http_code]
        self.code = http_code
        self.title = klass.title
        self.status = '%s %s' % (self.code, self.title)
        self.explanation = msg
        self.response = response
        # default params
        self.msg = msg

    def _status_int__get(self):
        """
        The status as an integer
        """
        return int(self.status.split()[0])
    def _status_int__set(self, value):
        self.status = value
    status_int = property(_status_int__get, _status_int__set, doc=_status_int__get.__doc__)
    
    status_code = restkit.errors.deprecated_property(
        status_int, 'status_code', 'use .status_int instead',
        warning=False)

    def _get_message(self):
        return self.explanation
    def _set_message(self, msg):
        self.explanation = msg or ''
    message = property(_get_message, _set_message)

webob_exceptions = False
def wrap_exceptions():
    """ wrap restkit exception to return WebBob exceptions"""
    global webob_exceptions
    if webob_exceptions: return
    restkit.errors.ResourceError = WebobResourceError
    webob_exceptions = True
    