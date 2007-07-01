import db.base

class Tuning(db.base.Object):
    def __init__(self, id = -1):
        super(Tuning, self).__init__(id)        
        self._tuningName = ''
        self._tuningText = ''
    
