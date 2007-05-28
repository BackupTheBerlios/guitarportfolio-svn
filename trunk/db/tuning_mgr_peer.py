import db
from db import tuning_peer
from objs import tuning

# TODO: Should be called TuningSetpeer

class TuningMgrPeer(db.base.Peer):
    def __init__(self, conn):
        super(TuningMgrPeer, self).__init__(conn)        
    
    # --------------------------------------------------------------------------
    def Restore(self):
        sql = 'select id from tuning'
        r = self._ExecuteRestore(None, sql)

        list = []
        p = tuning_peer.TuningPeer(self._conn)
        for t in r:
            tun = tuning.Tuning(t[0])
            p.Restore(tun)
            list.append(tun)

        return list
