"""
    Tunings module. This module keeps a collection of tunings, and some 
    functions to get tuning classes from it, or establish some relations
"""

from db import category_mgr_peer

class CategoryMgr(object):
    def __init__(self):
        self._list = []

    def GetCategoryById(self, id):
        """ Returns a caegory object or None when there 
            was no category with that ID """
        for s in self._list:
            if s._id == id:
                return s
        return None

    def GetCategoryByName(self, name):
        """ Returns a category object or None when there 
            was no category with that name """
        for s in self._list:
            if s._name == name:
                return s
        return None

__mgr = None

def Get():
    global __mgr
    if __mgr == None:
        __mgr = CategoryMgr()
    return __mgr

# TODO: This needs to be in the peer
def RestoreFromDb(conn):
    mgr = Get()
    p = category_mgr_peer.CategoryMgrPeer(conn)
    mgr._list = p.Restore()
