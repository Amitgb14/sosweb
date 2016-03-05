import json
import collections



def _open(location):

    global data
    data = ""
    with open(location+'/sos_reports/sos.json') as fread:
        data = json.load(fread)
    
    data = collections.OrderedDict(sorted(data.items()))

def plugin_read(location):

    _open(location)
    return data


