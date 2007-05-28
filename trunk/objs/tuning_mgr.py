"""
    Tunings module. This module keeps a collection of tunings, and some 
    functions to get tuning classes from it, or establish some relations
"""

import db.tuning_mgr_peer

class TuningMgr(object):
    def __init__(self):
        self._list = []

    def GetTuningById(self, id):
        """ Returns tuning instance belonging to the ID """
        for s in self._list:
            if s._id == id:
                return s
        return None

    def GetDefaultTuning(self):
        for s in self._list:
            if s._tuningName == 'Standard':
                return s
        return None

__mgr = None

def Get():
    global __mgr
    if __mgr == None:
        __mgr = TuningMgr()
    return __mgr

# TODO: This should be in the peer
def RestoreFromDb(conn):
    mgr = Get()
    p = db.tuning_mgr_peer.TuningMgrPeer(conn)
    mgr._list = p.Restore()
        
