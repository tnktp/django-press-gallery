from django.http import HttpResponse
from django.utils import simplejson
from django.utils.encoding import force_unicode
from django.utils.functional import Promise

class LazyEncoder(simplejson.JSONEncoder):
    def default(self, o):
        if isinstance(o, Promise):
            return force_unicode(o)
        else:
            return super(LazyEncoder, self).default(o)

class JSONResponse(HttpResponse):
    def __init__(self, status, data={}):
        HttpResponse.__init__(
            self, content=simplejson.dumps(data, cls=LazyEncoder),
            mimetype="application/json",
            status=status,
        )