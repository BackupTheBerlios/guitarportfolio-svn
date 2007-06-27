import datetime
from wx.lib.pubsub import Publisher

import db

LOG_UNDEFINED           = 0  # not defined
LOG_STATUSCHANGE        = 1  # change to other status
LOG_PROGRESS_CHANGE_ACC = 2  # change to accuracy  0 - 10
LOG_PROGRESS_CHANGE_CMP = 3  # change to completed 0 - 10
LOG_MESSAGE             = 4  # a message 

class LogItem(db.base.Object):
    """ Log item contains one log line, with a time stamp, type and optional
        message """
        
    def __init__(self, id = -1):
        super(LogItem, self).__init__(id) 
        self._type = LOG_UNDEFINED
        self._text = ''
        self._value = 0
        self._date = datetime.datetime.now()     
  
    def tostr(self):
        str = 'Log Entry: ' + self._date.strftime('%Y %m %d %H:%M:%S') + ' -- ' + repr(self._type) + ' "' + self._text + '" ' + repr(self._value) 
        return str

# =============================================================================
    
