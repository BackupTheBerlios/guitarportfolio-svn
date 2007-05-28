import db
from objs import tuning

class TuningPeer(db.base.Peer):
    def __init__(self, conn):
        super(TuningPeer, self).__init__(conn)        
    
    # --------------------------------------------------------------------------
    def Restore(self, obj):
        sql = 'select tuning_name, tuning_text from tuning where id = ?'
        
        r = self._ExecuteRestore(obj, sql)
        obj._tuningName = r[0]
        obj._tuningText = r[1]
    
    # --------------------------------------------------------------------------
    def Update(self, obj):
        self._UpdateError(obj)
