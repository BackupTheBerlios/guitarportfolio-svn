import db.category_peer
from objs import category

# TODO: Should be called CategorySetPeer

class CategoryMgrPeer(db.base.Peer):
    def __init__(self, conn):
        super(CategoryMgrPeer, self).__init__(conn)        
    
    # --------------------------------------------------------------------------
    def Restore(self):
        
        sql = 'select id from category'
        r = self._ExecuteRestore(None, sql, all = True)

        list = []
        p = db.category_peer.CategoryPeer(self._conn)
        for t in r:
            cat = category.Category(t[0])
            p.Restore(cat)
            list.append(cat)

        return list
