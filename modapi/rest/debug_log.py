import logging
import json
from modapi.rest.schema import Flag

debuglog=logging.getLogger(__file__)
debuglog.setLevel(logging.DEBUG)

file_handler=logging.FileHandler('debug.log', mode='a')
# file_formatter=logging.Formatter(json.dumps({'time':'%(asctime)s',
#                                              'message':
#                                              '%(message)s'}))
# file_handler.setFormatter(file_formatter)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            'time': self.formatTime(record, self.datefmt),
            'func': record.funcName,
            'file': record.pathname,
            'msg': record.getMessage()
        })


file_handler.setFormatter(JsonFormatter())

def filter_msgs(record):
    return __file__ == record.name

file_handler.addFilter(filter_msgs)
debuglog.addHandler(file_handler)
debuglog.propagate = False


def msg(user, payload=None, status_code=200):
    return {"user":user,
            "payload": payload,
            "status_code":status_code}
