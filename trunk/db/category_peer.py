import db

class CategoryPeer(db.base.Peer):
    # --------------------------------------------------------------------------
    def __init__(self, conn):
        super(CategoryPeer, self).__init__(conn)        
    
    # --------------------------------------------------------------------------
    def Restore(self, obj):
        sql = 'select name from category where id = ?'
        
        r = self._ExecuteRestore(obj, sql)
        obj._name = r[0]
                
    # --------------------------------------------------------------------------
    def Update(self, obj):
        if obj._id == -1:
            sql = 'insert into category (name) values (?)'
        else:
            sql = 'update category set name = ? where id = ?'
        data = (obj._name,)
        
        self._ExecuteUpdate(obj, sql, data)

    # --------------------------------------------------------------------------
    def Delete(self, obj):
        sql = 'delete from category where id = ?'
        r = self._ExecuteDelete(obj, sql)
